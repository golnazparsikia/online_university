from typing import NewType

from django.db.models import QuerySet
from django.db.models.fields.files import File
from elearning.warehouse.models import (
    Product,
    Bundle,
    ProductMedia,
    Question,
    QuestionHelp,
    Answer
)

Division = NewType("Division", Product)
Bootcamp = NewType("Bootcamp", Product)
Course = NewType("Course", Product)
Project = NewType("Project", Product)
Lesson = NewType("Lesson", Product)
Chapter = NewType("Chapter", Product)
Practice = NewType("Practice", Product)

placeholder = NewType("Placeholder",Answer) 

ProductQuerySet = QuerySet(Product)
BundleQuerySet = QuerySet(Bundle)
ProductMediaQuerySet = QuerySet(ProductMedia)
QuestionQuerySet = QuerySet(Question)
QuestionHelpQuerySet = QuerySet(QuestionHelp)
AnswerQuerySet = QuerySet(Answer)

CheckboxQuestion = NewType("Checkbox", Question)
RadioQuestion = NewType("Radio", Question)
PlaceholderQuestion = NewType("Placeholder", Question)
ConditionalQuestion = NewType("Conditional", Question)
CodeQuestion = NewType("Code", Question)

picture = NewType("picture", File)
