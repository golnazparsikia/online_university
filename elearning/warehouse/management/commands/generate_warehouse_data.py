from typing import Any, TextIO
from django.core.management.base import BaseCommand, CommandParser

from elearning.warehouse.repository.generator import WarehouseDataGenerator

WGD = WarehouseDataGenerator()


class Command(BaseCommand):
    help = "Generate fake data for warehouse app."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--total",
            type=int,
            default=100,
            help="Specify numbers of total generation."
        )

    def handle(self, *args: Any, **kwargs: Any) -> str | None:
        total: int = kwargs["total"]

        WGD.create_products(total, batch_size=1_000_000)
        WGD.create_bundles(total, batch_size=1_000_000)
        WGD.create_product_medias(total, batch_size=1_000_000)
        WGD.create_questions(total, batch_size=1_000_000)
        WGD.create_question_helps(total, batch_size=1_000_000)
        WGD.create_answers(total, batch_size=1_000_000)

        msg = f"{total} records are generated for each table in warehouse."
        self.show_success_msg(msg)

    def show_success_msg(self, msg: str) -> TextIO:
        self.stdout.write(self.style.SUCCESS(msg))

    def show_error_msg(self, msg: str) -> TextIO:
        self.stdout.write(self.style.ERROR(msg))
