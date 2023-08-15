from enum import Enum

from django.db import models


class SCOPE(models.TextChoices):
    DIVISION = "Division"
    BOOTCAMP = "Bootcamp"
    COURSE = "Course"
    LESSON = "Lesson"
    CHAPTER = "Chapter"
    PROJECT = "Project"
    PRACTICE = "Practice"


class QUESTIONTYPES(models.TextChoices):
    CHECKBOX = "Checkbox"
    RADIO = "Radio"
    PLACEHOLDER = "Placeholder"
    CONDITIONAL = "Conditional"
    CODE = "Code"


class DIFFICULTY(models.TextChoices):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCE = "Advance"
    PRODUCTIVE = "Productive"


class QUESTIONTYPEANSWERSCOUNT(Enum):
    CHECKBOX = 5
    RADIO = 4
    PLACEHOLDER = 1
    CONDITIONAL = 2
    CODE = 1
