# from dataclasses import dataclass, field
# from typing import Literal
# from abc import ABC, abstractmethod

# from lumen.domain.enums import AuthProvider
# from .email import Email


# @dataclass(frozen=True, slots=True, kw_only=True)
# class Identity(ABC):
#     """
#     Base abstract class representing a user identity.

#     Defines the contract for all authentication methods in the system.
#     Ensures that every identity has a provider type and a method to retrieve
#     a string identifier.
#     """

#     provider: AuthProvider

#     @property
#     @abstractmethod
#     def identifier(self) -> str:
#         """
#         Returns the unique identifier of the entity as a string.
#         """
#         pass


# @dataclass(frozen=True, slots=True, kw_only=True)
# class EmailIdentity(Identity):
#     """
#     Represents user identity via Email and Password (Web Login).

#     Used for standard website registration.
#     """

#     provider: Literal[AuthProvider.EMAIL] = AuthProvider.EMAIL
#     email: Email
#     password_hash: str
#     avatar_url: str | None = field(default=None)

#     @property
#     def identifier(self) -> str:
#         """Returns the email as the identifier."""
#         return self.email.value


# @dataclass(frozen=True, slots=True, kw_only=True)
# class CLIIdentity(Identity):
#     """
#     Represents user identity via CLI.
#     """

#     provider: Literal[AuthProvider.CLI] = AuthProvider.CLI
#     username: str
#     password_hash: str

#     @property
#     def identifier(self) -> str:
#         """Returns the user name as the identifier."""
#         return self.username
