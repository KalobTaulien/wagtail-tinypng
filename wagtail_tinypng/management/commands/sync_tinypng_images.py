from django.core.management.base import BaseCommand

from wagtail.images import get_image_model

from wagtail_tinypng.models import WagtailTinyPNGImage


class Command(BaseCommand):
    """Base command."""

    help = "Select all Wagtail Images and create a new OneToOne relationship with the WagtailTinyPNGImage model"

    def handle(self, *args, **options):
        """Execute command."""
        Image = get_image_model()
        all_images = Image.objects.all()
        total_new = 0
        total_existing = 0
        print("Looking at {} images".format(all_images.count()))
        print("------")
        for image in all_images:
            print(image.title)
            tinified_image, created = WagtailTinyPNGImage.objects.get_or_create(
                wagtail_image=image
            )
            if created:
                print("- Created a OneToOne relationship")
                total_new = total_new + 1
            else:
                print("- Existing relationship")
                total_existing = total_existing + 1
        print(
            "Done with {} new relationships and {} already existing relationships".format(
                total_new, total_existing
            )
        )
        return None
