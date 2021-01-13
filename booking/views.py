from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from .models import Barber 
from .forms import NewClientForm
import json 

# Create your views here.
def index(request):
    return render(request, "main/index.html")

class Barbers(ListView):
    model = Barber
    context_object_name = 'barbers'

class Barber_schedule(DetailView):
    model = Barber
    context_object_name = 'barber'

def detail(request, pk):
    barber = Barber.objects.get(id = pk)
    # parse your json to objects
    schedule = json.dumps(barber.schedule)
    new_client_form = NewClientForm()

    context = {
        'schedule': schedule,
        'barber': barber, 
        'new_client_form': new_client_form, 
        }
    try: 
        if(request.session['confirmed']):   
            update_context = {
                'confirmed': True,
            }      
            context.update(update_context)
            request.session['confirmed'] = False
    except:
        pass
    
    return render(request, 'booking/barber_detail.html', context)

def add_client(request):
    if request.method == 'POST':
        form = NewClientForm(request.POST)
        if form.is_valid():
            form.save()
        request.session['confirmed'] = True 
        return HttpResponseRedirect('/barbers/' + request.POST['barber'])
    return HttpResponseRedirect('/')