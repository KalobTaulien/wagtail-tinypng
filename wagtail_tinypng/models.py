from django.db import models

from .utils import display_size


class WagtailTinyPNGImage(models.Model):
    """A class to track tinifed images."""

    wagtail_image = models.OneToOneField(
        "wagtailimages.Image",  # @todo get the custom image class
        on_delete=models.CASCADE,
    )
    original_size = models.PositiveIntegerField(
        default=0, help_text="Original image size before minification"
    )
    minified_size = models.PositiveIntegerField(
        default=0, help_text="Minified image size after minification"
    )
    date_minified = models.DateTimeField(
        auto_now=False,
        blank=True,
        null=True,
        help_text="The date this image was minified",
    )

    def __str__(self):
        return self.wagtail_image.title

    @property
    def is_minified(self):
        """If there is a minified size, assume the image has been minified. 

        No need for additional database column.
        """
        if self.minified_size:
            return True 
        return False

    @property
    def savings(self):
        if self.original_size:
            percent = 100 - round(self.minified_size / self.original_size * 100)
            bytes_saved = display_size(self.original_size - self.minified_size)
            return f"{percent}% ({bytes_saved} saved)"
        return "-"
    
    @property
    def display_original_size(self):
        """Display the images' original size."""
        if not self.original_size:
            size = self.wagtail_image.file_size 
        else:
            size = self.original_size 
        return display_size(size)

    @property
    def display_minified_size(self):
        """Display the images' minified size."""
        if not self.minified_size:
            return "-"
        return display_size(self.minified_size)

    class Meta:
        verbose_name = "Compressed Image"
        verbose_name_plural = "Compressed Images"
