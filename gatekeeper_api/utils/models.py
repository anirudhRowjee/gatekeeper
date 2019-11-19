from django.db import models
from django.conf import settings
from PIL import Image
from django.core.files import File
import qrcode as qrcode_lib

# Create your models here.

def get_qrcode(instr):
    # returns a qrcode image object
    qr = qrcode_lib.QRCode(
            version=3,
            error_correction=qrcode_lib.constants.ERROR_CORRECT_L,
            border=1,
            box_size=20)
    qr.add_data(instr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


class barcode(models.Model):
    uid = models.CharField(max_length=10, unique=True)
    image = models.ImageField(upload_to='media/barcodes/', blank=True)

    def __str__(self):
        return self.uid

    def set_barcode_image(self):
        # method to generate barcode and save it
        qrcode = get_qrcode(self.uid)
        print(qrcode)
        #img_object = File(open(image, 'rb'))
        self.image = File(open(qrcode._img), 'rb')
        self.save()

class date(models.Model):
    date_name = models.CharField(max_length = 100)
    date = models.DateField()

    def __str__(self):
        returnstr = "{date} - {occasion}"
        return returnstr.format(date=self.date, occasion=self.date_name)
