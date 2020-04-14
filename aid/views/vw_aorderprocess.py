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
def aorderprocess(request):
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                         "Productid_tblaProduct, "
                         "purchase_price_tblaproduct, "
                         "customerdescription_tblaProduct, "
                         "margin_tblaproduct, "
                         "unit_tblaproduct, "
                         "enabletoorderprocess_tblaproduct, "
                         "obsolete_tblaproduct, "
                         "currencyisocode_tblcurrency_ctblaproduct "

                         "FROM aid_tblaproduct "

                         "WHERE enabletoorderprocess_tblaproduct=1 and obsolete_tblaproduct=0 ")
        enabledproductstoorderprocess = cursor1.fetchall()

        return render(request, 'aid/aorderprocess.html', {'enabledproductstoorderprocess': enabledproductstoorderprocess})
