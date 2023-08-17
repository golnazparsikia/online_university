from enum import Enum

from django.db import models


class Scope(models.TextChoices):
    DIVISION = "Division"
    BOOTCAMP = "Bootcamp"
    COURSE = "Course"
    LESSON = "Lesson"
    CHAPTER = "Chapter"
    PROJECT = "Project"
    PRACTICE = "Practice"


class QuestionType(models.TextChoices):
    CHECKBOX = "Checkbox"
    RADIO = "Radio"
    PLACEHOLDER = "Placeholder"
    CONDITIONAL = "Conditional"
    CODE = "Code"


class Difficulty(models.TextChoices):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCE = "Advance"
    PRODUCTIVE = "Productive"


class QuestionTypeAnswersCount(Enum):
    CHECKBOX = 5
    RADIO = 4
    PLACEHOLDER = 1
    CONDITIONAL = 2
    CODE = 1
