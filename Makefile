# Environment
ENV ?= dev
VALID_ENVS := dev prod

ifneq ($(strip $(env)),)
	ENV := $(env)
endif

ifeq (,$(filter $(ENV),$(VALID_ENVS)))
$(error ENV must be one of: $(VALID_ENVS))
endif

DOCKER_COMPOSE_FILE = $(if $(filter $(ENV),prod),$(CURDIR)/docker/docker-compose.yaml,$(CURDIR)/docker/docker-compose-dev.yaml)
ENV_FILE ?= $(if $(filter $(ENV),prod),$(CURDIR)/.env.prod,$(CURDIR)/.env)
DOCKER_COMPOSE = ENV_FILE=$(ENV_FILE) docker compose -f $(DOCKER_COMPOSE_FILE) --env-file $(ENV_FILE)

USE_GPU ?= $(shell grep "^USE_GPU=" $(ENV_FILE) 2>/dev/null | cut -d'=' -f2 | tr -d '[:space:]')
CLI_SERVICE = $(if $(filter true,$(USE_GPU)),cli-gpu,cli-cpu)
INSTALL_DIR = $(HOME)/.local/bin

# Default Target
.DEFAULT_GOAL := help

# Colors
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

# -----------------
# 🐳 Docker Targets
# -----------------

.PHONY: up
up: ## Start all Docker Compose services in the background
	@echo "$(GREEN)Starting all Docker services...$(RESET)"
	$(DOCKER_COMPOSE) up -d $(UP_FLAGS)

.PHONY: up-build
up-build: UP_FLAGS := --build
up-build: up ## Start all services and rebuild images

.PHONY: up-recreate
up-recreate: UP_FLAGS := --build --force-recreate
up-recreate: up ## Start all services with rebuild and force recreate

.PHONY: down
down: ## Stop and remove containers and networks
	@echo "$(YELLOW)Stopping all Docker services...$(RESET)"
	$(DOCKER_COMPOSE) down

.PHONY: clean
clean: ## Stop and remove containers, networks, and VOLUMES
	@echo "$(RED)Cleaning all Docker resources and volumes...$(RESET)"
	$(DOCKER_COMPOSE) down -v

.PHONY: logs
logs: ## View the logs of all Docker Compose containers
	$(DOCKER_COMPOSE) logs -f

.PHONY: config
config: ## Validate and print resolved Docker Compose config
	$(DOCKER_COMPOSE) config

.PHONY: db
db: ## Start the database service
	@echo "$(GREEN)Starting database...$(RESET)"
	$(DOCKER_COMPOSE) up -d db

.PHONY: cli-cpu
cli-cpu: ## Start the CLI service (CPU)
	@echo "$(GREEN)Starting CLI service (CPU)...$(RESET)"
	$(DOCKER_COMPOSE) up -d cli-cpu

.PHONY: cli-gpu
cli-gpu: ## Start the CLI service (GPU)
	@echo "$(GREEN)Starting CLI GPU service...$(RESET)"
	$(DOCKER_COMPOSE) up -d cli-gpu

.PHONY: install-cli
install-cli:
	@echo "$(GREEN)Installing the CLI tool...$(RESET)"
	@mkdir -p $(INSTALL_DIR)
	@sed -e "s|__DOCKER_COMPOSE_FILE__|$(DOCKER_COMPOSE_FILE)|g" \
	     -e "s|__ENV_FILE__|$(ENV_FILE)|g" \
	     -e "s|__CLI_SERVICE__|$(CLI_SERVICE)|g" \
	     scripts/lumen > $(INSTALL_DIR)/lumen
	@chmod +x $(INSTALL_DIR)/lumen
	@$(DOCKER_COMPOSE) exec -e _LUMEN_COMPLETE=bash_source $(CLI_SERVICE) lumen > $(HOME)/.lumen-complete.bash 2>/dev/null || echo "# Completion failed" > $(HOME)/.lumen-complete.bash
	@grep -qxF 'source $(HOME)/.lumen-complete.bash' $(HOME)/.bashrc || echo 'source $(HOME)/.lumen-complete.bash' >> $(HOME)/.bashrc
	@echo "$(GREEN)Done!$(RESET)"

.PHONY: migrate
migrate: ## Apply database migrations using Alembic
	@echo "$(GREEN)Applying database migrations...$(RESET)"
	alembic upgrade head

.PHONY: makemigrations
makemigrations: ## Autogenerate a new migration (Usage: make makemigrations msg="your message")
	@echo "$(GREEN)Creating new migration...$(RESET)"
	alembic revision --autogenerate -m "$(msg)"

.PHONY: clean-py
clean-py: ## Remove unnecessary python cache files
	@echo "$(YELLOW)Cleaning up __pycache__ and unused files...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: format
format: ## Format Python code using Ruff
	@echo "$(GREEN)Formatting code with Ruff...$(RESET)"
	ruff format

.PHONY: lint
lint: ## Format Python code using Ruff
	@echo "$(GREEN)Checking code with Ruff...$(RESET)"
	ruff check

.PHONY: type-check
type-check: ## Format Python code using Ruff
	@echo "$(GREEN)Checking code with Ruff...$(RESET)"
	mypy src/

.PHONY: help
help: ## Display this help
	@echo ''
	@echo 'Usage:'
	@echo '  $(YELLOW)make$(RESET) $(GREEN)<target>$(RESET)'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(GREEN)%s$(RESET)\n", $$1, $$2}' $(MAKEFILE_LIST)
