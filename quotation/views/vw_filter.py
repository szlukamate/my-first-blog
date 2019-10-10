from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction, connections
from array import *
import simplejson as json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
import subprocess
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as x12
# import pdb;
# pdb.set_trace()
@login_required
def filtermain(request):

        filterfield = []

        # fieldname, visibility

        fieldproperties = ('customerdescription',1)
        filterfield.append(fieldproperties)

        fieldproperties = ('listprice',1)
        filterfield.append(fieldproperties)

        fieldproperties = ('currency',1)
        filterfield.append(fieldproperties)



        json_data = json.dumps(filterfield[1][0])

        return HttpResponse(json_data, content_type="application/json")
def filteraddfilteroptinsonproductform(request):

        filterfield = []

        # fieldname, visibility

        fieldproperties = ('customerdescription',1)
        filterfield.append(fieldproperties)

        fieldproperties = ('listprice',1)
        filterfield.append(fieldproperties)

        fieldproperties = ('currency',1)
        filterfield.append(fieldproperties)



        json_data = json.dumps(filterfield[1][0])

        return HttpResponse(json_data, content_type="application/json")
def filtertemplatehtmlonproductform(request):
        selectedvalue = request.POST['selectedvalue']

        return render(request, 'quotation/filtertemplatehtml.html',{'selectedvalue': selectedvalue})
