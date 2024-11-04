from django.db import models
from .constants import CARGO_TRACKING_URLS

class Cargo(models.Model):
    carrier_name = models.CharField(max_length=100, verbose_name="Kargo Adı")
    tracking_number = models.CharField(max_length=50, verbose_name="Takip Numarası")

    def get_tracking_url(self):
        # Sabit URL şablonlarını kullanarak takip URL'sini oluştur
        url_template = CARGO_TRACKING_URLS.get(self.carrier_name)
        if url_template:
            return url_template.format(tracking_no=self.tracking_number)
        return None

    def __str__(self):
        return f"{self.carrier_name} - {self.tracking_number}"