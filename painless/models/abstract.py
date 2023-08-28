import os
import io
from PIL import Image
from pathlib import Path
from django.db import models
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)


class PictureOperationAbstract(models.Model):
    """
    Abstract base model providing functionality for working with pictures.

    This model abstracts the common picture-related functionality like alternate text, dimensions,
    and methods to retrieve information about the picture.

    Attributes:
        alternate_text (str): Alternate text for the picture, used for accessibility and SEO purposes.
        width_field (int): Width of the picture in pixels (editable field).
        height_field (int): Height of the picture in pixels (editable field).

    Meta:
        abstract (bool): Indicates that this is an abstract base model.

    Methods:
        get_picture_url(): Get the URL of the picture or a placeholder if no picture is available.
        get_picture_size(): Get the size of the picture file in bytes.
        get_picture_dimensions(): Get the dimensions of the picture (width, height).
        get_file_name(): Get the name of the picture file.
    """

    alternate_text = models.CharField(
        _("Alternate Text"),
        max_length=110,
        validators=[
            MaxLengthValidator(150),
            MinLengthValidator(3)
        ],
        null=True,
        blank=True,
        help_text=_('Describe the picture that is uploaded. Please provide a descriptive text for accessibility and SEO.')
    )

    width_field = models.PositiveSmallIntegerField(
        _("Picture Width"),
        null=True,
        blank=True,
        editable=False,
        help_text=_("Width of the picture in pixels.")
    )

    height_field = models.PositiveSmallIntegerField(
        _("Picture Height"),
        null=True,
        blank=True,
        editable=False,
        help_text=_("Height of the picture in pixels.")
    )

    class Meta:
        abstract = True

    def get_picture_url(self):
        """
        Get the URL of the picture or a placeholder if no picture is available.

        Returns:
            str: The URL of the picture or a placeholder text.
        """
        return self.picture.url if self.picture else 'No Image'

    def get_picture_size(self):
        """
        Get the size of the picture file in bytes.

        Returns:
            int: The size of the picture file in bytes.
        """
        return self.picture.size

    def get_picture_dimensions(self):
        """
        Get the dimensions of the picture (width, height).

        Returns:
            tuple: A tuple containing the width and height of the picture.
        """
        return (self.picture.width, self.picture.height)

    def get_file_name(self):
        """
        Get the name of the picture file.

        Returns:
            str: The name of the picture file.
        """
        return os.path.basename(self.picture.name)
