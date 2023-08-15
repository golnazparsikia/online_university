import random

from tqdm import tqdm

from django.utils.text import slugify

from painless.repository.generator import BaseDataGenerator
from elearning.warehouse.models import(
    Product,
    Bundle,
    ProductMedia,
    Question,
    QuestionHelp,
    Answer
)
from elearning.warehouse.helper.consts import DIFFICULTY, QUESTIONTYPES


class WarehouseDataGenerator(BaseDataGenerator):
    def get_random_difficulty(self):
        return random.choice(DIFFICULTY.labels)

    def get_random_question_type(self):
        return random.choice(QUESTIONTYPES.labels)

    def create_products(self, total, batch_size):
        division_objs = [
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
                priority=self.get_random_int(1, total)
            )
            for _ in tqdm(range(10)) if (words := self.get_random_text())
        ]
        divisions = Product.objects.bulk_create(
            division_objs,
            batch_size=batch_size
        )

        bootcamp_objs = [
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
                priority=self.get_random_int(1, total)
            )
            for _ in tqdm(range(range//20))
            if (words := self.get_random_text())
        ]
        bootcamps = Product.objects.bulk_create(
            bootcamp_objs,
            batch_size=batch_size
        )

        course_objs = [
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
                priority=self.get_random_int(1, total)
            )
            for _ in tqdm(range(range//5)) if (words := self.get_random_text())
        ]
        courses = Product.objects.bulk_create(
            course_objs,
            batch_size=batch_size
        )

        project_objs = [
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
                priority=self.get_random_int(1, total)
            )
            for _ in tqdm(range(range//20))
            if (words := self.get_random_text())
        ]
        projects = Product.objects.bulk_create(
            project_objs,
            batch_size=batch_size
        )

        lesson_objs = [
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
                priority=self.get_random_int(1, total)
            )
            for _ in tqdm(range(range//3)) if (words := self.get_random_text())
        ]
        lessons = Product.objects.bulk_create(
            lesson_objs,
            batch_size=batch_size
        )

        chapter_objs = [
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
                priority=self.get_random_int(1, total)
            )
            for _ in tqdm(range(range//3)) if (words := self.get_random_text())
        ]
        chapters = Product.objects.bulk_create(
            chapter_objs,
            batch_size=batch_size
        )

        practice_objs = [
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
                priority=self.get_random_int(1, total)
            )
            for _ in tqdm(range(range//4)) if (words := self.get_random_text())
        ]
        practices = Product.objects.bulk_create(
            practice_objs,
            batch_size=batch_size
        )

        return [divisions
                + bootcamps
                + courses
                + projects
                + lessons
                + chapters
                + practices
                ]

    def create_bundles(self, total, batch_size):
        bundle_objs = [
            Bundle(
                bootcamp =self.get_random_from_seq(
                    Product.objects.filter(scope="Bootcamp")
                ),
                course=self.get_random_from_seq(
                    Product.objects.filter(scope="Course")
                ),
            )
            for _ in tqdm(range(total))
        ]
        bundles = Bundle.objects.bulk_create(
            bundle_objs,
            batch_size=batch_size,
        )

        return bundles

    def create_product_medias(self, total, batch_size):
        product_media_objs = [
            ProductMedia(
                product=self.get_random_from_seq(Product.objects.all()),
                sku=self.get_random_sku(),
                alternate_text=self.get_random_words(5),
                width_field=self.get_random_int(50, 800),
                height_field=self.get_random_int(50, 800),
                duration=self.get_random_float(1, 60)
            )
            for _ in tqdm(range(total))
        ]
        product_medias = ProductMedia.objects.bulk_create(
            product_media_objs,
            batch_size=batch_size
        )

        return product_medias

    def create_questions(self, total, batch_size):
        question_objs = [
            Question(
                product=self.get_random_from_seq(Product.objects.all()),
                text=self.get_random_text(4),
                kind=self.get_random_question_type(),
                description=self.get_random_text(6)
            )
            for _ in tqdm(range(total))
        ]
        questions = Question.objects.bulk_create(
            question_objs,
            batch_size=batch_size,
        )

        return questions

    def create_question_helps(self, total, batch_size):
        question_help_objs = [
            QuestionHelp(
                question=self.get_random_from_seq(Question.objects.all()),
                plain_text=self.get_random_text(4),
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

    def create_answers(self, total, batch_size):
        #! set is correct and priority
        answer_objs = [
            Answer(
                question=self.get_random_from_seq(Question.objects.all()),
                text=self.get_random_text(1),
                order_placeholder=self.get_random_int(total),
            )
            for _ in tqdm(range(total))
        ]
        answers = Answer.objects.bulk_create(
            answer_objs,
            batch_size=batch_size,
        )

        return answers
