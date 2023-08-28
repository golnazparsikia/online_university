from django.db import models
from django.utils.translation import gettext_lazy as _

from painless.models.mixins.common import TimestampMixin
from painless.models.abstract import PictureOperationAbstract

class Gallery(PictureOperationAbstract, TimestampMixin):
    """
    Represents a gallery of images in the warehouse.

    This model represents a gallery containing images in the warehouse. It inherits from
    PictureOperationAbstract and TimestampMixin, providing additional functionality and timestamp fields.

    Attributes:
        title (str): The title of the gallery.
        picture (ImageField): The image associated with the gallery.
        objects (Manager): The default manager for the model.
    
    Meta:
        verbose_name (str): The singular name for the model, displayed in the admin interface.
        verbose_name_plural (str): The plural name for the model, displayed in the admin interface.
        default_manager_name (str): The name of the default manager for the model.

    Methods:
        __str__(): Returns a string representation of the gallery (its title).
        __repr__(): Returns a string representation of the gallery (its title).
    """

    title = models.CharField(
        "Title",
        unique=True,
        max_length=100,
        help_text="Title of the Product"
    )

    picture = models.ImageField(
        _("picture"),
        upload_to='shop/warehouse/gallery/',
        height_field='height_field',
        width_field='width_field',
        max_length=110,
        validators=[],
        null=True,
        blank=True,
        help_text=_('Image field for the gallery'),
        db_comment='Image field for the gallery'
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
        default_manager_name = 'objects'

    def __str__(self):
        """
        Returns a string representation of the gallery.

        Returns:
            str: The title of the gallery.
        """
        return self.title

    def __repr__(self):
        """
        Returns a string representation of the gallery.

        Returns:
            str: The title of the gallery.
        """
        return self.title
