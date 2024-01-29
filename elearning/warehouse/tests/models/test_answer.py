from django.test import TestCase
from django.core.exceptions import ValidationError

from elearning.warehouse.models import Question, Answer
from elearning.warehouse.repository.generator import WarehouseDataGenerator
from elearning.warehouse.helper.consts import QuestionType


class AnswerModelTest(TestCase):
    TOTAL_DIVISIONS = 1
    TOTAL_BOOTCAMPS = 1
    TOTAL_PROJECTS = 1
    TOTAL_COURSES = 1
    TOTAL_LESSONS = 1
    TOTAL_CHAPTERS = 5
    TOTAL_QUESTIONS = 5
    TOTAL_CHECKBOX_ANSWERS = 1
    TOTAL_RADIO_ANSWERS = 1
    TOTAL_PLACEHOLDER_ANSWERS = 1
    TOTAL_CONDITIONAL_ANSWERS = 1
    TOTAL_CODE_ANSWERS = 1

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

        cls.checkbox_answers = cls.generator.create_checkbox_answers(
            questions=cls.questions,
            disable_progress_bar=True
        )
        cls.radio_answers = cls.generator.create_radio_answers(
            questions=cls.questions,
            disable_progress_bar=True
        )
        cls.placeholder_answers = cls.generator.create_placeholder_answers(
            questions=cls.questions,
            disable_progress_bar=True
        )
        cls.conditional_answers = cls.generator.create_conditional_answers(
            questions=cls.questions,
            disable_progress_bar=True
        )
        cls.code_answers = cls.generator.create_code_answers(
            questions=cls.questions,
            disable_progress_bar=True
        )

        cls.answers = (
            cls.checkbox_answers + cls.radio_answers + cls.placeholder_answers
            + cls.conditional_answers + cls.code_answers
        )

    def test_none_order_placeholder_for_no_placeholder_questions(self):
        question = Question(
            product=self.chapters[0],
            text="Question's Text",
            kind=QuestionType.CHECKBOX
        )

        answer = Answer(
            question=question,
            text="Answer's Text",
            is_correct=False,
            order_placeholder=1
        )

        with self.assertRaises(ValidationError) as error:
            answer.clean()
        self.assertIn("Questions other than placeholders should have None for placeholders.", error.exception.messages)

    def test_unique_order_placeholder_for_placeholder_questions(self):
        question = Question(
            product=self.chapters[1],
            text="Question's Text",
            kind=QuestionType.PLACEHOLDER
        )

        answer1 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=False,
            order_placeholder=1
        )
        answer2 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=False,
            order_placeholder=1
        )

        with self.assertRaises(ValidationError) as error:
            question.save()
            answer1.save()
            answer2.clean()
        self.assertIn("This order_placeholder for this question is duplicated.", error.exception.messages)

    def test_just_one_true_answer_for_radio_questions(self):
        question = Question(
            product=self.chapters[2],
            text="Question's Text",
            kind=QuestionType.RADIO
        )

        answer1 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=True,
            order_placeholder=None
        )
        answer2 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=True,
            order_placeholder=None
        )

        with self.assertRaises(ValidationError) as error:
            question.save()
            answer1.save()
            answer2.clean()
        self.assertIn("Only 1 correct answer is ok for radio and conditional question type.", error.exception.messages)

    def test_just_one_true_answer_for_conditional_questions(self):
        question = Question(
            product=self.chapters[2],
            text="Question's Text",
            kind=QuestionType.CONDITIONAL
        )

        answer1 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=True,
            order_placeholder=None
        )
        answer2 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=True,
            order_placeholder=None
        )

        with self.assertRaises(ValidationError) as error:
            question.save()
            answer1.save()
            answer2.clean()
        self.assertIn("Only 1 correct answer is ok for radio and conditional question type.", error.exception.messages)

    def test_just_one_answer_for_code_questions(self):
        question = Question(
            product=self.chapters[3],
            text="Question's Text",
            kind=QuestionType.CODE
        )

        answer1 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=True,
            order_placeholder=None
        )
        answer2 = Answer(
            question=question,
            text="Answer's Text",
            is_correct=False,
            order_placeholder=None
        )

        with self.assertRaises(ValidationError) as error:
            question.save()
            answer1.save()
            answer2.clean()
        self.assertIn("It should be just 1 answer for code type questions.", error.exception.messages)

    def test_just_true_answer_allow_for_code_question(self):
        question = Question(
            product=self.chapters[4],
            text="Question's Text",
            kind=QuestionType.CODE
        )

        answer = Answer(
            question=question,
            text="Answer's Text",
            is_correct=False,
            order_placeholder=None
        )

        with self.assertRaises(ValidationError) as error:
            answer.clean()
        self.assertIn("The answer should be correct for the code type question.", error.exception.messages)

    def test_str(self):
        with self.assertNumQueries(0):
            for answer in self.answers:
                actual = str(answer)
                expected = f"{answer.id} Answer"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __str__ is `{actual}` but got `{expected}`"
                )

    def test_repr(self):
        with self.assertNumQueries(0):
            for answer in self.answers:
                actual = repr(answer)
                expected = f"{answer.__class__.__name__}: {answer.id}"
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"actual __repr__ is `{actual}` but got `{expected}`"
                )
