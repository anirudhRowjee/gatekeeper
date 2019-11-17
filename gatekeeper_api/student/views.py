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
            uid=uid,
            filename=str(uid),
            file=csv_file)
        adder.save()
        message = adder.addStudents()
        print("message ", message)
        message_actual = message[0]
        if message[1] == True:
            status = 'OK'
        if message[1] == False:
            status = 'NO'
        return render(request, "student/addstudents.html", {'message':message_actual, 'status':status })

    else:
        return render(request, "student/addstudents.html")
