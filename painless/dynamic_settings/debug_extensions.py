from kernel.settings import config
from painless.dynamic_settings.enums import EnvMode


class DynamicDebugExtensions:
    """
    A class with a dynamic method to manage the enabling of extensions
    based on debug mode, environment mode and is_extension_enabled
    """

    def __init__(self) -> None:
        """
        Initializes the DynamicDebugExtensions object by 
        reading the ENABLE_DEBUG_MODE and ENV_MODE from settings via config
        """

        self.is_debug_mode: bool = config.get_value(
            'mode',
            'ENABLE_DEBUG_MODE',
            default=False
        )
        self.env_mode: str = config.get_value(
            'mode',
            'ENV_MODE'
        )

    def should_extensions_enable(self, is_extension_enabled: bool) -> bool:
        """
        Determine whether extensions should be enabled based 
        on the is_extension_enabled flag from settings.toml, 
        debug mode, and environment mode.

        Parameters
        ----------
        is_extension_enabled : bool
            A flag indicating whether the extension 
            is set to enabled in settings.

        Returns
        -------
        bool
            True if the extension should be enabled, False otherwise.
        """
        is_dev_debug_mode = all(
            (self.env_mode == EnvMode.DEVELOPMENT, self.is_debug_mode)
        )
        return any((is_extension_enabled, is_dev_debug_mode))
