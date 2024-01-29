from django.test import TestCase
from django.core.exceptions import ValidationError

from elearning.warehouse.repository.generator import WarehouseDataGenerator
from elearning.warehouse.models import Bundle


class BundleModelTest(TestCase):
    TOTAL_DIVISIONS = 1
    TOTAL_BOOTCAMPS = 5
    TOTAL_COURSES = 5
    TOTAL_PROJECTS = 5

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

        cls.bundles = cls.generator.create_bundles(
            bootcamps=cls.bootcamps,
            courses=cls.courses,
            disable_progress_bar=True
        )

    def test_valid_bootcamp(self):
        bundle = Bundle(
            bootcamp=self.projects[0],
            course=self.courses[0]
        )

        with self.assertRaises(ValidationError) as error:
            bundle.clean()
        self.assertIn("Invalid product.", error.exception.messages)

    def test_valid_course(self):
        bundle = Bundle(
            bootcamp=self.bootcamps[1],
            course=self.projects[1]
        )

        with self.assertRaises(ValidationError) as error:
            bundle.clean()
        self.assertIn("Invalid product.", error.exception.messages)

    def test_duplicate_bundle(self):
        bundle1 = Bundle(
            bootcamp=self.bootcamps[2],
            course=self.projects[2]
        )
        bundle2 = Bundle(
            bootcamp=self.bootcamps[2],
            course=self.projects[2]
        )

        with self.assertRaises(ValidationError) as error:
            bundle1.save()
            bundle2.clean()
        self.assertIn("Invalid product.", error.exception.messages)

    def test_str(self):
        with self.assertNumQueries(0):
            for bundle in self.bundles:
                actual = str(bundle)
                expected = f"({bundle.bootcamp}, {bundle.course})"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __str__ is `{actual}` but got `{expected}`"
                )

    def test_repr(self):
        with self.assertNumQueries(0):
            for bundle in self.bundles:
                actual = repr(bundle)
                expected = f"{bundle.__class__.__name__}: ({bundle.bootcamp}, {bundle.course})"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __repr__ is `{actual}` but got `{expected}`"
                )
