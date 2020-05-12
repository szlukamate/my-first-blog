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
def acustomerconfirmation(request, docid):
    useremail = request.user.email
    cursor3 = connection.cursor()
    cursor3.execute("SELECT "
                    "Doc_kindid_tblaDoc_id, "
                    "docnumber_tblaDoc, "
                    "pretag_tbladockind "

                    "FROM aid_tbladoc "

                    "JOIN aid_tbladoc_kind as DK "
                    "ON Doc_kindid_tblaDoc_id = DK.Doc_kindid_tblaDoc_kind "

                    "WHERE docid_tbladoc=%s ", [docid])
    customerordernumbers = cursor3.fetchall()
    for x in customerordernumbers:
            customerordernumberdocnumber = x[1]
            customerordernumberpretag = x[2]
    customerordernumber = str(customerordernumberpretag) + str(customerordernumberdocnumber)

    return render(request, 'aid/acustomerconfirmation.html', {'customerordernumber': customerordernumber, 'useremail': useremail})
