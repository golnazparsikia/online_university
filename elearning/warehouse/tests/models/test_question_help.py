from django.test import TestCase

from elearning.warehouse.repository.generator import WarehouseDataGenerator


class QuestionModelTest(TestCase):
    TOTAL_DIVISIONS = 1
    TOTAL_BOOTCAMPS = 1
    TOTAL_PROJECTS = 1
    TOTAL_COURSES = 1
    TOTAL_LESSONS = 1
    TOTAL_CHAPTERS = 5
    TOTAL_QUESTIONS = 5
    TOTAL_QUESTION_HELPS = 5

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

        cls.questions = cls.generator.create_questions(
            chapters=cls.chapters,
            total=cls.TOTAL_QUESTIONS,
            disable_progress_bar=True
        )

        cls.question_helps = cls.generator.create_question_helps(
            questions=cls.questions,
            total=cls.TOTAL_QUESTION_HELPS,
            disable_progress_bar=True
        )

    def test_str(self):
        with self.assertNumQueries(0):
            for question_help in self.question_helps:
                actual = str(question_help)
                expected = f"{question_help.id} Question Help"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __str__ is `{actual}` but got `{expected}`"
                )

    def test_repr(self):
        with self.assertNumQueries(0):
            for question_help in self.question_helps:
                actual = repr(question_help)
                expected = f"{question_help.__class__.__name__}: {question_help.id}"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __repr__ is `{actual}` but got `{expected}`"
                )
