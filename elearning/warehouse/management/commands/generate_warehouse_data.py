from typing import Any, TextIO
from django.core.management.base import BaseCommand, CommandParser

from elearning.warehouse.models import Product, Question
from elearning.warehouse.helper.consts import QuestionType
from elearning.warehouse.repository.generator import WarehouseDataGenerator

DGL = WarehouseDataGenerator()


class Command(BaseCommand):
    """
    Django management command for generating fake data for the warehouse app.

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

    This command generates various types of fake data for the warehouse app,
    including divisions, bootcamps, courses, projects, lessons, chapters,
    practices, bundles, product medias, questions, question helps, and answers.

    """
    help = "Generate fake data for warehouse app."

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

        parser.add_argument(
            "--total-products",
            type=int,
            default=0,
            help="Specify numbers of total products generation.",
        )

        parser.add_argument(
            "--total-product-medias",
            type=int,
            default=0,
            help="Specify numbers of total product medias generation.",
        )

        parser.add_argument(
            "--total-questions",
            type=int,
            default=0,
            help="Specify numbers of total questions generation.",
        )

        parser.add_argument(
            "--total-question-helps",
            type=int,
            default=0,
            help="Specify numbers of total question helps generation.",
        )

        parser.add_argument(
            "--create-answers",
            type=bool,
            default=False,
            help="Specify numbers of total answers generation.",
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
        total_products = kwargs["total_products"]
        total_product_medias = kwargs["total_product_medias"]
        total_questions = kwargs["total_questions"]
        total_question_helps = kwargs["total_question_helps"]
        create_answers = kwargs["create_answers"]

        error_msg = "Problem with generating data. Check the logs"

        # Generation
        if total:
            try:
                divisions = DGL.create_divisions(total=10)
                self.show_success_msg(
                    "Divisions have successfully been created."
                )
                bootcamps = DGL.create_bootcamps(divisions, total=total//20)
                self.show_success_msg(
                    "Bootcamps have successfully been created."
                )
                courses = DGL.create_courses(total=total//5)
                self.show_success_msg(
                    "Courses have successfully been created."
                )
                projects = DGL.create_projects(bootcamps, total=total*3//20)
                self.show_success_msg(
                    "Projects have successfully been created."
                )
                lessons = DGL.create_lessons(courses, total=total//4)
                self.show_success_msg(
                    "Lessons have successfully been created."
                )
                chapters = DGL.create_chapters(lessons, total=total//4)
                self.show_success_msg(
                    "Chapters have successfully been created."
                )
                practices = DGL.create_chapters(chapters, total=total//10)
                self.show_success_msg(
                    "Practices have successfully been created.\n"
                )

                no_chapter_products = (divisions + bootcamps + courses + projects + lessons + practices)     # noqa: E501

                DGL.create_bundles(bootcamps, courses)
                self.show_success_msg(
                    "Bundles have successfully been created.\n"
                )

                DGL.create_chapter_medias(chapters, total=total//2)
                DGL.create_no_chapter_product_medias(
                    no_chapter_products,
                    total=total//2
                )
                self.show_success_msg(
                    "Product medias have successfully been created.\n"
                )

                questions = DGL.create_questions(chapters, total=total)
                self.show_success_msg(
                    "Questions have successfully been created.\n"
                )

                DGL.create_question_helps(questions, total=total)
                self.show_success_msg(
                    "Question helps have successfully been created.\n"
                )

                checkbox_questions = list(
                    Question.objects.filter(kind=QuestionType.CHECKBOX)
                )
                DGL.create_checkbox_answers(checkbox_questions)
                radio_questions = list(
                    Question.objects.filter(kind=QuestionType.RADIO)
                )
                DGL.create_radio_answers(radio_questions)
                placeholder_questions = list(
                    Question.objects.filter(kind=QuestionType.PLACEHOLDER)
                )
                DGL.create_placeholder_answers(
                    placeholder_questions
                )
                conditional_questions = list(
                    Question.objects.filter(kind=QuestionType.CONDITIONAL)
                )
                DGL.create_conditional_answers(
                    conditional_questions
                )
                code_questions = list(
                    Question.objects.filter(kind=QuestionType.CODE)
                )
                DGL.create_code_answers(code_questions)
                self.show_success_msg(
                    "Answers have successfully been created.\n"
                )

                msg = f"Almost {total} records are generated for each table" \
                f" in warehouse."
                self.show_success_msg(msg)
            except Exception:
                self.show_error_msg(error_msg)

        if total_products:
            try:
                divisions = DGL.create_divisions(total=10)
                self.show_success_msg(
                    "Divisions have successfully been created."
                )
                bootcamps = DGL.create_bootcamps(
                    divisions,
                    total=total_products//20
                )
                self.show_success_msg(
                    "Bootcamps have successfully been created."
                )
                courses = DGL.create_courses(total=total_products//5)
                self.show_success_msg(
                    "Courses have successfully been created."
                )
                projects = DGL.create_projects(
                    bootcamps,
                    total=total_products*3//20
                )
                self.show_success_msg(
                    "Projects have successfully been created."
                )
                lessons = DGL.create_lessons(courses, total=total_products//4)
                self.show_success_msg(
                    "Lessons have successfully been created."
                )
                chapters = DGL.create_chapters(lessons, total=total_products//4)
                self.show_success_msg(
                    "Chapters have successfully been created."
                )
                practices = DGL.create_chapters(
                    chapters,
                    total=total_products//10
                )
                self.show_success_msg(
                    "Practices have successfully been created."
                )

                DGL.create_bundles(bootcamps, courses)
                self.show_success_msg(
                    "Bundles have successfully been created.\n"
                )

                self.show_success_msg(
                    f"\nAlmost {total_products} Products are" "generated"
                )
            except Exception:
                self.show_error_msg(error_msg)

        if total_product_medias:
            try:
                chapters = list(Product.objects.filter(scope='Chapter'))
                no_chapter_products = list(
                    Product.objects.exclude(scope='Chapter')
                )

                DGL.create_chapter_medias(
                    chapters,
                    total=total_product_medias//2
                )
                DGL.create_no_chapter_product_medias(
                    no_chapter_products,
                    total=total_product_medias//2
                )
                self.show_success_msg(
                    f"{total_product_medias} Product medias have" \
                    f"successfully been created."
                )
            except IndexError:
                self.show_error_msg(
                    "You have to have some records in your product table."
                )
            except Exception:
                self.show_error_msg(error_msg)

        if total_questions:
            try:
                chapters = list(Product.objects.filter(scope="Chapter"))

                questions = DGL.create_questions(
                    chapters,
                    total=total_questions
                )
                self.show_success_msg(
                    f"{total_questions} Questions have successfully been "
                    "created."
                )
            except IndexError:
                self.show_error_msg(
                    "You have to have some records in your product table."
                )
            except Exception:
                self.show_error_msg(error_msg)

        if total_question_helps:
            try:
                questions = list(Question.objects.all())

                DGL.create_question_helps(
                    questions,
                    total=total_question_helps
                )
                self.show_success_msg(
                    f"{total_question_helps} Question helps have " \
                    f"successfully been created."
                )
            except IndexError:
                self.show_error_msg(
                    "You have to have some records in your question table."
                )
            except Exception:
                self.show_error_msg(error_msg)

        if create_answers:
            try:
                checkbox_questions = list(
                    Question.objects.filter(kind=QuestionType.CHECKBOX)
                )
                DGL.create_checkbox_answers(checkbox_questions)
                radio_questions = list(
                    Question.objects.filter(kind=QuestionType.RADIO)
                )
                DGL.create_radio_answers(radio_questions)
                placeholder_questions = list(
                    Question.objects.filter(kind=QuestionType.PLACEHOLDER)
                )
                DGL.create_placeholder_answers(
                    placeholder_questions
                )
                conditional_questions = list(
                    Question.objects.filter(kind=QuestionType.CONDITIONAL)
                )
                DGL.create_conditional_answers(
                    conditional_questions
                )
                code_questions = list(
                    Question.objects.filter(kind=QuestionType.CODE)
                )
                DGL.create_code_answers(code_questions)
                self.show_success_msg(
                    "Answers have successfully been created."
                )
            except IndexError:
                self.show_error_msg(
                    "You have to have some records in your question table."
                )
            except Exception:
                self.show_error_msg(error_msg)

    def show_success_msg(self, msg: str) -> TextIO:
        """Displays a success message on the console."""
        self.stdout.write(self.style.SUCCESS(msg))

    def show_error_msg(self, msg: str) -> TextIO:
        """Displays an error message on the console."""
        self.stdout.write(self.style.ERROR(msg))
