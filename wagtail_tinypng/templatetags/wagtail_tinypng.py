# -*- coding: utf-8 -*-
import os

from django import template
from django.conf import settings
from wagtail.images import get_image_model

from ..models import WagtailTinyPNGImage
from ..utils import display_size as display_size_function

register = template.Library()


@register.simple_tag()
def wagtail_tinypng_image(image_id):

    # Get the image model. It might be a custom image model. Best to use this.
    Image = get_image_model()
    try:
        image = Image.objects.get(pk=image_id)
    except Image.DoesNotExist:
        # Image does not exist
        return {}
    except Exception:
        # A catch-all exception
        return {}

    tinified_image, created = WagtailTinyPNGImage.objects.get_or_create(wagtail_image=image)

    # Check if the original image size matches the comrpessed size (if compressed)
    # If the image is not compressed, do nothing.
    # If the image IS compressed and the minified_size doesn't match the original image file_size,
    # then reset the fields on `tinifed_image`
    wagtail_image = tinified_image.wagtail_image
    if tinified_image.is_minified and tinified_image.minified_size != wagtail_image.file_size:
        # Image is minified and there's an image size conflict between what was minified and what currently exists
        tinified_image.minified_size = 0
        tinified_image.original_size = wagtail_image.file_size
        tinified_image.save()

    return {
        'tinified': tinified_image,
    }


@register.filter
def display_size(value):
    """A simple template filter to turn bytes into B, KB, MB, GB, TB, etc."""
    return display_size_function(value)


@register.filter
def allowable_image_type(image_object):
    """Check if an image object has a .jpeg, .jpg or .png extension."""
    filename, file_extension = os.path.splitext(image_object.filename)
    if file_extension.lower() in ['.jpeg', '.jpg', '.png']:
        return True
    return False


@register.simple_tag(takes_context=False, name='has_tinypng_key')
def has_tinypng_key():
    """Used for checking if an API key is set in the template."""
    api_key = getattr(settings, 'TINIFY_API_KEY', False)
    return api_key
