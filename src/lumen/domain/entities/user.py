# from uuid import UUID, uuid4
# from dataclasses import dataclass, field
# from datetime import datetime, timezone

# from lumen.domain.enums import AuthProvider
# from lumen.domain.value_objects import Identity, EmailIdentity, CLIIdentity


# @dataclass(slots=True)
# class User:
#     name: str
#     identities: list[Identity] = field(default_factory=list[Identity])
#     created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
#     updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
#     id: UUID = field(default_factory=uuid4)

#     def __post_init__(self) -> None:
#         self.rename(self.name)

#     def add_identity(self, identity: Identity) -> None:
#         """
#         Links a new identity to the user profile.

#         :param identity: The identity entity to be added (e.g., Email).
#         :type identity: Identity
#         :raises IdentityAlreadyExistsError: If an identity with the same provider already exists.
#         """
#         if self.has_identity(identity.provider):
#             raise IdentityAlreadyExistsError(identity.provider)

#         self.identities.append(identity)

#     def revoke_identity(self, provider: AuthProvider) -> None:
#         """
#         Revokes (removes) an identity from the user profile.

#         Prevents removing the identity if it is the only one remaining,
#         ensuring the user always has at least one method to log in.

#         :param provider: The authentication provider to remove.
#         :type provider: AuthProvider
#         :raises LastIdentityRevokeError: If attempting to remove the last remaining identity.
#         """
#         if len(self.identities) <= 1:
#             raise LastIdentityRevokeError(provider)

#         self.identities = [i for i in self.identities if i.provider != provider]

#     @property
#     def email_identity(self) -> EmailIdentity | None:
#         """
#         Retrieves the Email identity associated with the user, if any.

#         :return: The EmailIdentity object or None if not found.
#         :rtype: EmailIdentity | None
#         """
#         return next((i for i in self.identities if isinstance(i, EmailIdentity)), None)

#     @property
#     def cli_identity(self) -> CLIIdentity | None:
#         """
#         Retrieves the CLI identity associated with the user, if any.

#         :return: The CLIIdentity object or None if not found.
#         :rtype: CLIIdentity | None
#         """
#         return next((i for i in self.identities if isinstance(i, CLIIdentity)), None)

#     def has_identity(self, provider: AuthProvider) -> bool:
#         """
#         Checks if the user has a linked identity for the specified provider.

#         :param provider: The provider to check.
#         :type provider: AuthProvider
#         :return: True if the identity exists, False otherwise.
#         :rtype: bool
#         """
#         return any(i.provider == provider for i in self.identities)

#     def rename(self, value: str) -> None:
#         normalized = value.strip()
#         if not (MIN_USER_NAME_LENGTH <= len(normalized) <= MAX_USER_NAME_LENGTH):
#             raise UserInvalidNameError(value)
#         if normalized[0] in ALLOWED_NAME_SEPARATORS:
#             raise UserInvalidNameError(value)
#         if normalized[-1] in ALLOWED_NAME_SEPARATORS:
#             raise UserInvalidNameError(value)
#         if any(not self._is_valid_name_symbol(symbol) for symbol in normalized):
#             raise UserInvalidNameError(value)
#         if any(
#             left in ALLOWED_NAME_SEPARATORS and right in ALLOWED_NAME_SEPARATORS
#             for left, right in pairwise(normalized)
#         ):
#             raise UserInvalidNameError(value)

#         self.name = normalized

#     @staticmethod
#     def _is_valid_name_symbol(symbol: str) -> bool:
#         return (
#             unicodedata.category(symbol).startswith(("L", "M"))
#             or symbol in ALLOWED_NAME_SEPARATORS
#         )
