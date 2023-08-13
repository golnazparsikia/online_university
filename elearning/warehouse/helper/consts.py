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
    PRACTICE = "Practice"


class DIFFICULTY(models.TextChoices):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCE = "Advance"
    PRODUCTIVE = "Productive"
