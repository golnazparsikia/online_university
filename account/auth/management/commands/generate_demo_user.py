from typing import Any, TextIO
from django.core.management.base import BaseCommand, CommandParser

from account.auth.repository.generator import UserDataGenerator
from account.auth.models import User
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
            "--demo",
            type=int,
            default=1,
            help="Specify numbers of demo generation."
        )
    
    def handle(self, *args, **kwargs):
        # Argument
        demo = kwargs["demo"]

        # Constants
        phone_number = '989212922187'
        password = '@DMT_group'

        # Generation
        try:
            # Check if the demo user already exists
            demo_user, created = User.objects.get_or_create(phone_number=phone_number)
            if created:
                # Set the password for the demo user
                demo_user.set_password(password)
                demo_user.save()

                self.show_success_msg(f"Demo user has successfully been created\n\t📞 phone number: {phone_number}\n\t🔑 password: {password}")

                # You can now generate additional demo users if needed
                for _ in range(demo - 1):
                    User.objects.create(phone_number=phone_number, password=password)

                msg = f"{demo} demo users have been generated."
                self.show_success_msg(msg)
            else:
                self.show_success_msg(f"Demo user with phone number {phone_number} already exists.")

        except Exception as e:
            self.show_error_msg(f"Problem with generating data: {str(e)}")
            
    def show_success_msg(self, msg: str) -> TextIO:
        """Displays a success message on the console."""
        self.stdout.write(self.style.SUCCESS(msg))

    def show_error_msg(self, msg: str) -> TextIO:
        """Displays an error message on the console."""
        self.stdout.write(self.style.ERROR(msg))
