import random
import uuid
from typing import Any, Sequence
from datetime import datetime

from mimesis.locales import Locale
from mimesis import Generic, Text, Datetime, File


class BaseDataGenerator:
    """
    A base class for generating various types of fake data.

    Args:
        locale (str, optional): Locale code for generating data.
            Defaults to "en".

    Attributes:
        generic (Generic): Instance of Generic for generating generic data.
        text (Text): Instance of Text for generating text data.
        date_time (Datetime): Instance Datetime for generating datetime data.
        file (File): Instance of File for generating file-related data.
    """
    def __init__(self, locale: str = "en") -> None:
        """
        Initialize the BaseDataGenerator instance with the given locale.

        Args:
            locale (str, optional): Locale code for generating data.
                Defaults to "en".
        """
        self.generic = Generic(getattr(Locale, locale.upper()))
        self.text = Text(getattr(Locale, locale.upper()))
        self.date_time = Datetime(getattr(Locale, locale.upper()))
        self.file = File()

    def get_random_from_seq(self, seq: Sequence) -> Any:
        """
        Return a random element from the given sequence.

        Args:
            seq (Sequence): The sequence from which to select a random element.

        Returns:
            Any: A randomly selected element from the sequence.
        """
        return random.choice(seq=seq)

    def get_random_sku(self) -> str:
        """
        Generate and return a random SKU (Stock Keeping Unit) as a string.

        Returns:
            str: A randomly generated SKU.
        """
        return str(uuid.uuid4())

    def get_random_words(self, qty: int = 2) -> str:
        """
        Generate and return a string containing random words.

        Args:
            qty (int, optional): The number of words to generate.
                Defaults to 2.

        Returns:
            str: A string containing randomly generated words.
        """
        return " ".join(self.text.words(quantity=qty))

    def get_random_text(self, qty: int = 2) -> str:
        """
        Generate and return random text.

        Args:
            qty (int, optional): The number of text segments to generate.
                Defaults to 2.

        Returns:
            str: Randomly generated text.
        """
        return self.text.text(quantity=qty)

    def get_random_float(self, start: float, end: float) -> float:
        """
        Generate and return a random floating-point number within the specified
        range.

        Args:
            start (float): The lower bound of the range.
            end (float): The upper bound of the range.

        Returns:
            float: A random floating-point number.
        """
        return round(random.uniform(start, end), 2)

    def get_random_int(self, start: int, end: int) -> int:
        """
        Generate and return a random integer within the specified range.

        Args:
            start (int): The lower bound of the range.
            end (int): The upper bound of the range.

        Returns:
            int: A random integer.
        """
        return random.randint(start, end)

    def get_random_bool(self) -> bool:
        """
        Generate and return a random boolean value (True or False).

        Returns:
            bool: A randomly generated boolean value.
        """
        return random.choice((True, False))

    def get_random_datetime(self) -> datetime:
        """
        Generate and return a random datetime object.

        Returns:
            datetime: A randomly generated datetime object.
        """
        return self.date_time.datetime()

    def get_random_file(self) -> str:
        """
        Generate and return a random file name.

        Returns:
            str: A randomly generated file name.
        """
        return self.file.file_name()

    def get_random_number(self) -> int:
        """
        Generate and return a random 12-digit number that starts with '989'.

        Returns:
            int: A random 12-digit integer.
        """
        prefix = '989'
        random_digits = [random.randint(0, 9) for _ in range(9)]  # Generate 9 random digits.
        random_number = int(prefix + ''.join(map(str, random_digits)))  # Concatenate the prefix and random digits.
        return random_number
