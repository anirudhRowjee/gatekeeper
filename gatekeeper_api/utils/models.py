from django.db import models
from django.conf import settings
from PIL import Image
from django.core.files import File
import pyqrcode
import png
import os
from django.conf import settings
# Create your models here.


def get_qrcode(instr):
    # returns a qrcode image object
    dir = os.path.join(
        settings.MEDIA_ROOT, "media/barcodes/barcodes_staging/{uid}.png".format(uid=instr))
    qr = pyqrcode.create(
        '{}'.format(instr),
        error='L',
        version=3,
        mode='binary'
    )
    img = qr.png(
        dir,
        scale=6,
        module_color=[0, 0, 0, 255],
        background=(255, 255, 255)
    )
    return img


class barcode(models.Model):
    uid = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='media/barcodes/', blank=True)

    def __str__(self):
        return self.uid

    def set_barcode_image(self):
        # method to generate barcode and save it
        qrcode = get_qrcode(self.uid)
        # img_object = File(open(image, 'rb'))
        self.image = qrcode
        self.save()


class date(models.Model):
    date_name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        returnstr = "{date} - {occasion}"
        return returnstr.format(date=self.date, occasion=self.date_name)
