from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from . import models as passes
from student import models as student
from utils import models as utils
from utils import helpers as helpers
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response


def normalize_students(queryset):
    # function to accept queryset and convert to JSON
    return {str(student): str(student.unique_id) for student in queryset}


def normalize_dates(queryset):
    # function to accept queryset and convert to JSON
    return {str(date.date_name): str(date.id) for date in queryset}


def normalize_guests(queryset):
    # function to accept queryset and convert to JSON
    return {str(guest.guestname): {'id': str(guest.id), 'guest_of': str(guest.guest_of)} for guest in queryset}


def sendpass(guestpass):
    template = '''
    <html>
        <body>
        <center>
            <h1> FREEDOM INTERNATIONAL SCHOOL </h1>
            <h2> GUEST PASS FOR {event} </h2>
            <h3 style='color:red;'> ( VALID ONLY FOR {event.date} ) </h3>
            <h2> PASS CATEGORY :<div style='background-color:{passcolor};'> {category} </div> </h2>
            <h2> GUEST NAME : {guestname} </h2>
            <h2> GUEST OF : {guest_student}</h2>
            <h2> PASSCODE : {passcode} </h2>
            <h3 style='color:red;'> PLEASE FIND THE PASS ATTACHED BELOW. KEEP THIS IMAGE SAFE </h3>
            <h3 style='color:red;'> PRESENT THIS CODE AT THE ENTRY GATE TO BE ADMITTED. </h3>
        </center>
        </body>
    </html>
    '''
    subject = 'GUEST PASS {passcode} - FIS {event}'.format(
        passcode=guestpass.barcode.uid,
        event=guestpass.date_valid.date_name,)
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
        guest_student = str(guestpass.guest_of),
        passcolor = guestpass.category.color,
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


def get_guest_info(request):
    if request.method == "POST":
        if 'uid' in request.POST.keys():
            try:
                uid = request.POST['uid']
                if uid == '' or len(uid) != 12 or uid.isalpha() or uid.isdigit() :
                    return JsonResponse({'error':'invalid'})
                print(uid)
                barcode = utils.barcode.objects.get(
                    uid=uid)
                guestpass = passes.guestPass.objects.get(barcode=barcode)
                student_id = guestpass.guest_of.id
                studentdata = student.student.objects.get(id=student_id)
                pass_category = model_to_dict(guestpass.category)
                data = model_to_dict(studentdata)
                #data.update(model_to_dict(guestpass))
                data.update({'uid': guestpass.barcode.uid,
                            'guest_of': str(guestpass.guest_of), 'guestpass':model_to_dict(guestpass),
                            'event': str(guestpass.date_valid),
                             'guest_id': guestpass.id, 'category':pass_category})
                return JsonResponse(data)
            except:
                return JsonResponse({'error': 'QR CODE DOESNT EXIST'})
        elif 'checkinid' in request.POST.keys():
            guest_id = request.POST['checkinid']
            print(guest_id)
            guestpass = passes.guestPass.objects.get(id=guest_id)
            if guestpass.checked_in == True:
                # guest has already checked in
                guestpass.checked_in = False
                guestpass.save()
            else:
                # guest has checked out
                guestpass.checked_in = True
                guestpass.save()
            # sending back checked_in data
            return JsonResponse({'checked_in': guestpass.checked_in})


def home(request):
    if request.method == "POST":
        guest_id = request.POST['guest']
        guest_obj = passes.guestPass.objects.get(id=guest_id)
        data = model_to_dict(guest_obj)
        student_id = guest_obj.guest_of.id
        studentdata = student.student.objects.get(id=student_id)
        data.update(model_to_dict(studentdata))
        data.update({'uid': guest_obj.barcode.uid, 'guest_id': guest_obj.id})
        return JsonResponse(data)
    else:
        guests = normalize_guests(passes.guestPass.objects.all())
        return render(request, 'passes/home.html', {'guests': guests})
