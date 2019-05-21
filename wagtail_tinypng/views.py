""""wagtailtinypng views."""
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

import tinify

from .models import WagtailTinyPNGImage
from .templatetags.wagtail_tinypng import allowable_image_type


class TinifyPNG(TemplateView):
    """Basic Template View for handling a POST and GET request."""

    http_method_names = ["get", "post"]

    def post(self, request, *args, **kwargs):
        """When POSTing an image minification request."""
        tinify.key = settings.TINIFY_API_KEY
        image_id = kwargs["pk"]
        image_url = reverse("wagtailimages:edit", args=(image_id,))
        image, created = WagtailTinyPNGImage.objects.get_or_create(
            wagtail_image_id=image_id
        )
        original_image = image.wagtail_image

        # If the image is not a .jpeg, .jpg or .png provide the user with a better error message
        if not allowable_image_type(original_image):
            messages.error(
                request,
                "Image format not supported. Only .jpeg, .jpg and .png images can be losslessly compressed.",
            )
            return redirect(image_url)

        # Don't check if the image is minified already.
        # A user MIGHT want to re-comrpess an image, and that's up to them
        try:
            # Set the original image filesize
            image.original_size = original_image.file.size
            # Use the image source
            source = tinify.from_file(original_image.file.path)
            # If resizing to a maximum width or height.
            # This is very "not clever" code, just to keep this nice and simple.
            resize_width = None
            resize_height = None
            if getattr(settings, "TINIFY_MAX_WIDTH", None):
                try:
                    resize_width = int(settings.TINIFY_MAX_WIDTH)
                except ValueError:
                    # Could not set a width
                    pass

                if resize_width:
                    # Resize the image to a max width of `resize_width` in pixels. ie. 2000px.
                    resized = source.resize(method="scale", width=resize_width)
                    # Write file to local system
                    resized.to_file(original_image.file.path)
            elif getattr(settings, "TINIFY_MAX_HEIGHT", None):
                try:
                    resize_height = int(settings.TINIFY_MAX_HEIGHT)
                except ValueError:
                    # Could not set a height
                    pass

                if resize_height:
                    # Resize the image to a max height of `resize_height` in pixels. ie. 2000px.
                    resized = source.resize(method="scale", height=resize_height)
                    # Write file to local system
                    resized.to_file(original_image.file.path)
            else:
                # There was no max width or height set. Compress as normal.
                source.to_file(original_image.file.path)

            # Update WagtailTinyPNGImage.minified_size
            # Update Image.minified_size
            image.minified_size = original_image.file.size
            original_image.file_size = original_image.file.size
            # Update WagtailTinyPNGImage.date_minified
            image.date_minified = timezone.now()
            # Save WagtailTinyPNGImage
            image.save()

            # Re-save the width and height in case there was a TinyPNG resize
            original_image.height = original_image.file.height
            original_image.width = original_image.file.width
            original_image.save()

            # Lastly, remove existing image rendiditions that might be using the bloated (old) image
            # By recreating image renditions the smaller (thumbnailed) versions of the images will also shrink
            # Taking this approach means we don't need to shrink every image rendition, we can simply compress the
            # main image, and that event will cascade to all other image variations.
            original_image.renditions.all().delete()

            percent = 100 - round(image.minified_size / image.original_size * 100)
            messages.success(
                request,
                "Image minified. You've saved {}%! You have used {} compressions this month.".format(
                    percent, tinify.compression_count
                ),
            )
        except tinify.AccountError as e:
            messages.warning(request, "TinyPNG account error. {}".format(e.message))
        except tinify.ServerError as e:
            messages.error(request, "TinyPNG.com server error. {}".format(e.message))
        except tinify.ConnectionError as e:
            messages.error(
                request, "TinyPNG.com connection error. {}".format(e.message)
            )
        except tinify.ClientError as e:
            messages.warning(
                request, "TinyPNG.com connection error. {}".format(e.message)
            )
        except tinify.Error as e:
            messages.error(request, "Compression error. {}".format(e.message))
        except Exception as e:
            if settings.DEBUG:
                # Local debugging
                exception_type = type(e)
                print(exception_type)
            messages.error(request, "Compression error. {}".format(e.message))

        return redirect(image_url)

    def get(self, request, *args, **kwargs):
        """If GET request, redirect back to the image edit page."""
        image_url = reverse("wagtailimages:edit", args=(kwargs["pk"],))
        return redirect(image_url)
