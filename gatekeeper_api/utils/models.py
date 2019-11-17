from django.db import models
import barcode as barcode_lib
from django.conf import settings
from PIL import Image
from django.core.files import File

# Create your models here.

def get_code128_barcode(instr):
    # returns a barcode image object
    code128 = barcode_lib.get_barcode_class('code128')
    barcode_object = code128(instr)
    return barcode_object


class barcode(models.Model):
    uid = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='media/barcodes/', blank=True)

    def __str__(self):
        return self.uid

    def set_barcode_image(self):
        # method to generate barcode and save it
        barcode = get_code128_barcode(self.uid)
        image = barcode.save("barcodes_staging/{name}".format(name=str(self.uid)))
        img_object = File(open(image, 'rb'))
        self.image = img_object
        self.save()

class date(models.Model):
    date_name = models.CharField(max_length = 100)
    date = models.DateField()

    def __str__(self):
        returnstr = "{date} - {occasion}"
        return returnstr.format(date=self.date, occasion=self.date_name)
