from django.test import TestCase
from django.core.exceptions import ValidationError

from elearning.warehouse.models import ProductMedia
from elearning.warehouse.repository.generator import WarehouseDataGenerator


class ProductMediaTest(TestCase):
    TOTAL_DIVISIONS = 1
    TOTAL_BOOTCAMPS = 5
    TOTAL_PROJECTS = 5
    TOTAL_COURSES = 5
    TOTAL_LESSONS = 5
    TOTAL_CHAPTERS = 5
    TOTAL_PRACTICES = 5

    TOTAL_CHAPTER_MEDIAS = 5
    TOTAL_NO_CHAPTER_MEDIAS = 5

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

        cls.no_chapter_products = (cls.divisions + cls.bootcamps + cls.projects
            + cls.courses + cls.lessons + cls.practices
        )

        cls.chapter_medias = cls.generator.create_chapter_medias(
            chapters=cls.chapters,
            total=cls.TOTAL_CHAPTER_MEDIAS,
            disable_progress_bar=True
        )
        cls.no_chapter_medias = cls.generator.create_no_chapter_product_medias(
            no_chapter_products=cls.no_chapter_products,
            total=cls.TOTAL_NO_CHAPTER_MEDIAS,
            disable_progress_bar=True
        )

        cls.product_medias = cls.chapter_medias + cls.no_chapter_medias

    def test_valid_product_for_product_media(self):
        product_media = ProductMedia(
            product=self.lessons[0],
            duration=5.00
        )
        with self.assertRaises(ValidationError) as error:
            product_media.clean()
        self.assertIn("Lessons can not have product media.", error.exception.messages)

    def test_str(self):
        with self.assertNumQueries(0):
            for product_media in self.product_medias:
                actual = str(product_media)
                expected = f"{product_media.id} Product Media"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __str__ is `{actual}` but got `{expected}`"
                )

    def test_repr(self):
        with self.assertNumQueries(0):
            for product_media in self.product_medias:
                actual = repr(product_media)
                expected = f"{product_media.__class__.__name__}: {product_media.id}"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __str__ is `{actual}` but got `{expected}`"
                )
