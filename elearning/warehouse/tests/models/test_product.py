from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from elearning.warehouse.models import Product
from elearning.warehouse.repository.generator import WarehouseDataGenerator
from elearning.warehouse.helper.consts import Scope, Difficulty

class ProductModelTest(TestCase):
    TOTAL_DIVISIONS = 1
    TOTAL_BOOTCAMPS = 5
    TOTAL_PROJECTS = 5
    TOTAL_COURSES = 5
    TOTAL_LESSONS = 5
    TOTAL_CHAPTERS = 5
    TOTAL_PRACTICES = 5

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.generator = WarehouseDataGenerator()
        cls.divisions = cls.generator.create_divisions(
            total=cls.TOTAL_DIVISIONS,
            disable_progress_bar=True
        )
        cls.bootcamps = cls.generator.create_bootcamps(
            divisions=cls.divisions,
            total=cls.TOTAL_BOOTCAMPS,
            disable_progress_bar=True
        )
        cls.projects = cls.generator.create_projects(
            bootcamps=cls.bootcamps,
            total=cls.TOTAL_PROJECTS,
            disable_progress_bar=True
        )
        cls.courses = cls.generator.create_courses(
            total=cls.TOTAL_COURSES,
            disable_progress_bar=True
        )
        cls.lessons = cls.generator.create_lessons(
            courses=cls.courses,
            total=cls.TOTAL_LESSONS,
            disable_progress_bar=True
        )
        cls.chapters = cls.generator.create_chapters(
            lessons=cls.lessons,
            total=cls.TOTAL_CHAPTERS,
            disable_progress_bar=True
        )
        cls.practices = cls.generator.create_practices(
            lessons=cls.lessons,
            total=cls.TOTAL_PRACTICES,
            disable_progress_bar=True
        )

        cls.products = (cls.divisions + cls.bootcamps + cls.projects
            + cls.courses + cls.lessons + cls.chapters + cls.practices
        )

    def test_invalid_parent_for_division(self):
        title = "Division Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.chapters[0],
            scope=Scope.DIVISION,
            is_buyable=False,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("Invalid parent for the division.", error.exception.messages)

    def test_invalid_parent_for_bootcamp(self):
        title = "Bootcamp Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.practices[0],
            scope=Scope.BOOTCAMP,
            is_buyable=False,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("Invalid parent for the bootcamp.", error.exception.messages)

    def test_invalid_parent_for_course(self):
        title = "Course Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.lessons[0],
            scope=Scope.COURSE,
            is_buyable=True,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("Invalid parent for the course.", error.exception.messages)

    def test_invalid_parent_for_project(self):
        title = "Project Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.divisions[0],
            scope=Scope.PROJECT,
            is_buyable=False,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("Invalid parent for the project.", error.exception.messages)

    def test_invalid_parent_for_lesson(self):
        title = "Lesson Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.bootcamps[0],
            scope=Scope.LESSON,
            is_buyable=False,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("Invalid parent for the lesson.", error.exception.messages)

    def test_invalid_parent_for_chapter(self):
        title = "Chapter Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.courses[0],
            scope=Scope.CHAPTER,
            is_buyable=False,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("Invalid parent for the chapter.", error.exception.messages)

    def test_invalid_parent_for_practice(self):
        title = "Practice Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.divisions[0],
            scope=Scope.PRACTICE,
            is_buyable=False,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("Invalid parent for the practice.", error.exception.messages)

    def test_is_buyable_false_for_no_course_products(self):
        title = "Bootcamp Title"

        product = Product(
            title=title,
            slug=slugify(title),
            parent=self.divisions[0],
            scope=Scope.BOOTCAMP,
            is_buyable=True,
            difficulty=Difficulty.ADVANCE,
            priority=20
        )

        with self.assertRaises(ValidationError) as error:
            product.clean()
        self.assertIn("All the products except courses are not buyable.", error.exception.messages)

    def test_str(self):
        with self.assertNumQueries(0):
            for product in self.products:
                actual = str(product)
                expected = product.title
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __str__ is `{actual}` but got `{expected}`"
                )

    def test_repr(self):
        with self.assertNumQueries(0):
            for product in self.products:
                actual = repr(product)
                expected = f"{product.__class__.__name__}: {product.title}"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __repr__ is `{actual}` but got `{expected}`"
                )
