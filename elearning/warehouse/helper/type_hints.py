from django.db.models import QuerySet

from elearning.warehouse.models import (
    Product,
    Bundle,
    ProductMedia,
    Question,
    QuestionHelp,
    Answer
)

ProductQuerySet = QuerySet(Product)
BundleQuerySet = QuerySet(Bundle)
ProductMediaQuerySet = QuerySet(ProductMedia)
QuestionQuerySet = QuerySet(Question)
QuestionHelpQuerySet = QuerySet(QuestionHelp)
AnswerQuerySet = QuerySet(Answer)
