# Environment
ENV ?= dev
VALID_ENVS := dev prod

ifeq (,$(filter $(ENV),$(VALID_ENVS)))
$(error ENV must be one of: $(VALID_ENVS))
endif

ENV_FILE = $(CURDIR)/.env
-include $(ENV_FILE)

ACTIVE_PROFILE = $(if $(filter true,$(USE_GPU)),gpu,cpu)
DOCKER_COMPOSE_FILE = $(if $(filter $(ENV),prod),$(CURDIR)/docker/docker-compose.yaml,$(CURDIR)/docker/docker-compose-dev.yaml)
DOCKER_COMPOSE = USER_ID=$$(id -u) GROUP_ID=$$(id -g) ENV_FILE=$(ENV_FILE) COMPOSE_PROFILES=$(ACTIVE_PROFILE) docker compose -f $(DOCKER_COMPOSE_FILE) --env-file $(ENV_FILE)


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
	mkdir -p $(EMBEDDING_CACHE_DIR)
	$(DOCKER_COMPOSE) up -d $(UP_FLAGS)

.PHONY: up-build
up-build: UP_FLAGS := --build
up-build: up ## Start all services and rebuild images

.PHONY: up-recreate
up-recreate: UP_FLAGS := --build --force-recreate
up-recreate: up ## Start all services with rebuild and force recreate

.PHONY: db
db: ## Start the database service
	@echo "$(GREEN)Starting database...$(RESET)"
	$(DOCKER_COMPOSE) up -d db

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

.PHONY: install-cli
install-cli:
	@mkdir -p $(HOME)/.local/bin
	@chmod +x $(CURDIR)/scripts/lumen
	@ln -sf $(CURDIR)/scripts/lumen $(HOME)/.local/bin/lumen
	@echo "CLI installed. Restart terminal or run: source ~/.bashrc"

.PHONY: migrate
migrate: ## Apply database migrations using Alembic
	@echo "$(GREEN)Applying database migrations...$(RESET)"
	alembic upgrade head

.PHONY: makemigrations
makemigrations: ## Autogenerate a new migration (Usage: make makemigrations msg="your message")
	@echo "$(GREEN)Creating new migration...$(RESET)"
	alembic revision --autogenerate -m "$(msg)"

.PHONY: dump-quotes
dump-quotes: ## Create a compressed dump of quotes
	@echo "$(GREEN)Exporting quotes to assets/quotes.dump...$(RESET)"
	$(DOCKER_COMPOSE) exec -T db sh -c 'pg_dump -U $$POSTGRES_USER -d $$POSTGRES_DB -t quotes -t quote_embeddings -F c' > assets/quotes.dump

.PHONY: restore-quotes
restore-quotes: ## Restore quotes from assets/quotes.dump
	@echo "$(YELLOW)Restoring quotes from assets/quotes.dump...$(RESET)"
	$(DOCKER_COMPOSE) exec -T db sh -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB -c "DROP TABLE IF EXISTS quote_embeddings CASCADE; DROP TABLE IF EXISTS quotes CASCADE;"'
	$(DOCKER_COMPOSE) exec -T db sh -c 'pg_restore -U $$POSTGRES_USER -d $$POSTGRES_DB --no-owner --no-privileges -t quotes -t quote_embeddings -1' < assets/quotes.dump

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
