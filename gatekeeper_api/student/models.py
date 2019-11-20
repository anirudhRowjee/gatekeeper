from django.db import models
from django.db import IntegrityError
import csv
# Create your models here.


def filter_duplicates(in_file):
    rows = []
    with open(in_file, 'r') as data:
        reader = csv.reader(data)
        for row in reader:
            rows.append(row)

    row_map = {row[0] : 0 for row in rows }

    for x in rows:
        row_map[x[0]] += 1

    duplicates = {x:row_map[x] for x in row_map.keys() if row_map[x] > 1}
    if len(duplicates) == 0:
        return None
    else:
        return duplicates




class student(models.Model):

    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=10)

    def __str__(self):
        return "{name} ({std_class}) - {unique_id}".format(name=self.name, unique_id=self.unique_id, std_class=self.student_class)


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

        # filter for duplicates
        status = filter_duplicates(mainfile_path)
        if status is None:
            pass
        else:
            message = "There is Duplicate Student Data! {message}".format(message=status)
            return [status, False]

        with open(mainfile_path) as data:
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                print(row)
                uid = row[0].lstrip().rstrip()
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
        if dataset[1] == False:
            # error
            errorlist = [" {admno} - {n} occurrances ".format(admno=x, n=dataset[0][x]) for x in dataset[0].keys()]
            errorstring = "DUPLICATES >> " + " | ".join(errorlist)
            return errorstring, False
        successes = 0
        total = len(dataset)
        master = []
        print("processed dump", dataset)
        for student_data in dataset:
            try:
                new = student(
                    name=student_data['name'],
                    unique_id=student_data['uid'],
                    student_class=student_data['student_class']
                )
                new.save()
                master.append(new)
                successes += 1
                print("<< Uploaded student {current} of {total} >>".format(current = successes, total = total))
            except IntegrityError:
                message = "There is Duplicate Student Data! All data has been deleted."
                for i in master:
                    i.delete()
                return [message, False]

        message = "{successes} out of {total} students successfully added"
        return [message.format(successes=successes, total=total), True]
