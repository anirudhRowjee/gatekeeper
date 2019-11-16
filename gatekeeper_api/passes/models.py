from django.db import models

# Create your models here.

class guestPass(models.Model):

    # model for guest passes

    barcode = models.ForeignKey() #fkey to barcode object
    date_valid = models.ForeignKey() #fkey to dates object
    guestname = models.CharField(max_length=100)
    email = models.EmailField()
    date_issued = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    guest_of = models.ForeignKey() #fkey to student

    def __str__(self):
        datastr = "{guestname} - guest of {student}".format(guestname=self.guestname,
                                                            student = self.guest_of.name)
