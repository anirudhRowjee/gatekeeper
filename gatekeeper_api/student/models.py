from django.db import models
from django.db import IntegrityError

# Create your models here.

class student(models.Model):

    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=10)

    def __str__(self):
        return "{name} - {unique_id}".format(name=self.name, unique_id=self.unique_id)


class StudentAdder(models.Model):
    # functions to add students from CSV files
    uid = models.CharField(max_length=20, unique=True)
    filename = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/studentlists/')
    migrated = models.DateTimeField(auto_now=True)

    def getFileDump(self):
        # get dump from CSV file in JSON
        data = {}
        mainfile_path = self.file.path
        with open(mainfile_path) as data:
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                uid, name, student_class = row[0], row[1], row[2]
                new = {'uid':uid, 'name':name, 'student_class':student_class}
                data += new
        return data

    def addStudents(self):
        # add students from JSON data dump
        dataset = self.getFileDump()
        successes = 0
        total = len(dataset)
        for student in dataset:
            try:
                new = student.objects.get_or_create(
                        name = student['name'],
                        uid = student['uid'],
                        student_class = student['student_class']
                        )
                successes += 1
            except IntegrityError:
                print("student {dump} already exists".format(dump=student))

        message =  "{successes} out of {total} students successfully added"
        return message.format(successes = successes, total = total)
