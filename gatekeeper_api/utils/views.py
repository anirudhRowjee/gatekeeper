from django.shortcuts import render,redirect
from . import models as utils
# Create your views here.

def registerdate(request):
    if request.method == "POST":
        data = request.POST
        event_name = data['name']
        date = data['date']
        new_event = utils.date(date_name=event_name,date=date)
        new_event.save()
        return render(request, 'utils/date.html')
    else:
        return render(request, "utils/date.html")