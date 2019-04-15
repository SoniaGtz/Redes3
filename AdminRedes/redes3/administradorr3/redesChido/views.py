from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic.base import TemplateView
# Create your views here.
def index(request):
    response = redirect('index.html')
    return response

class HomeView(TemplateView):
    template_name = '/adminlte/index.html'
