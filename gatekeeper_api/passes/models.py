from django.db import models

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10, default="#000000")

    def __str__(self):
        return self.name


class guestPass(models.Model):

    # model for guest passes
    barcode = models.ForeignKey('utils.barcode', on_delete=models.CASCADE) #fkey to barcode object
    date_valid = models.ForeignKey('utils.date', on_delete=models.CASCADE) #fkey to dates object
    guestname = models.CharField(max_length=100)
    email = models.EmailField()
    date_issued = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    guest_of = models.ForeignKey('student.student', on_delete=models.CASCADE) #fkey to student
    category = models.ForeignKey(category, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        datastr = "{guestname} - guest of {student}".format(guestname=self.guestname,
                                                            student = self.guest_of.name)
        return datastr


