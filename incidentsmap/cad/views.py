from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .enricher import Enricher

def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        enricher = Enricher(filename)
        return render(request, 'cad/index.html', {
            'uploaded_file_url': uploaded_file_url
        })
    else:
        template = loader.get_template('cad/index.html')
        context = {}
        return HttpResponse(template.render(context, request))


