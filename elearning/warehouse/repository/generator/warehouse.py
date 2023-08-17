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
    DIFFICULTY,
    QUESTIONTYPES,
    QUESTIONTYPEANSWERSCOUNT as QTAC,
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
    def get_random_difficulty(self) -> str:
        return random.choice(DIFFICULTY.labels)

    def get_random_question_type(self) -> str:
        return random.choice(QUESTIONTYPES.labels)

    def get_total_answer(self, question_obj: Question) -> int:
        question_kind = question_obj.kind
        answers_quantity = getattr(QTAC, question_kind.upper()).value

        return answers_quantity

    def get_valid_is_correct(
        self, question_obj: Question
    ) -> bool | QuestionTypeError:
        question_kind = question_obj.kind

        if question_kind == "Checkbox":
            is_correct = self.get_random_bool()

        elif question_kind in ("Radio", "Conditional"):
            if not question_obj.answers.filter(is_correct=True).exists():
                is_correct = True
            else:
                is_correct = False

        elif question_kind in ("Placeholder", "Code"):
            is_correct = True

        else:
            QuestionTypeError(
                f"QuestionType from {question_obj} doesn't exists."
            )

        return is_correct

    def create_products(self, total: int, batch_size: int) -> ProductQuerySet:
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
            for _ in tqdm(range(10))
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
            for _ in tqdm(range(total // 20))
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
            for _ in tqdm(range(total // 5))
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
            for _ in tqdm(range(total // 20))
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
            for _ in tqdm(range(total // 3))
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
            for _ in tqdm(range(total // 3))
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
            for _ in tqdm(range(total // 4))
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
        bootcamps = Product.objects.filter(scope="Bootcamp")
        courses = Product.objects.filter(scope="Course")

        bundle_objs: List[Bundle] = [
            Bundle(
                bootcamp=self.get_random_from_seq(bootcamps),
                course=self.get_random_from_seq(courses),
            )
            for _ in tqdm(range(total))
        ]
        bundles = Bundle.objects.bulk_create(
            bundle_objs,
            batch_size=batch_size,
        )

        return bundles

    def create_product_medias(
        self, total: int, batch_size: int
    ) -> ProductMediaQuerySet:
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
            for _ in tqdm(range(total))
        ]
        product_medias = ProductMedia.objects.bulk_create(
            product_media_objs, batch_size=batch_size
        )

        return product_medias

    def create_questions(
        self, total: int, batch_size: int
    ) -> QuestionQuerySet:
        products = Product.objects.all()

        question_objs: List[Question] = [
            Question(
                product=self.get_random_from_seq(products),
                text=self.get_random_words(4),
                kind=self.get_random_question_type(),
                description=self.get_random_text(6),
            )
            for _ in tqdm(range(total))
        ]
        questions = Question.objects.bulk_create(
            question_objs,
            batch_size=batch_size,
        )

        return questions

    def create_question_helps(
        self, total: int, batch_size: int
    ) -> QuestionHelpQuerySet:
        questions = Question.objects.all()

        question_help_objs: List[QuestionHelp] = [
            QuestionHelp(
                question=self.get_random_from_seq(questions),
                plain_text=self.get_random_words(4),
                alternate_text=self.get_random_words(5),
                width_field=self.get_random_int(50, 800),
                height_field=self.get_random_int(50, 800),
            )
            for _ in tqdm(range(total))
        ]
        question_helps = QuestionHelp.objects.bulk_create(
            question_help_objs,
            batch_size=batch_size,
        )

        return question_helps

    def create_answers(self, total: int, batch_size: int) -> AnswerQuerySet:
        questions = Question.objects.all()

        answer_objs: List[Answer] = list()
        priority_counter = 0

        # Iterate on all Question objects.
        for question_obj in tqdm(questions):
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
