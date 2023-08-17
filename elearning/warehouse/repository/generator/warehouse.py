import random
from typing import List

from tqdm import tqdm

from django.utils.text import slugify

from painless.repository.generator import BaseDataGenerator
from elearning.warehouse.models import (
    Product,
    Bundle,
    ProductMedia,
    Question,
    QuestionHelp,
    Answer,
)
from elearning.warehouse.helper.consts import (
    Difficulty,
    QuestionType,
    QuestionTypeAnswersCount as QTAC
)
from elearning.warehouse.helper.type_hints import (
    ProductQuerySet,
    BundleQuerySet,
    ProductMediaQuerySet,
    QuestionQuerySet,
    QuestionHelpQuerySet,
    AnswerQuerySet,
)
from elearning.warehouse.helper.exceptions import QuestionTypeError


class WarehouseDataGenerator(BaseDataGenerator):
    """
    A class responsible for generating fake data for warehouse tables.
    Inherits from BaseDataGenerator for data generation utilities.
    """
    def get_random_difficulty(self) -> Difficulty:
        """Return a randomly chosen difficulty level."""
        return random.choice(Difficulty.labels)

    def get_random_question_type(self) -> QuestionType:
        """Return a randomly chosen question type."""
        return random.choice(QuestionType.labels)

    def get_total_answer(self, question_obj: Question) -> int:
        """Return the total number of answers based on the question's type."""
        question_kind = question_obj.kind
        answers_quantity = getattr(QTAC, question_kind.upper()).value

        return answers_quantity

    def get_valid_is_correct(
        self, question: Question
    ) -> bool:
        """
        Determine whether an answer is correct or not based on the question
        type. It ensures the logic of handling the truthiness of each specific
        question's answers.

        Args:
            question_obj (Question): The question object.

        Raise:
            QuestionTypeError if there's a type error.

        Returns:
            bool | QuestionTypeError: Boolean indicating correctness or
        """
        question_kind = question.kind

        if question_kind == QuestionType.CHECKBOX:
            is_correct = self.get_random_bool()

        elif question_kind in (QuestionType.RADIO, QuestionType.CONDITIONAL):
            if not question.answers.filter(is_correct=True).exists():
                is_correct = True
            else:
                is_correct = False

        elif question_kind in (QuestionType.PLACEHOLDER, QuestionType.CODE):
            is_correct = True

        else:
            QuestionTypeError(
                f"QuestionType from {question} doesn't exists."
            )

        return is_correct

    def create_products(self,
                        total: int,
                        batch_size: int,
                        disable_progress_bar: bool=False) -> ProductQuerySet:
        """
        Generate and create fake product data.

        Each scope is initiated and created separately, so it would be possible
        to handle parent fields for each scope.
        Args:
            total (int): Total number of products to generate.
            batch_size (int): Batch size for bulk creation.

        Returns:
            ProductQuerySet: List of all generated Product objects.
        """
        division_objs: List[Product] = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope="Division",
                difficulty=self.get_random_difficulty(),
                parent=None,
                is_buyable=False,
                description=self.get_random_text(6),
                experience=self.get_random_float(1, 5),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(10), disable=disable_progress_bar)
            if (words := self.get_random_words(3))
        ]
        divisions = Product.objects.bulk_create(
            division_objs,
            batch_size=batch_size
        )

        bootcamp_objs: List[Product] = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope="Bootcamp",
                parent=self.get_random_from_seq(divisions),
                difficulty=self.get_random_difficulty(),
                is_buyable=self.get_random_bool(),
                description=self.get_random_text(6),
                experience=self.get_random_float(1, 5),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total // 20), disable=disable_progress_bar)
            if (words := self.get_random_words(3))
        ]
        bootcamps = Product.objects.bulk_create(
            bootcamp_objs,
            batch_size=batch_size
        )

        course_objs: List[Product] = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope="Course",
                difficulty=self.get_random_difficulty(),
                parent=None,
                is_buyable=True,
                description=self.get_random_text(6),
                experience=self.get_random_float(1, 5),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total // 5), disable=disable_progress_bar)
            if (words := self.get_random_words(3))
        ]
        courses = Product.objects.bulk_create(
            course_objs,
            batch_size=batch_size
        )

        project_objs: List[Product] = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope="Project",
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(bootcamps),
                is_buyable=False,
                description=self.get_random_text(6),
                experience=self.get_random_float(1, 5),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total // 20), disable=disable_progress_bar)
            if (words := self.get_random_words(3))
        ]
        projects = Product.objects.bulk_create(
            project_objs,
            batch_size=batch_size
        )

        lesson_objs: List[Product] = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope="Lesson",
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(courses),
                is_buyable=False,
                description=self.get_random_text(6),
                experience=self.get_random_float(1, 5),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total // 3), disable=disable_progress_bar)
            if (words := self.get_random_words(3))
        ]
        lessons = Product.objects.bulk_create(
            lesson_objs,
            batch_size=batch_size
        )

        chapter_objs: List[Product] = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope="Chapter",
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(lessons),
                is_buyable=self.get_random_bool(),
                description=self.get_random_text(6),
                experience=self.get_random_float(1, 5),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total // 3), disable=disable_progress_bar)
            if (words := self.get_random_words(3))
        ]
        chapters = Product.objects.bulk_create(
            chapter_objs,
            batch_size=batch_size
        )

        practice_objs: List[Product] = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope="Practice",
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(lessons),
                is_buyable=self.get_random_bool(),
                description=self.get_random_text(6),
                experience=self.get_random_float(1, 5),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total // 4), disable=disable_progress_bar)
            if (words := self.get_random_words(3))
        ]
        practices = Product.objects.bulk_create(
            practice_objs,
            batch_size=batch_size
        )

        return [
            divisions + bootcamps + courses + projects + lessons + chapters
            + practices
        ]

    def create_bundles(self, total: int, batch_size: int) -> BundleQuerySet:
        """
        Generate and create fake bundle data.

        The "bootcamp" and "course" fields are received randomly from products
        with the "Bootcamp" and "Course" scopes, respectively.

        Args:
            total (int): Total number of bundles to generate.
            batch_size (int): Batch size for bulk creation.

        Returns:
            BundleQuerySet: List of generated Bundle objects.
        """
        bootcamps = Product.objects.filter(scope="Bootcamp")
        courses = Product.objects.filter(scope="Course")

        bundle_objs: List[Bundle] = [
            Bundle(
                bootcamp=self.get_random_from_seq(bootcamps),
                course=self.get_random_from_seq(courses),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
        ]
        bundles = Bundle.objects.bulk_create(
            bundle_objs,
            batch_size=batch_size,
        )

        return bundles

    def create_product_medias(
        self, total: int, batch_size: int
    ) -> ProductMediaQuerySet:
        """
        Generate and create fake product media data.

        Product foreign keys are randomly retrieved from a queryset that
        contains records from the product table.

        Args:
            total (int): Total number of product media items to generate.
            batch_size (int): Batch size for bulk creation.

        Returns:
            ProductMediaQuerySet: List of generated ProductMedia objects.
        """
        products = Product.objects.all()

        product_media_objs: List[ProductMedia] = [
            ProductMedia(
                product=self.get_random_from_seq(products),
                sku=self.get_random_sku(),
                alternate_text=self.get_random_words(3),
                width_field=self.get_random_int(50, 800),
                height_field=self.get_random_int(50, 800),
                duration=self.get_random_float(1, 60),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
        ]
        product_medias = ProductMedia.objects.bulk_create(
            product_media_objs, batch_size=batch_size
        )

        return product_medias

    def create_questions(
        self,
        total: int,
        batch_size: int,
        disable_progress_bar: bool=False
    ) -> QuestionQuerySet:
        """
        Generate and create fake question data.

        Product foreign keys are randomly retrieved from a queryset that
        contains records from the product table.

        Args:
            total (int): Total number of questions to generate.
            batch_size (int): Batch size for bulk creation.

        Returns:
            QuestionQuerySet: List of generated Question objects.
        """
        products = Product.objects.all()

        question_objs: List[Question] = [
            Question(
                product=self.get_random_from_seq(products),
                text=self.get_random_words(4),
                kind=self.get_random_question_type(),
                description=self.get_random_text(6),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
        ]
        questions = Question.objects.bulk_create(
            question_objs,
            batch_size=batch_size,
        )

        return questions

    def create_question_helps(
        self,
        total: int,
        batch_size: int,
        disable_progress_bar: bool=False
    ) -> QuestionHelpQuerySet:
        """
        Generate and create fake question help data.

        Question foreign keys are randomly retrieved from a queryset that
        contains records from the query table.

        Args:
            total (int): Total number of question helps to generate.
            batch_size (int): Batch size for bulk creation.

        Returns:
            QuestionHelpQuerySet: List of generated QuestionHelp objects.
        """
        questions = Question.objects.all()

        question_help_objs: List[QuestionHelp] = [
            QuestionHelp(
                question=self.get_random_from_seq(questions),
                plain_text=self.get_random_words(4),
                alternate_text=self.get_random_words(5),
                width_field=self.get_random_int(50, 800),
                height_field=self.get_random_int(50, 800),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
        ]
        question_helps = QuestionHelp.objects.bulk_create(
            question_help_objs,
            batch_size=batch_size,
        )

        return question_helps

    def create_answers(self, total: int, batch_size: int) -> AnswerQuerySet:
        """
        Generate and create fake answer data.

        Question foreign keys are randomly retrieved from a queryset that
        contains records from the query table.

        Args:
            total (int): Total number of answers to generate.
            batch_size (int): Batch size for bulk creation.

        Returns:
            AnswerQuerySet: List of generated Answer objects.
        """
        questions = Question.objects.all()

        answer_objs: List[Answer] = list()
        priority_counter = 0

        # Iterate on all Question objects.
        for question_obj in tqdm(questions, disable=disable_progress_bar):
            # How many answers should a question has.
            total_answers = self.get_total_answer(question_obj)
            for _ in range(total_answers):
                answer = Answer(
                    question=question_obj,
                    text=self.get_random_words(3),
                    order_placeholder=self.get_random_int(1, total),
                    priority=priority_counter,
                    is_correct=self.get_valid_is_correct(question_obj),
                )
                answer_objs.append(answer)

                priority_counter += 1

        answers = Answer.objects.bulk_create(
            answer_objs,
            batch_size=batch_size,
        )

        return answers
