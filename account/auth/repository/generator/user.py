import os
import random

from typing import List
from itertools import count
from tqdm import tqdm
from painless.repository.generator.base import BaseDataGenerator
from account.auth.models import User
from account.auth.helper.type_hints import Users


class UserDataGenerator(BaseDataGenerator):
    """
    A class responsible for generating fake data for user table.
    Inherits from BaseDataGenerator for data generation utilities.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the WarehouseDataGenerator.

        Attributes:
            priority_counter (itertools.count): A counter that generates
            sequential priority values for generated data.
        """
        super().__init__(*args, **kwargs)

    def create_user(
        self,
        total: int = 5,
        batch_size: int = 10,
        disable_progress_bar: bool = False
    ) -> List[Users]:
        """Create Product objects with user scope.

        Args:
            total (int): Total number of users to create.
            batch_size (int): Number of users to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[user]: List of created Product objects.
        """
        user_objs = [
            User(
                username=phone_number,
                email=f"{words}@gmail.com",
                phone_number=phone_number,
                first_name=self.get_random_words(1),
                last_name=self.get_random_words(1),
                secret_key=words,
                is_active=self.get_random_bool(),
                is_staff=self.get_random_bool(),
                is_superuser=False,
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'user {self.get_random_words(2)}') and (phone_number  := self.get_random_number())
        ]
        users = User.objects.bulk_create(
            user_objs,
            batch_size=batch_size
        )
        return users
