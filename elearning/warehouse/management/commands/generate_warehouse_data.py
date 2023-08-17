from typing import Any, TextIO
from django.core.management.base import BaseCommand, CommandParser

from elearning.warehouse.repository.generator import WarehouseDataGenerator

WGD = WarehouseDataGenerator()


class Command(BaseCommand):
    """
    A management command to generate fake data for the warehouse app.

    This command allows the user to generate fake data for various tables in
    the warehouse app such as products, bundles, product media, questions,
    question helps, and answers. The amount of fake data generated can be
    controlled by specifying the total number of records to be generated.

    Usage:
    python manage.py generate_warehouse_data --total <total_records>
    """
    help = "Generate fake data for warehouse app."

    def add_arguments(self, parser: CommandParser) -> None:
        """Adds a command-line argument to specify the total number of data
        generations. The default value is 100.
        """
        parser.add_argument(
            "--total",
            type=int,
            default=100,
            help="Specify numbers of total generation."
        )

    def handle(self, *args: Any, **kwargs: Any) -> str | None:
        """
        Handles the main logic of generating fake data for warehouse app
        tables. It creates fake data for products, bundles, product media,
        questions, question helps, and answers. The specified total number of
        records are generated for each table. If an exception occurs during the
        generation process, an error message is displayed.
        """
        total: int = kwargs["total"]
        try:
            WGD.create_products(total, batch_size=1_000_000)
            WGD.create_bundles(total, batch_size=1_000_000)
            WGD.create_product_medias(total, batch_size=1_000_000)
            WGD.create_questions(total, batch_size=1_000_000)
            WGD.create_question_helps(total, batch_size=1_000_000)
            WGD.create_answers(total, batch_size=1_000_000)

            msg = f"{total} records are generated for each table in warehouse."
            self.show_success_msg(msg)
        except Exception as error:
            msg = "Problem with generating data. Check the logs"
            self.show_error_msg(msg)

    def show_success_msg(self, msg: str) -> TextIO:
        """Displays a success message on the console."""
        self.stdout.write(self.style.SUCCESS(msg))

    def show_error_msg(self, msg: str) -> TextIO:
        """Displays an error message on the console."""
        self.stdout.write(self.style.ERROR(msg))
