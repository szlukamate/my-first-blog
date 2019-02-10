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
                "prefacetextforquotation_tblprefaceforquotation, "
                "creationtime_tblprefaceforquotation "
                "FROM quotation_tblprefaceforquotation "
                "WHERE obsolete_tblprefaceforquotation =0")


        prefacesforquotation = cursor3.fetchall()

        return render(request, 'quotation/prefaceforquotation.html', {'prefacesforquotation': prefacesforquotation })

def coredata_prefaceforquotationadd(request):
        cursor1 = connection.cursor()
        cursor1.execute(
                "INSERT INTO quotation_tblprefaceforquotation (prefacenameforquotation_tblprefaceforquotation) VALUES ('New')")
        transaction.commit()

        return redirect('coredata_prefaceforquotation')
def coredata_prefaceforquotationremove(request, pk):
        cursor1 = connection.cursor()
        cursor1.execute(
                "UPDATE quotation_tblprefaceforquotation SET "
                "obsolete_tblprefaceforquotation=1 "
                "WHERE prefaceidforquotation_tblprefaceforquotation =%s ", [pk])

        transaction.commit()

        return redirect('coredata_prefaceforquotation')
def coredata_backpageforquotation(request):
        if request.method == "POST":
                backpageid = request.POST['backpageid']
                backpagename = request.POST['backpagename']
                backpagetext = request.POST['backpagetext']
                cursor1 = connection.cursor()
                cursor1.execute(

                "UPDATE quotation_tblbackpageforquotation SET "
                "backpagenameforquotation_tblbackpageforquotation=%s, "
                "backpagetextforquotation_tblbackpageforquotation=%s "
                "WHERE backpageidforquotation_tblbackpageforquotation =%s ", [backpagename, backpagetext, backpageid])

        cursor3 = connection.cursor()
        cursor3.execute(
                "SELECT "
                "backpageidforquotation_tblbackpageforquotation, "
                "backpagenameforquotation_tblbackpageforquotation, "
                "backpagetextforquotation_tblbackpageforquotation, "
                "creationtime_tblbackpageforquotation "
                "FROM quotation_tblbackpageforquotation "
                "WHERE obsolete_tblbackpageforquotation =0")


        backpagesforquotation = cursor3.fetchall()

        return render(request, 'quotation/backpageforquotation.html', {'backpagesforquotation': backpagesforquotation })
def coredata_backpageforquotationadd(request):
        cursor1 = connection.cursor()
        cursor1.execute(
                "INSERT INTO quotation_tblbackpageforquotation (backpagenameforquotation_tblbackpageforquotation) VALUES ('New')")
        transaction.commit()

        return redirect('coredata_backpageforquotation')
def coredata_backpageforquotationremove(request, pk):
        cursor1 = connection.cursor()
        cursor1.execute(
                "UPDATE quotation_tblbackpageforquotation SET "
                "obsolete_tblbackpageforquotation=1 "
                "WHERE backpageidforquotation_tblbackpageforquotation =%s ", [pk])

        transaction.commit()

        return redirect('coredata_backpageforquotation')
