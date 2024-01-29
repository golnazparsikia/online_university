from django.test import TestCase

from elearning.warehouse.repository.generator import WarehouseDataGenerator as DGL      # noqa: E505

class WarehouseModelsTest(TestCase):
    TOTAL_PRODUCTS = 5
    TOTAL_DIVISION = 5
    TOTAL_BOOTCAMP = 5
    TOTAL_COURSE = 5
    TOTAL_CHAPTER = 5
    TOTAL_LESSON = 5
    TOTAL_PROJECT = 5
    TOTAL_PRACTICE = 5
    TOTAL_QUESTIONS = 5
    TOTAL_QUESTION_HELPS = 5

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.generator = DGL(locale='en')

        cls.Division = cls.generator.create_divisions(
            cls.TOTAL_DIVISION,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Bootcamp = cls.generator.create_bootcamps(
            cls.Division,
            cls.TOTAL_BOOTCAMP,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Course = cls.generator.create_courses(
            cls.TOTAL_COURSE,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Lesson = cls.generator.create_lessons(
            cls.Course,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Chapter = cls.generator.create_chapters(
            cls.Lesson,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Project = cls.generator.create_projects(
            cls.Chapter,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Practice = cls.generator.create_practices(
            cls.Project,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Question = cls.generator.create_questions(
            cls.Practice,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Question_help = cls.generator.create_question_helps(
            cls.Question,
            batch_size=5000,
            disable_progress_bar=True
    )

        cls.Checkbox = cls.generator.create_checkbox_answers(
            questions=cls.Question,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Radio = cls.generator.create_radio_answers(
            questions=cls.Question,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Placeholder = cls.generator.create_placeholder_answers(
            questions=cls.Question,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Conditional = cls.generator.create_conditional_answers(
            questions=cls.Question,
            batch_size=5000,
            disable_progress_bar=True
    )
        cls.Code = cls.generator.create_code_answers(
            questions=cls.Question,
            batch_size=5000,
            disable_progress_bar=True
    )

    def test_division_str_method(self):
        with self.assertNumQueries(0):
            for division in self.Division:
                actual_str = str(division)
                expected_str = division.title
                actual_repr = repr(division)
                expected_repr = division.title
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_bootcamp_str_repr_method(self):
        with self.assertNumQueries(0):
            for bootcamp in self.Bootcamp:
                actual_str = str(bootcamp)
                expected_str = bootcamp.title
                actual_repr = repr(bootcamp)
                expected_repr = bootcamp.title
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_course_str_repr_method(self):
        with self.assertNumQueries(0):
            for Course in self.Course:
                actual_str = str(Course)
                expected_str = Course.title
                actual_repr = repr(Course)
                expected_repr = Course.title
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_lesson_str_repr_method(self):
        with self.assertNumQueries(0):
            for Lesson in self.Lesson:
                actual_str = str(Lesson)
                expected_str = Lesson.title
                actual_repr = repr(Lesson)
                expected_repr = Lesson.title
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_chapter_str_repr_repr_method(self):
        with self.assertNumQueries(0):
            for Chapter in self.Chapter:
                actual_str = str(Chapter)
                expected_str = Chapter.title
                actual_repr = repr(Chapter)
                expected_repr = Chapter.title
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_project_str_repr_method(self):
        with self.assertNumQueries(0):
            for Project in self.Project:
                actual_str = str(Project)
                expected_str = Project.title
                actual_repr = repr(Project)
                expected_repr = Project.title
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_Practice_str_repr_method(self):
        with self.assertNumQueries(0):
            for Practice in self.Practice:
                actual_str = str(Practice)
                expected_str = Practice.title
                actual_repr = repr(Practice)
                expected_repr = Practice.title
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )


    def test_checkbox_str_repr_method(self):
        with self.assertNumQueries(0):
            for Checkbox in self.Checkbox:
                actual_str = str(Checkbox)
                expected_str = f'{Checkbox.id} Answer'
                actual_repr = repr(Checkbox)
                expected_repr = f'{Checkbox.id} Answer'
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_radio_str_repr_method(self):
        with self.assertNumQueries(0):
            for Radio in self.Radio:
                actual_str = str(Radio)
                expected_str = f'{Radio.id} Answer'
                actual_repr = repr(Radio)
                expected_repr = f'{Radio.id} Answer'
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_placeholder_str_repr_method(self):
        with self.assertNumQueries(0):
            for Placeholder in self.Placeholder:
                actual_str = str(Placeholder)
                expected_str = f'{Placeholder.id} Answer'
                actual_repr = repr(Placeholder)
                expected_repr = f'{Placeholder.id} Answer'
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_checkbox_str_repr_method(self):
        with self.assertNumQueries(0):
            for Checkbox in self.Checkbox:
                actual_str = str(Checkbox)
                expected_str = f'{Checkbox.id} Answer'
                actual_repr = repr(Checkbox)
                expected_repr = f'{Checkbox.id} Answer'
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_conditional_str_repr_method(self):
        with self.assertNumQueries(0):
            for Conditional in self.Conditional:
                actual_str = str(Conditional)
                expected_str = f'{Conditional.id} Answer'
                actual_repr = repr(Conditional)
                expected_repr = f'{Conditional.id} Answer'
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )

    def test_code_str_repr_method(self):
        with self.assertNumQueries(0):
            for Code in self.Code:
                actual_str = str(Code)
                expected_str = f'{Code.id} Answer'
                actual_repr = repr(Code)
                expected_repr = f'{Code.id} Answer'
                
                self.assertEqual(
                    actual_str,
                    expected_str,
                    msg=f'Actual __str__ method is `{actual_str}` '
                        f'but expected is `{expected_str}`.'
                )
                self.assertEqual(
                    actual_repr,
                    expected_repr,
                    msg=f'Actual __str__ method is `{actual_repr}` '
                        f'but expected is `{expected_repr}`.'
                )


    def test_str_question(self):
        postfix = "{} Question"
        with self.assertNumQueries(0):
            for question in self.Question:
                actual = str(question)
                expected = postfix.format(question.id)
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"Actual __str__ method is `{actual}` "
                        f"but expected is `{expected}`."
                )

    def test_repr_question(self):
        postfix = "{} Question"
        with self.assertNumQueries(0):
            for question in self.Question:
                actual = repr(question)
                expected = postfix.format(question.id)
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"Actual __repr__ method is `{actual}` "
                        f"burt expected is `{expected}`."
                )

    def test_str_question_help(self):
        postfix = "{} Question Help"
        with self.assertNumQueries(0):
            for question_help in self.Question_help:
                actual = str(question_help)
                expected = postfix.format(question_help.id)
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"Actual __str__ method is `{actual}` "
                        f"but expected is `{expected}`."
                )

    def test_repr_question_help(self):
        postfix = "{} Question Help"
        with self.assertNumQueries(0):
            for question_help in self.Question_help:
                actual = repr(question_help)
                expected = postfix.format(question_help.id)
                self.assertEqual(
                    actual,
                    expected,
                    msg=f"Actual __repr__ method is `{actual}` "
                        f"burt expected is `{expected}`."
                )