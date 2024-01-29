import logging

from django.contrib.auth import get_user_model

import pyotp

from ...helper.errors import (
    OTPMsg as OTPErr,
    TOTPMsg as TOTPErr
)
from ...helper import exceptions as exc
from ...helper.text_choices import OTPReasonOptions
from ...helper.typings import (
    Minutes,
    PositiveInt
)

logger = logging.getLogger(__name__)
User = get_user_model()

class OTPService:
    """
    The OTP Service class provides methods to generate, validate, and expire
    one-time password (OTP) tokens.
    """

    @staticmethod
    def generate_totp_token(
            user: User,
            token_length: PositiveInt = 6,
            lifespan: Minutes = 10) -> pyotp.TOTP:

        logger.info(f"Generating an OTP token for user {user} with type TOTP.")
        if not user:
            logger.warning("Invalid `user` provided for Creating TOTP Token.")
            raise exc.TokenError()

        if not (4 <= token_length <= 13):
            err_msg = OTPErr.TOKEN_LENGTH.format(token_length=token_length)
            logger.warning(err_msg)
            raise exc.TokenLengthError(err_msg)

        if lifespan < 1:
            err_msg = TOTPErr.LIFESPAN.format(lifespan=lifespan)
            logger.warning(err_msg)
            raise exc.TokenLifeSpanError(err_msg)

        totp = pyotp.TOTP(
            pyotp.random_base32(),
            digits=token_length,
            interval=Minutes(lifespan * 60)
        )

        return totp

    @staticmethod
    def validate_totp_token(
            user: User,
            totp: pyotp.TOTP,
            token: str,
            reason: OTPReasonOptions) -> bool:
        """
        Validates a one-time password (OTP) token for the given user and reason.
        The validation process checks whether the provided token matches an
        existing, active OTP token for the user, and verifies that it has not
        expired.

        Args:
            user (User): The user for whom the OTP token is being validated.
            token (str): The OTP token to be validated
            reason (OTPReasonOptions): The reason for the token's creation.

        Raises:
            TokenError: This method checks totp object must be instance of pyotp.TOTP

        Returns:
            bool: True if the OTP token is valid and not expired, otherwise False.
        """
        logger.info(f"Verifying an OTP token for user {user} with type TOTP.")
        is_token_verified = False

        if not user or not totp or not token or not reason:
            logger.debug("Invalid input provided for validating OTP Token.")
            is_token_verified = False

        if not isinstance(totp, pyotp.TOTP):
            logger.debug("Invalid Token. Token must be an instance of `pyotp.TOTP`.", exc_info=True)
            raise exc.TokenError("Token must be an instance of `pyotp.TOTP`.")

        if totp.verify(token):
            logger.info(f"Provided token is valid for user: {user}.")
            is_token_verified = True
        else:
            logger.warning(f"Provided token is expired or invalid for user: {user}.")
            is_token_verified = False

        return is_token_verified

    @staticmethod
    def generate_hotp_token(
            user: User,
            token_length: PositiveInt = 6,
            initial_counter: int = 0) -> tuple[pyotp.HOTP, int]:
        """
        Generates a HOTP token for the given user.

        Args:
            user (User): The user for whom the HOTP token is generated.
            token_length (PositiveInt): The length of the HOTP token (default: 6).
            initial_counter (int): The initial counter value for HOTP (default: 0).

        Returns:
            Tuple[pyotp.HOTP, int]: A tuple containing the generated HOTP instance and
            the initial counter value.
        """
        logger.info(f"Generating a HOTP token for user {user}.")

        if not user:
            logger.warning("Invalid `user` provided for creating HOTP Token.")
            raise exc.TokenError()

        if not (4 <= token_length <= 13):
            err_msg = OTPErr.TOKEN_LENGTH.format(token_length=token_length)
            logger.warning(err_msg)
            raise exc.TokenLengthError(err_msg)

        hotp = pyotp.HOTP(pyotp.random_base32(), digits=token_length)
        return hotp, initial_counter

    @staticmethod
    def validate_hotp_token(
            user: User,
            hotp: pyotp.HOTP,
            token: str,
            reason: OTPReasonOptions,
            counter: int) -> bool:
        """
        Validates a HOTP token for the given user and reason.

        Args:
            user (User): The user for whom the HOTP token is being validated.
            hotp (pyotp.HOTP): The HOTP instance used for validation.
            token (str): The HOTP token to be validated.
            reason (OTPReasonOptions): The reason for the token's creation.
            counter (int): The counter value to use for validation.

        Returns:
            bool: True if the HOTP token is valid, otherwise False.
        """
        logger.info(f"Verifying a HOTP token for user {user}.")
        is_token_verified = False

        if not user or not hotp or not token or not reason or counter is None:
            logger.debug("Invalid input provided for validating HOTP Token.")
            is_token_verified = False

        if not isinstance(hotp, pyotp.HOTP):
            logger.debug("Invalid Token. Token must be an instance of `pyotp.HOTP`.", exc_info=True)
            raise exc.TokenError("Token must be an instance of `pyotp.HOTP`.")

        if hotp.verify(token, counter=counter):
            logger.info(f"Provided token is valid for user: {user}.")
            is_token_verified = True
        else:
            logger.warning(f"Provided token is expired or invalid for user: {user}.")
            is_token_verified = False

        return is_token_verified
