from painless.helper.typing import (
    Byte,
    MegaByte,
    Day,
    Second
)


class UnitConvertor:

    @staticmethod
    def convert_byte_to_megabyte(value: Byte) -> MegaByte:
        return value * 1e-6

    @staticmethod
    def convert_megabyte_to_byte(value: MegaByte) -> Byte:
        return value * 1_000_000

    @staticmethod
    def convert_days_to_seconds(value: Day) -> Second:
        return 60 * 60 * 24 * value
