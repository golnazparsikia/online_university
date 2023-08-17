from django.test import TestCase

from elearning.warehouse.models import QuestionHelp
from elearning.warehouse.repository.generator import WarehouseDataGenerator as DGL


class QuestionHelpTest(TestCase):
    TOTAL_PRODUCTS = 5
    TOTAL_QUESTIONS = 5
    TOTAL_QUESTION_HELPS = 5

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.generator = DGL(locale='en')
        cls.products = cls.generator.create_products(
            cls.TOTAL_PRODUCTS,
            batch_size=1000,
            disable_progress_bar=True
        )
        cls.questions = cls.generator.create_questions(
            cls.TOTAL_QUESTIONS,
            batch_size=1000,
            disable_progress_bar=True
        )
        cls.question_helps = cls.generator.create_question_helps(
            cls.TOTAL_QUESTION_HELPS,
            batch_size=1000,
            disable_progress_bar=True
        )

    def test_str_question_help(self):
        postfix = '{} Question Help'

        with self.assertNumQueries(0):
            for question_help in self.question_helps:
                actual = str(question_help)
                expected = postfix.format(question_help.id)
                self.assertEqual(
                    actual,
                    expected,
                    msg=f'Actual __str__ method is `{actual}` ' \
                        f'but expected is `{expected}`.'
                )

    def test_repr_question_help(self):
        postfix = '{} Question Help'

        with self.assertNumQueries(0):
            for question_help in self.question_helps:
                actual = repr(question_help)
                expected = postfix.format(question_help.id)
                self.assertEqual(
                    actual,
                    expected,
                    msg=f'Actual __repr__ method is `{actual}` ' \
                        f'but expected is `{expected}`.'
                )
