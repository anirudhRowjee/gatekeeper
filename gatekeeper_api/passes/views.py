from django.shortcuts import render
from . import models as passes
from student import models as student
from utils import models as utils
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def normalize_students(queryset):
    # function to accept queryset and convert to JSON
    return {student: str(student.unique_id) for student in queryset}


def normalize_dates(queryset):
    # function to accept queryset and convert to JSON
    return {date: str(date.id) for date in queryset}


def register(request):
    if request.method == "POST":
        data = request.POST
        name = data['name']
        email = data['email']
        UID = data['uid']
        event_id = data['event']

        # get related foreign key objects
        try:
            student_new = student.student.get(unique_id=UID)
            event = utils.date.get(id=event_id)
        except ObjectDoesNotExist:
            # throw error
            pass

        # create object
        try:
            new_pass = passes.guestPass(
                guestname=name,
                email=email,
                date_valid=event,
                guest_of=student_new
            )
        except IntegrityError:
            # throw error
            pass

        message = {'type': 'success or fail', 'message': 'what happened'}
        students = student.student.objects.all()
        students = normalize_students(students)
        dates = utils.date.objects.all()
        dates = normalize_dates(dates)
        return render(request, 'passes/register.html', {'dates': dates, 'students': students})

    else:
        # pack students for JS-based live search
        students = student.student.objects.all()
        students = normalize_students(students)
        dates = utils.date.objects.all()
        dates = normalize_dates(dates)
        return render(request, 'passes/register.html', {'dates': dates, 'students': students})
