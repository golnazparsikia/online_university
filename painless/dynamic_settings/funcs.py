from typing import Optional
from .exceptions import SettingsNotAllowed
from .enums import EnvMode
from kernel.settings import config


def verify_production_mode(production_mode_enabled: bool, stage_mode_enabled: bool, debug_mode_enabled: bool):
    """
    Checks the values of production and stage mode settings and sets the DEBUG value accordingly.
    :param production_mode_enabled: Whether production mode is enabled or not
    :param stage_mode_enabled: Whether stage mode is enabled or not
    :param debug_mode_enabled: Whether debug mode is enabled or not in stage mode
    :return: The DEBUG value
    """
    # Check mode values and set DEBUG accordingly
    if production_mode_enabled and not stage_mode_enabled:
        DEBUG = False
    elif production_mode_enabled and stage_mode_enabled:
        debug_mode_enabled = config.get_value('mode', 'DEBUG_MODE_ENABLED')

        if debug_mode_enabled:
            DEBUG = True
        else:
            raise SettingsNotAllowed(
                f"DEBUG_MODE_ENABLED cannot be enabled with the value: `{debug_mode_enabled}`."
                "This setting is only allowed to be set to True in stage environments."
            )
    else:
        raise SettingsNotAllowed(
            f"PRODUCTION_MODE_ENABLED cannot be enabled with the value: `{production_mode_enabled}`."
            "This setting is only allowed to be set to True in production environments."
        )
    return DEBUG

def set_session_cookie_domain(mode: EnvMode, domain: Optional[str]=None) -> Optional[str]:
    """
    Determines the appropriate `SESSION_COOKIE_DOMAIN` value based on the current 
    environment mode.
    
    In development mode, `SESSION_COOKIE_DOMAIN` is set to None, allowing for seamless 
    local development. e.g. It support both localhost and 127.0.0.1.

    In production mode, `SESSION_COOKIE_DOMAIN` is set to a specific value retrieved
    from the configuration system, enhancing security and privacy of user sessions.

    Args:
        mode (str): The current environment mode, e.g., 'development' or 'production'.
        config (object, optional): A configuration object providing access to 
                                    configuration settings.
    
    Returns:
        str or None: The value to be used as `SESSION_COOKIE_DOMAIN`.
    """
    EnvMode.validate(mode, raise_exception=True)
    session_cookie_domain = None if mode == EnvMode.DEVELOPMENT else domain

    return session_cookie_domain
