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
def coredata_payment(request):
        if request.method == "POST":
                paymentid = request.POST['paymentid']
                paymentname = request.POST['paymentname']
                paymenttext = request.POST['paymenttext']
                cursor1 = connection.cursor()
                cursor1.execute(

                "UPDATE quotation_tblpayment SET "
                "paymentname_tblpayment=%s, "
                "paymenttextforquotation_tblpayment=%s "
                "WHERE paymentid_tblpayment =%s ", [paymentname, paymenttext, paymentid])

        cursor3 = connection.cursor()
        cursor3.execute(
                "SELECT "
                "paymentid_tblpayment, "
                "paymentname_tblpayment, "
                "paymenttextforquotation_tblpayment, "
                "creationtime_tblpayment "
                "FROM quotation_tblpayment "
                "WHERE obsolete_tblpayment =0")


        payments = cursor3.fetchall()

        return render(request, 'quotation/payment.html', {'payments': payments })
def coredata_paymentadd(request):
        cursor1 = connection.cursor()
        cursor1.execute(
                "INSERT INTO quotation_tblpayment (paymentname_tblpayment) VALUES ('New')")
        transaction.commit()

        return redirect('coredata_payment')
def coredata_paymentremove(request, pk):
        cursor1 = connection.cursor()
        cursor1.execute(
                "UPDATE quotation_tblpayment SET "
                "obsolete_tblpayment=1 "
                "WHERE paymentid_tblpayment =%s ", [pk])

        transaction.commit()

        return redirect('coredata_payment')
def coredata_currency(request):
        if request.method == "POST":
                currencyid = request.POST['currencyid']
                currencyisocode = request.POST['currencyisocode']
                currencydescription = request.POST['currencydescription']
                currencyrate = request.POST['currencyrate']

                cursor1 = connection.cursor()
                cursor1.execute(

                "UPDATE quotation_tblcurrency SET "
                "currencyisocode_tblcurrency=%s, "
                "currencydescription_tblcurrency=%s, "
                "currencyrate_tblcurrency=%s "
                "WHERE currencyid_tblcurrency =%s ", [currencyisocode, currencydescription, currencyrate, currencyid])

        cursor3 = connection.cursor()
        cursor3.execute(
                "SELECT "
                "currencyid_tblcurrency, "
                "currencyisocode_tblcurrency, "
                "currencydescription_tblcurrency, "
                "currencyrate_tblcurrency, "
                "creationtime_tblcurrency "
                "FROM quotation_tblcurrency "
                "WHERE obsolete_tblcurrency =0")


        currencys = cursor3.fetchall()

        return render(request, 'quotation/currency.html', {'currencys': currencys })
def coredata_currencyadd(request):
        cursor1 = connection.cursor()
        cursor1.execute(
                "INSERT INTO quotation_tblcurrency (currencydescription_tblcurrency) VALUES ('New')")
        transaction.commit()

        return redirect('coredata_currency')
def coredata_currencyremove(request, pk):
        cursor1 = connection.cursor()
        cursor1.execute(
                "UPDATE quotation_tblcurrency SET "
                "obsolete_tblcurrency=1 "
                "WHERE currencyid_tblcurrency =%s ", [pk])

        transaction.commit()

        return redirect('coredata_currency')
