from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
#from .forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
# import pdb;
# pdb.set_trace()

def coredata_prefaceforquotation(request):
        if request.method == "POST":
                prefaceid = request.POST['prefaceid']
                prefacename = request.POST['prefacename']
                prefacetext = request.POST['prefacetext']
                cursor1 = connection.cursor()
                cursor1.execute(

                "UPDATE quotation_tblprefaceforquotation SET "
                "prefacenameforquotation_tblprefaceforquotation=%s, "
                "prefacetextforquotation_tblprefaceforquotation=%s "
                "WHERE prefaceidforquotation_tblprefaceforquotation =%s ", [prefacename, prefacetext, prefaceid])

        cursor3 = connection.cursor()
        cursor3.execute(
                "SELECT "
                "prefaceidforquotation_tblprefaceforquotation, "
                "prefacenameforquotation_tblprefaceforquotation, "
                "prefacetextforquotation_tblprefaceforquotation "
                "FROM quotation_tblprefaceforquotation ")


        prefacesforquotation = cursor3.fetchall()

        return render(request, 'quotation/prefaceforquotation.html', {'prefacesforquotation': prefacesforquotation })
