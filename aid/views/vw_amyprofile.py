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
def amyprofileform(request, pk):
    useridnow = request.user.id

    if request.method == "POST":
            fieldvalue = request.POST['fieldvalue']
            rowid = request.POST['rowid']
            fieldname = request.POST['fieldname']

            cursor22 = connection.cursor()
            cursor22.callproc("spmyprofileformfieldsupdate", [fieldname, fieldvalue, rowid])
            results23 = cursor22.fetchall()
            print(results23)

            json_data = json.dumps(results23)

            return HttpResponse(json_data, content_type="application/json")
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT "
        "id, "
        "username, "
        "email "
        
        "FROM auth_user "

        "WHERE id=%s ",
        [pk])
    usernowrowfromtable = cursor0.fetchall()
    #import pdb;
    #pdb.set_trace()

    #        for instancesingle in particularcompany:
#            id = instancesingle[0]
#            email = instancesingle[1]
#            email = instancesingle[1]

    return render(request, 'aid/amyprofile.html', {'usernowrowfromtable': usernowrowfromtable })
