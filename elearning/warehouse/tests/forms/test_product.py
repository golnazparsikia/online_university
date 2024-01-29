from django.test import TestCase
from django.core.exceptions import ValidationError

from elearning.warehouse.forms import (
    DivisionForm,
    BootcampForm,
    CourseForm,
    LessonForm,
    ChapterForm,
    PracticeForm,
    ProjectForm
)
from elearning.warehouse.repository.generator import WarehouseDataGenerator
from elearning.warehouse.helper.consts import Scope


class ProductFormTest(TestCase):
    TOTAL_DIVISIONS = 1
    TOTAL_BOOTCAMPS = 1
    TOTAL_PROJECTS = 1
    TOTAL_COURSES = 1
    TOTAL_LESSONS = 1
    TOTAL_CHAPTERS = 1
    TOTAL_PRACTICES = 1

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

        cls.division_form = DivisionForm(instance=cls.divisions[0])
        cls.bootcamp_form = BootcampForm(instance=cls.bootcamps[0])
        cls.course_form = CourseForm(instance=cls.courses[0])
        cls.project_form = ProjectForm(instance=cls.projects[0])
        cls.lesson_form = LessonForm(instance=cls.lessons[0])
        cls.chapter_form = ChapterForm(instance=cls.chapters[0])
        cls.practice_form = PracticeForm(instance=cls.practices[0])

    def test_valid_initial_scope_division(self):
        self.assertEqual(self.division_form.fields["scope"].initial, Scope.DIVISION)

    def test_valid_initial_scope_bootcamp(self):
        self.assertEqual(self.bootcamp_form.fields["scope"].initial, Scope.BOOTCAMP)

    def test_valid_initial_scope_course(self):
        self.assertEqual(self.course_form.fields["scope"].initial, Scope.COURSE)

    def test_valid_initial_scope_project(self):
        self.assertEqual(self.project_form.fields["scope"].initial, Scope.PROJECT)

    def test_valid_initial_scope_lesson(self):
        self.assertEqual(self.lesson_form.fields["scope"].initial, Scope.LESSON)

    def test_valid_initial_scope_chapter(self):
        self.assertEqual(self.chapter_form.fields["scope"].initial, Scope.CHAPTER)

    def test_valid_initial_scope_practice(self):
        self.assertEqual(self.practice_form.fields["scope"].initial, Scope.PRACTICE)

    # TODO: clean_scope method in form have to be test.
    # def test_clean_scope_division(self):
    #     self.division_form.data["scope"] = Scope.BOOTCAMP

    #     # Check that form is not valid
    #     self.assertFalse(self.division_form.is_valid())
    #     breakpoint()

    #     # Assert the ValidationError is raised
    #     self.assertIn('Scope must be Division.', self.division_form.errors["scope"])

