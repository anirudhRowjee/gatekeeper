from django.shortcuts import render
import csv
import uuid
from . import models as passes
from student import models as student
from utils import models as utils
# Create your views here.


def get_unique_id():
    new = uuid.uuid4()
    return str(new).split('-')[-1]


def AddStudents(request):
    if request.method == "POST":
        # get CSV file
        csv_file = request.FILES['students-csv']
        uid = get_unique_id()
        adder = student.StudentAdder(
            uid=uid, filename=str(uid), file=csv_file)
        adder.save()
        adder.addStudents()

    else:
        return render(request, "student/addstudents.html")
