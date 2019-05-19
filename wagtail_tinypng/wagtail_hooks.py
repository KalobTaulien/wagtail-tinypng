from django.conf import settings
from django.urls import path, reverse
from django.utils.translation import ugettext as _
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .models import WagtailTinyPNGImage
from .views import TinifyPNG


@hooks.register("register_admin_urls")
def urlconf_time():
    """Add the form url to the Wagtail admin URLs."""
    return [path("tinify/<int:pk>/", TinifyPNG.as_view(), name="tinify_form")]
    
if 'wagtail.contrib.modeladmin' in settings.INSTALLED_APPS:
    class WagtailTinypngButtonHelper(ButtonHelper):
        def add_button(self, classnames_add=None, classnames_exclude=None):
            if classnames_add is None:
                classnames_add = []
            if classnames_exclude is None:
                classnames_exclude = []
            classnames = self.add_button_classnames + classnames_add
            cn = self.finalise_classname(classnames, classnames_exclude)
            return {
                "url": reverse("wagtailimages:add_multiple"),
                "label": _("Add image"),
                "classname": cn,
                "title": _("Add a new image"),
            }

        def edit_button(self, pk, classnames_add=None, classnames_exclude=None):
            if classnames_add is None:
                classnames_add = []
            if classnames_exclude is None:
                classnames_exclude = []
            classnames = self.edit_button_classnames + classnames_add
            cn = self.finalise_classname(classnames, classnames_exclude)
            image = WagtailTinyPNGImage.objects.get(pk=pk)

            return {
                "url": reverse("wagtailimages:edit", args=(image.wagtail_image_id,)),
                "label": _("Edit"),
                "classname": cn,
                "title": _("Edit this %s") % self.verbose_name,
            }

        def delete_button(self, pk, classnames_add=None, classnames_exclude=None):
            if classnames_add is None:
                classnames_add = []
            if classnames_exclude is None:
                classnames_exclude = []
            classnames = self.delete_button_classnames + classnames_add
            cn = self.finalise_classname(classnames, classnames_exclude)
            image = WagtailTinyPNGImage.objects.get(pk=pk)
            return {
                "url": reverse("wagtailimages:delete", args=(image.wagtail_image_id,)),
                "label": _("Delete"),
                "classname": cn,
                "title": _("Delete this %s") % self.verbose_name,
            }


    @modeladmin_register
    class WagtailTinyPNGImageAdmin(ModelAdmin):
        model = WagtailTinyPNGImage
        menu_label = "Compressed Images"
        menu_icon = "image"
        menu_order = 800
        add_to_settings_menu = True
        exclude_from_explorer = True
        inspect_view_enabled = True
        list_display = (
            "wagtail_image",
            "is_minified",
            "display_original_size",
            "display_minified_size",
            "savings",
            "date_minified",
        )
        ordering = ("wagtail_image__created_at",)
        button_helper_class = WagtailTinypngButtonHelper
