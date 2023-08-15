import random
import uuid

from mimesis.locales import Locale
from mimesis import (
    Generic,
    Text,
    Datetime,
    File
)

class BaseDataGenerator:
    def __init__(self, locale="en"):
        self.generic = Generic(getattr(Locale, locale.upper()))
        self.text = Text(getattr(Locale, locale.upper()))
        self.date_time = Datetime(getattr(Locale, locale.upper()))
        self.file = File()

    def get_random_from_seq(self, seq):
        return random.choice(seq=seq)

    def get_random_sku(self):
        return str(uuid.uuid4())

    def get_random_words(self, qty=2):
        return " ".join(self.text.words(quantity=qty))

    def get_random_text(self, qty=2):
        return self.text.text(quantity=qty)

    def get_random_float(self, start, end):
        return round(random.uniform(start, end), 2)

    def get_random_int(self, start, end):
        return random.randint(start, end)

    def get_random_bool(self):
        return random.choice((True, False))

    def get_random_datetime(self):
        return self.date_time.datetime()

    def get_random_file(self):
        return self.file.file_name()
