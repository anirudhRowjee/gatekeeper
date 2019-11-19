from django.shortcuts import render
from . import models as passes
from student import models as student
from utils import models as utils
from utils import helpers as helpers
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


def normalize_students(queryset):
    # function to accept queryset and convert to JSON
    return {str(student): str(student.unique_id) for student in queryset}


def normalize_dates(queryset):
    # function to accept queryset and convert to JSON
    return {str(date.date_name): str(date.id) for date in queryset}


def sendpass(guestpass):
    template = '''
    <html>
        <body>
        <center>
            <h1> FREEDOM INTERNATIONAL SCHOOL </h1>
            <h2> GUEST PASS FOR {event} </h2>
            <h3 style='color:red;'> ( VALID ONLY FOR {event.date} ) </h3>
            <h2> PASS CATEGORY {category} </h2>
            <h2> GUEST NAME : {guestname} </h2>
            <h2> GUEST OF : {guestofname} - {guestofclass} </h2>
            <h2> PASSCODE {passcode} </h2>
            <h3> PLEASE FIND THE PASS ATTACHED BELOW. KEEP THIS IMAGE SAFE </h3>
            <h3> PRESENT THIS CODE AT THE ENTRY GATE TO BE ADMITTED. </h3>
        </center>
        </body>
    </html>
    '''
    subject = 'GUEST PASS {passcode} - FIS ANNUAL DAY'.format(
        passcode=guestpass.barcode.uid)
    message = ''

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [guestpass.email, ]
    barcode_url = 'media/media/barcodes/barcodes_staging/{}.png'.format(
        str(guestpass.barcode.uid))
    final_message = template.format(
        passcode=guestpass.barcode.uid,
        barcode_url=barcode_url,
        event=guestpass.date_valid,
        category=guestpass.category,
        guestname=guestpass.guestname,
        guestofname=guestpass.guest_of.name,
        guestofclass=guestpass.guest_of.student_class
    )
    test_mail = EmailMessage(subject, final_message,
                             email_from, recipient_list)
    test_mail.content_subtype = 'html'
    test_mail.attach_file(barcode_url)
    test_mail.send(fail_silently=False)


def register(request):
    if request.method == "POST":
        data = request.POST
        name = data['name']
        email = data['email']
        UID = data['uid']
        event_id = data['event-date']
        paid = False
        if 'paid' in data.keys():
            paid = True
        category = data['category']

        # get related foreign key objects
        try:
            student_new = student.student.objects.get(unique_id=UID)
            event = utils.date.objects.get(id=event_id)
            category_obj = passes.category.objects.get(id=category)
            # generate barcode object
            new_barcode = utils.barcode(
                uid=helpers.gen_UID()
            )
            new_barcode.save()
            new_barcode.set_barcode_image()

            new_pass = passes.guestPass(
                guestname=name,
                email=email,
                date_valid=event,
                guest_of=student_new,
                barcode=new_barcode,
                category=category_obj,
                paid=paid,
            )
            new_pass.save()
        except ObjectDoesNotExist:
            error = "Student/Event doesnt exist. Choose the right options"
            return render(request, 'passes/register.html', {'message': error, 'status': 'OK'})

        message = {'type': 'success or fail', 'message': 'what happened'}
        students = student.student.objects.all()
        students = normalize_students(students)
        dates = utils.date.objects.all()
        dates = normalize_dates(dates)
        sendpass(new_pass)
        categories = passes.category.objects.all()
        return render(request, 'passes/register.html', {'dates': dates, 'students': students,
                                                        'status': 'OK', 'message': "New pass {pass_meta} generated".format(pass_meta=str(new_pass)),
                                                        'categories': categories,
                                                        })

    else:
        # pack students for JS-based live search
        try:
            students = student.student.objects.all()
            students = normalize_students(students)
            dates = utils.date.objects.all()
            dates = normalize_dates(dates)
            categories = passes.category.objects.all()
        except:
            error = "Students/Events are empty."
            return render(request, 'passes/register.html', {'error': error})
        return render(request, 'passes/register.html', {'dates': dates, 'students': students, 'categories': categories})


def validate(request):
    return render(request, 'passes/checkin.html')
