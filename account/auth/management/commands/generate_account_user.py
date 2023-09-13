from typing import Any, TextIO
from django.core.management.base import BaseCommand, CommandParser

from account.auth.repository.generator import UserDataGenerator

DGL = UserDataGenerator()


class Command(BaseCommand):
    """
    Django management command for generating fake data for the auth app.

    Usage:
        python manage.py generate_fake_data [options]

    Options:
        --total TOTAL                   Specify the total number of records to
                                        generate.
        --total-products TOTAL          Specify the total number of product
                                        records to generate.
        --total-product-medias TOTAL    Specify the total number of product
                                        media records to generate.
        --total-questions TOTAL         Specify the total number of question
                                        records to generate.
        --total-question-helps TOTAL    Specify the total number of question
                                        help records to generate.
        --create-answers BOOL           Specify whether to generate answers for
                                        questions.

    This command generates various types of fake data for the auth app,
    including divisions, bootcamps, courses, projects, lessons, chapters,
    practices, bundles, product medias, questions, question helps, and answers.

    """
    help = "Generate fake data for auth app."

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add command line arguments to the command.

        Args:
            parser (CommandParser): The command line argument parser.

        Returns:
            None
        """
        parser.add_argument(
            "--total",
            type=int,
            default=0,
            help="Specify numbers of total generation."
        )

    def handle(self, *args: Any, **kwargs: Any) -> str | TextIO | None:
        """
        Handle the command execution.

        Args:
            *args (Any): Additional arguments.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Union[str, TextIO, None]: A string, text output, or None.
        """
        # Arguments
        total = kwargs["total"]

        error_msg = "Problem with generating data. Check the logs"

        # Generation
        if total:
            DGL.create_user(total)
            self.show_success_msg(
                "user have successfully been created."
            )

            msg = f"Almost {total} records are generated for each table in"
            "auth."
            self.show_success_msg(msg)
        # except Exception:
        #     self.show_error_msg(error_msg)

    def show_success_msg(self, msg: str) -> TextIO:
        """Displays a success message on the console."""
        self.stdout.write(self.style.SUCCESS(msg))

    def show_error_msg(self, msg: str) -> TextIO:
        """Displays an error message on the console."""
        self.stdout.write(self.style.ERROR(msg))
