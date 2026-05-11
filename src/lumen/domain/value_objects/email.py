# from dataclasses import dataclass

# from email_validator import validate_email, EmailNotValidError
# from lumen.domain.exceptions import InvalidEmailError


# @dataclass(frozen=True, slots=True)
# class Email:
#     value: str

#     def __post_init__(self) -> None:
#         try:
#             valid = validate_email(self.value, check_deliverability=False)
#         except EmailNotValidError as exc:
#             raise InvalidEmailError(self.value) from exc

#         object.__setattr__(self, "value", valid.normalized)

#     def __str__(self) -> str:
#         return self.value
