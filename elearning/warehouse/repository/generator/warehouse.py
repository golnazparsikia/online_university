import os
import random

from typing import List
from itertools import count
from tqdm import tqdm

from django.utils.text import slugify
from kernel.settings import BASE_DIR

from django.core.files.uploadedfile import SimpleUploadedFile

from painless.repository.generator.base import BaseDataGenerator
from elearning.warehouse.models import (
    Product,
    Bundle,
    ProductMedia,
    Question,
    QuestionHelp,
    Answer,
)
from elearning.warehouse.helper.consts import (
    Scope,
    Difficulty,
    QuestionType
)
from elearning.warehouse.helper.type_hints import (
    Division,
    Bootcamp,
    Course,
    Project,
    Lesson,
    Chapter,
    Practice,
    CheckboxQuestion,
    RadioQuestion,
    PlaceholderQuestion,
    ConditionalQuestion,
    CodeQuestion,
)


class WarehouseDataGenerator(BaseDataGenerator):
    """
    A class responsible for generating fake data for warehouse tables.
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
        self.priority_counter = count(start=1)

    # ------------- Random and handler methods -------------
    def get_random_difficulty(self) -> Difficulty:
        """
        Return a randomly chosen difficulty level.

        Returns:
            Difficulty: A randomly selected difficulty level.
        """
        return random.choice(Difficulty.labels)

    def get_random_question_type(self) -> QuestionType:
        """
        Return a randomly chosen question type.

        Returns:
            QuestionType: A randomly selected question type.
        """
        return random.choice(QuestionType.labels)

    def set_is_correct(self, number: int) -> bool:
        """
        This method is used to handle the "is_correct" field for radio answer
        table. The method evaluates whether the provided number is divisible by
        4. If so, it returns True, implying that the corresponding radio answer
        should be marked as correct. Otherwise, it returns False.

        Parameters:
            number (int): The input number to evaluate.

        Returns:
            bool: True if the number is divisible by 4, otherwise False.
        """
        if number % 4 == 0:
            is_correct = True
        else:
            is_correct = False

        return is_correct

    def split_chapters(
        self, chapters: List[Chapter], is_question: bool
    ) -> List[Chapter]:
        if is_question:
            chapters = chapters[0::2]
        else:
            chapters = chapters[1::2]

        return chapters

    # ------------- Object creation methods -------------

    # - products creation -
    def create_divisions(
        self,
        total: int = 10,
        batch_size: int = 10,
        disable_progress_bar: bool = False
    ) -> List[Division]:
        """Create Product objects with Division scope.

        Args:
            total (int): Total number of divisions to create.
            batch_size (int): Number of divisions to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Division]: List of created Product objects.
        """
        division_objs = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope=Scope.DIVISION,
                difficulty=self.get_random_difficulty(),
                parent=None,
                is_buyable=False,
                description=self.get_random_text(6),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'division {self.get_random_words(3)}')
        ]
        divisions = Product.objects.bulk_create(
            division_objs,
            batch_size=batch_size
        )

        return divisions

    def create_bootcamps(
        self,
        divisions: List[Division],
        total: int = 40,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Bootcamp]:
        """Create Product objects with Bootcamp scope.

        Args:
            divisions (List[Division]): List of Product objects with Division
            scope to associate with Bootcamps.
            total (int): Total number of bootcamps to create.
            batch_size (int): Number of bootcamps to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Bootcamp]: List of created Product objects.
        """
        bootcamp_objs = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope=Scope.BOOTCAMP,
                parent=self.get_random_from_seq(divisions),
                difficulty=self.get_random_difficulty(),
                is_buyable=False,
                description=self.get_random_text(6),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'bootcamp {self.get_random_words(3)}')
        ]
        bootcamps = Product.objects.bulk_create(
            bootcamp_objs,
            batch_size=batch_size
        )

        return bootcamps

    def create_courses(
        self,
        total: int = 5_000,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Course]:
        """Create Product objects with Course scope.

        Args:
            total (int): Total number of courses to create.
            batch_size (int): Number of courses to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Course]: List of created Product objects.
        """
        course_objs = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope=Scope.COURSE,
                difficulty=self.get_random_difficulty(),
                parent=None,
                is_buyable=True,
                description=self.get_random_text(6),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'course {self.get_random_words(3)}')
        ]
        courses = Product.objects.bulk_create(
            course_objs,
            batch_size=batch_size
        )

        return courses

    def create_projects(
        self,
        bootcamps: List[Bootcamp],
        total: int = 120,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Project]:
        """Create Product objects with Project scope.

        Args:
            bootcamps (List[Bootcamp]): List of Product objects with Bootcamp
            scope to associate with Projects.
            total (int): Total number of projects to create.
            batch_size (int): Number of projects to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Project]: List of created Product objects.
        """
        project_objs = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope=Scope.PROJECT,
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(bootcamps),
                is_buyable=False,
                description=self.get_random_text(6),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'project {self.get_random_words(3)}')
        ]
        projects = Product.objects.bulk_create(
            project_objs,
            batch_size=batch_size
        )

        return projects

    def create_lessons(
        self,
        courses: List[Course],
        total: int = 1_000,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Lesson]:
        """Create Product objects with Lesson scope.

        Args:
            courses (List[Course]): List of Product objects with Course scope
            to associate with Lessons.
            total (int): Total number of lessons to create.
            batch_size (int): Number of lessons to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Lesson]: List of created Product objects.
        """
        lesson_objs = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope=Scope.LESSON,
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(courses),
                is_buyable=False,
                description=self.get_random_text(6),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'lesson {self.get_random_words(3)}')
        ]
        lessons = Product.objects.bulk_create(
            lesson_objs,
            batch_size=batch_size
        )

        return lessons

    def create_chapters(
        self,
        lessons: List[Lesson],
        total: int = 1_000,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Chapter]:
        """Create Product objects with Chapter scope.

        Args:
            lessons (List[Lesson]): List of Product objects with Chapter scope
            to associate with Chapters.
            total (int): Total number of chapters to create.
            batch_size (int): Number of chapters to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Chapter]: List of created Product objects.
        """
        chapter_objs = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope=Scope.CHAPTER,
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(lessons),
                is_buyable=False,
                description=self.get_random_text(6),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'chapter {self.get_random_words(3)}')
        ]
        chapters = Product.objects.bulk_create(
            chapter_objs,
            batch_size=batch_size
        )

        return chapters

    def create_practices(
        self,
        lessons: List[Lesson],
        total: int = 1_000,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Practice]:
        """Create Product objects with Practice scope.

        Args:
            lessons (List[Lesson]): List of Product objects with Lesson scope
            to associate with Practices.
            total (int): Total number of practices to create.
            batch_size (int): Number of practices to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Practice]: List of created Product objects.
        """
        practice_objs = [
            Product(
                title=words,
                slug=slugify(words),
                sku=self.get_random_sku(),
                scope=Scope.PRACTICE,
                difficulty=self.get_random_difficulty(),
                parent=self.get_random_from_seq(lessons),
                is_buyable=False,
                description=self.get_random_text(6),
                priority=self.get_random_int(1, total),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
            if (words := f'practice {self.get_random_words(3)}')
        ]
        practices = Product.objects.bulk_create(
            practice_objs,
            batch_size=batch_size
        )

        return practices

    def create_bundles(
        self,
        bootcamps: List[Bootcamp],
        courses: List[Course],
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Bundle]:
        """Create Bundle objects.

        Args:
            bootcamps (List[Bootcamp]): List of Product objects with Bootcamp
            scope to associate with Bundles.
            courses (List[Course]): List of Product objects with Course scope
            to associate with Bundles.
            batch_size (int): Number of bundles to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Bundle]: List of created Bundle objects.
        """
        bundle_objs = [
            Bundle(
                bootcamp=self.get_random_from_seq(bootcamps),
                course=course,
            )
            for course in tqdm(
                courses,
                disable=disable_progress_bar
            )
        ]
        bundles = Bundle.objects.bulk_create(
            bundle_objs,
            batch_size=batch_size,
        )

        return bundles

    # - chapter creation -
    def create_chapter_medias(
        self,
        chapters: List[Chapter],
        total: int = 500,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[ProductMedia]:
        """
        Create and insert a batch of ProductMedia(chapter media) objects into
        the database.

        This method generates a list of ProductMedia objects by iterating
        through a range of `total`, where each object is created with random
        attributes. The chapter media objects are then bulk inserted into the
        database.

        Parameters:
            chapters (List[Chapter]): A list of Product objects with Chapter
                scope from which the products are randomly chosen for media
                generation.
            total (int, optional): The total number of chapter media objects to
                generate.
            batch_size (int, optional): The number of objects to insert in each
                database bulk create operation.
            disable_progress_bar (bool, optional): If True, disables the
                progress bar during the creation process.

        Returns:
            List[ProductMedia]: A list of generated ProductMedia objects that
            have been inserted into the database.
        """
        chapter_media_objs = [
            ProductMedia(
                product=self.get_random_from_seq(
                    self.split_chapters(
                        chapters,
                        is_question=False
                    )
                ),
                sku=self.get_random_sku(),
                alternate_text=self.get_random_words(3),
                width_field=self.get_random_int(50, 800),
                height_field=self.get_random_int(50, 800),
                duration=self.get_random_float(1, 60),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
        ]
        chapter_medias = ProductMedia.objects.bulk_create(
            chapter_media_objs,
            batch_size=batch_size
        )

        return chapter_medias

    def create_no_chapter_product_medias(
        self,
        no_chapter_products: List[Product],
        total: int = 1_000_000,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[ProductMedia]:
        """
        Create and insert random product media objects excluding products with
        Chapter scope into the database.

        Parameters:
            products (List[Product]): List of Product objects(without chapters)
            for random selection.
            total (int, optional): Total number of objects to generate.
            batch_size (int, optional): Number of objects per bulk insert.
            disable_progress_bar (bool, optional): Disable progress bar.

        Returns:
            List[ProductMedia]: List of generated product media objects
            inserted in the database.
        """

        with open(os.path.join(BASE_DIR, os.path.normpath('media/demo/picture/Cucumber.jpg')), 'rb') as pic_file:
            pic_data = pic_file.read()

        with open(os.path.join(BASE_DIR, os.path.normpath('media/demo/video/eye.mp4')), 'rb') as video_file:
            video_data = video_file.read()

        with open(os.path.join(BASE_DIR, os.path.normpath('media/demo/pdf/sample.PDF')), 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        product_media_objs = [
            ProductMedia(
                product=self.get_random_from_seq(no_chapter_products),
                picture=SimpleUploadedFile(name='Cucumber.jpg', content=pic_data),
                video=SimpleUploadedFile(name='eye.mp4', content=video_data),
                pdf=SimpleUploadedFile(name='sample.PDF', content=pdf_data),
                sku=self.get_random_sku(),
                alternate_text=self.get_random_words(3),
                width_field=self.get_random_int(50, 800),
                height_field=self.get_random_int(50, 800),
                duration=self.get_random_float(1, 60),
            )
            for _ in tqdm(range(total), disable=disable_progress_bar)
        ]
        product_medias = ProductMedia.objects.bulk_create(
            product_media_objs,
            batch_size=batch_size
        )

        return product_medias

    def create_questions(
        self,
        chapters: List[Chapter],
        total: int = 1_000_000,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Question]:
        """Create Question objects.

        Args:
            chapters (List[Chapter]): List of Product objects with chapter
            scope to associate with Questions.
            total (int): Total number of questions to create.
            batch_size (int): Number of questions to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[Question]: List of created Question objects.
        """
        question_objs = [
            Question(
                product=self.get_random_from_seq(
                    self.split_chapters(
                        chapters,
                        is_question=True
                    )
                ),
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
        questions: List[Question],
        total: int = 1_000_000,
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[QuestionHelp]:
        """Create QuestionHelp objects.

        Args:
            questions (List[Question]): List of Question objects to associate
            with QuestionHelps.
            total (int): Total number of question helps to create.
            batch_size (int): Number of question helps to create in each batch.
            disable_progress_bar (bool): Whether to disable the progress bar.

        Returns:
            List[QuestionHelp]: List of created QuestionHelp objects.
        """
        question_help_objs = [
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

    # - answer creation -
    def create_checkbox_answers(
        self,
        questions: List[CheckboxQuestion],
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Answer]:
        """
        Create and insert Answer objects with checkbox type questions into the
        database.

        Parameters:
            questions (List[CheckboxQuestion]): List of CheckboxQuestion
            objects.
            batch_size (int, optional): Number of objects per bulk insert.
            disable_progress_bar (bool, optional): Disable progress bar.

        Returns:
            List[Answer]: List of generated answer objects inserted in the
            database.
        """
        answer_objs = [
            Answer(
                question=question,
                text=self.get_random_words(3),
                order_placeholder=None,
                is_correct=self.get_random_bool(),
                priority=next(self.priority_counter)
            )
            for question in tqdm(questions, disable=disable_progress_bar)
            for _ in range(self.get_random_int(2, 7))
        ]

        answers = Answer.objects.bulk_create(
            answer_objs,
            batch_size=batch_size
        )

        return answers

    def create_radio_answers(
        self,
        questions: List[RadioQuestion],
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Answer]:
        """
        Create and insert Answer objects with radio type questions into the
        database.

        Parameters:
            questions (List[RadioQuestion]): List of RadioQuestion objects.
            batch_size (int, optional): Number of objects per bulk insert.
            disable_progress_bar (bool, optional): Disable progress bar.

        Returns:
            List[Answer]: List of generated answer objects inserted in the
            database.
        """
        answer_objs = [
            Answer(
                question=question,
                text=self.get_random_words(3),
                order_placeholder=None,
                is_correct=self.set_is_correct(number),
                priority=next(self.priority_counter)
            )
            for question in tqdm(questions, disable=disable_progress_bar)
            for number in range(4)
        ]

        answers = Answer.objects.bulk_create(
            answer_objs,
            batch_size=batch_size
        )

        return answers

    def create_placeholder_answers(
        self,
        questions: List[PlaceholderQuestion],
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Answer]:
        """
        Create and insert Answer objects with placeholder type questions into
        the database.

        Parameters:
            questions (List[PlaceholderQuestion]): List of PlaceholderQuestion
            objects.
            batch_size (int, optional): Number of objects per bulk insert.
            disable_progress_bar (bool, optional): Disable progress bar.

        Returns:
            List[Answer]: List of generated answer objects inserted in the
            database.
        """
        answer_objs = [
            Answer(
                question=question,
                text=self.get_random_words(1),
                order_placeholder=order_placeholder,
                is_correct=self.get_random_bool(),
                priority=next(self.priority_counter)
            )
            for question in tqdm(questions, disable=disable_progress_bar)
            for order_placeholder in range(self.get_random_int(2, 7))
        ]

        answers = Answer.objects.bulk_create(
            answer_objs,
            batch_size=batch_size
        )

        return answers

    def create_conditional_answers(
        self,
        questions: List[ConditionalQuestion],
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Answer]:
        """
        Create and insert Answer objects with conditional type questions into the
        database.

        Parameters:
            questions (List[ConditionalQuestion]): List of ConditionalQuestion
            objects.
            batch_size (int, optional): Number of objects per bulk insert.
            disable_progress_bar (bool, optional): Disable progress bar.

        Returns:
            List[Answer]: List of generated answer objects inserted in the
            database.
        """
        answer_objs = [
            Answer(
                question=question,
                text=self.get_random_words(3),
                order_placeholder=None,
                is_correct=is_correct,
                priority=next(self.priority_counter)
            )
            for question in tqdm(questions, disable=disable_progress_bar)
            for is_correct in (True, False)
        ]

        answers = Answer.objects.bulk_create(
            answer_objs,
            batch_size=batch_size
        )

        return answers

    def create_code_answers(
        self,
        questions: List[CodeQuestion],
        batch_size: int = 1_000_000,
        disable_progress_bar: bool = False
    ) -> List[Answer]:
        """
        Create and insert Answer objects with code type questions into the
        database.

        Parameters:
            questions (List[CodeQuestion]): List of CodeQuestion objects.
            batch_size (int, optional): Number of objects per bulk insert.
            disable_progress_bar (bool, optional): Disable progress bar.

        Returns:
            List[Answer]: List of generated answer objects inserted in the
            database.
        """
        answer_objs = [
            Answer(
                question=question,
                text=self.get_random_words(3),
                order_placeholder=None,
                is_correct=True,
                priority=next(self.priority_counter)
            )
            for question in tqdm(questions, disable=disable_progress_bar)
        ]

        answers = Answer.objects.bulk_create(
            answer_objs,
            batch_size=batch_size
        )

        return answers
