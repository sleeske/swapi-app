from typing import Collection

from django.db import models
from django.utils.translation import gettext_lazy as _


class Collection(models.Model):
    csv_file = models.FileField(_("csv file"), upload_to="collections")
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")
        ordering = ("-created",)

