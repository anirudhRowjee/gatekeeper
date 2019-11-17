from django.shortcuts import render
from . import models as passes
from student import models as student
from utils import models as utils
from utils import helpers as helpers
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

def normalize_students(queryset):
    # function to accept queryset and convert to JSON
    return {str(student): str(student.unique_id) for student in queryset}


def normalize_dates(queryset):
    # function to accept queryset and convert to JSON
    return {str(date.date_name): str(date.id) for date in queryset}


def register(request):
    if request.method == "POST":
        data = request.POST
        name = data['name']
        email = data['email']
        UID = data['uid']
        event_id = data['event-date']

        # get related foreign key objects
        try:
            student_new = student.student.objects.get(unique_id=UID)
            event = utils.date.objects.get(id=event_id)
            # generate barcode object
            new_barcode = utils.barcode(
                uid = helpers.gen_UID()
            )
            new_barcode.save()
            new_barcode.set_barcode_image()

            new_pass = passes.guestPass(
                guestname=name,
                email=email,
                date_valid=event,
                guest_of=student_new,
                barcode=new_barcode
            )
            new_pass.save()
        except ObjectDoesNotExist:
            error = "Student/Event doesnt exist. Choose the right options"
            return render(request, 'passes/register.html', {'error': error})
        
        message = {'type': 'success or fail', 'message': 'what happened'}
        students = student.student.objects.all()
        students = normalize_students(students)
        dates = utils.date.objects.all()
        dates = normalize_dates(dates)
        return render(request, 'passes/register.html', {'dates': dates, 'students': students})

    else:
        # pack students for JS-based live search
        try:
            students = student.student.objects.all()
            students = normalize_students(students)
            dates = utils.date.objects.all()
            dates = normalize_dates(dates)
        except:
            error = "Students/Events are empty."
            return render(request, 'passes/register.html', {'error': error})
        return render(request, 'passes/register.html', {'dates': dates, 'students': students})
