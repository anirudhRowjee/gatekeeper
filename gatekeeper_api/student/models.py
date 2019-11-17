from django.db import models
from django.db import IntegrityError
import csv
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
        dump = []
        mainfile_path = self.file.path
        with open(mainfile_path) as data:
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                print(row)
                uid = row[0]
                name = row[1]
                student_class = row[2]
                new = {'uid': uid, 'name': name,
                       'student_class': student_class}
                print("new, ", new)
                dump.append(new)
        print("Student file dump", dump)
        return dump

    def addStudents(self):
        # add students from JSON data dump
        dataset = self.getFileDump()
        successes = 0
        total = len(dataset)
        print("processed dump", dataset)
        for student_data in dataset:
            try:
                new = student(
                    name=student_data['name'],
                    unique_id=student_data['uid'],
                    student_class=student_data['student_class']
                )
                new.save()
                successes += 1
            except IntegrityError:
                message = "There is Duplicate Student Data!"
                return [message, False]

        message = "{successes} out of {total} students successfully added"
        return [message.format(successes=successes, total=total), True]
