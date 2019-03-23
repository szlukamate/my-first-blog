from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
#from .forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from array import *
import json
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
# import pdb;
# pdb.set_trace()

def emailform(request, pk):
        if request.method == "POST":
                fieldvalue = request.POST['fieldvalue']
                rowid = request.POST['rowid']
                docid = request.POST['docid']
                fieldname = request.POST['fieldname']
                tbl = request.POST['tbl']

                if tbl == "tblDoc_details":
                        # not possible
                        nop
                elif tbl == "tblDoc":
                        cursor8 = connection.cursor()
                        sqlquery = "UPDATE quotation_tbldoc SET " + fieldname + "= '" + fieldvalue + "' WHERE Docid_tblDoc =" + docid
                        cursor8.execute(sqlquery)

                        cursor9 = connection.cursor()
                        cursor9.execute("SELECT " + fieldname + " "
                                                                "FROM quotation_tbldoc "
                                                                "WHERE Docid_tblDoc = %s ", [docid])
                        results = cursor9.fetchall()
                        #import pdb;
                        #pdb.set_trace()

                        json_data = json.dumps(results)

                        return HttpResponse(json_data, content_type="application/json")

        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tblDoc, "
                        "Contactid_tblDoc_id, "
                        "Doc_kindid_tblDoc_id, "
                        "companyname_tblcompanies_ctbldoc, "
                        "firstname_tblcontacts_ctbldoc, "
                        "lastname_tblcontacts_ctbldoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbldoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
                        "prefacespecforquotation_tbldoc, "
                        "subject_tbldoc, "
                        "docnumber_tbldoc, "
                        "creatorid_tbldoc, "
                        "creationtime_tbldoc, "
                        "title_tblcontacts_ctbldoc, "
                        "mobile_tblcontacts_ctbldoc, "
                        "email_tblcontacts_ctbldoc, "
                        "pcd_tblcompanies_ctbldoc, "
                        "town_tblcompanies_ctbldoc, "
                        "address_tblcompanies_ctbldoc, "
                        "total_tbldoc, "
                        "deliverydays_tbldoc, "
                        "paymenttextforquotation_tblpayment_ctbldoc, "
                        "currencycodeinreport_tbldoc, "
                        "currencyrateinreport_tbldoc, "
                        "pretag_tbldockind, "
                        "debitaccountid_tbldoc, "
                        "creditaccountid_tbldoc, "
                        "accountvalue_tbldoc, "
                        "accountduedate_tbldoc "
                        "FROM quotation_tbldoc "
                        "JOIN quotation_tbldoc_kind "
                        "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                        "WHERE docid_tbldoc=%s ",
                        [pk])

        doc = cursor1.fetchall()
        for x in doc:
                creatorid = x[11]
                debitaccountid = x[25]
                creditaccountid = x[26]

        cursor10 = connection.cursor()
        cursor10.execute("SELECT id, "
                         "first_name, "
                         "last_name, "
                         "email, "
                         "subscriptiontext_tblauth_user "
                         "FROM auth_user "
                         "WHERE id=%s ", [creatorid])
        creatordata = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT accountid_tblchartofaccounts, "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts")
        chartofaccounts = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts "
                         "WHERE accountid_tblchartofaccounts=%s",
                         [debitaccountid])
        debitaccountname = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts "
                         "WHERE accountid_tblchartofaccounts=%s",
                         [creditaccountid])
        creditaccountname = cursor10.fetchall()


        return render(request, 'quotation/accountentry.html', {'doc': doc,
                                                        'chartofaccounts': chartofaccounts,
                                                        'debitaccountname': debitaccountname,
                                                        'creditaccountname': creditaccountname,
                                                        'creatordata': creatordata})
def emailadd (request):


    #subject = 'Thank you for registering to our site'
    #message = ' it  means a world to us '
    #email_from = 'g@g.gg'
    #recipient_list = ['szluka.mate@gmail.com', ]
    #attach_file('/home/szluka/djangogirls/output.pdf')
    #send_mail(subject, message, email_from, recipient_list)

    email = EmailMessage(
        'Subject here', 'Here is the message.', 'from@me.com', ['szluka.mate@gmail.com'])
    email.attach_file('/home/szluka/djangogirls/output.pdf')
    email.send()

    '''
    fieldvalue = request.POST['fieldvalue']
    docid = request.POST['entrydocid']
    fieldnameto = request.POST['fieldnameto'] # i.e. defaultprefaceidforquotation_tblcompanies

    cursor22 = connection.cursor()
    cursor22.callproc("spentryuniversalselections",[fieldnameto,fieldvalue,docid])
    results23 = cursor22.fetchall()
    print(results23)

    json_data = json.dumps(results23)

    return HttpResponse(json_data, content_type="application/json")

    def emailform (request, pk):
        if request.method == "POST":
            fieldvalue = request.POST['fieldvalue']
            rowid = request.POST['rowid']
            docid = request.POST['docid']
            fieldname = request.POST['fieldname']
            tbl = request.POST['tbl']

            if tbl == "tblDoc_details":
                # not possible
                nop
            elif tbl == "tblDoc":
                cursor8 = connection.cursor()
                sqlquery = "UPDATE quotation_tbldoc SET " + fieldname + "= '" + fieldvalue + "' WHERE Docid_tblDoc =" + docid
                cursor8.execute(sqlquery)

                cursor9 = connection.cursor()
                cursor9.execute("SELECT " + fieldname + " "
                                                        "FROM quotation_tbldoc "
                                                        "WHERE Docid_tblDoc = %s ", [docid])
                results = cursor9.fetchall()
                # import pdb;
                # pdb.set_trace()

                json_data = json.dumps(results)

                return HttpResponse(json_data, content_type="application/json")

        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tblDoc, "
                        "Contactid_tblDoc_id, "
                        "Doc_kindid_tblDoc_id, "
                        "companyname_tblcompanies_ctbldoc, "
                        "firstname_tblcontacts_ctbldoc, "
                        "lastname_tblcontacts_ctbldoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbldoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
                        "prefacespecforquotation_tbldoc, "
                        "subject_tbldoc, "
                        "docnumber_tbldoc, "
                        "creatorid_tbldoc, "
                        "creationtime_tbldoc, "
                        "title_tblcontacts_ctbldoc, "
                        "mobile_tblcontacts_ctbldoc, "
                        "email_tblcontacts_ctbldoc, "
                        "pcd_tblcompanies_ctbldoc, "
                        "town_tblcompanies_ctbldoc, "
                        "address_tblcompanies_ctbldoc, "
                        "total_tbldoc, "
                        "deliverydays_tbldoc, "
                        "paymenttextforquotation_tblpayment_ctbldoc, "
                        "currencycodeinreport_tbldoc, "
                        "currencyrateinreport_tbldoc, "
                        "pretag_tbldockind, "
                        "debitaccountid_tbldoc, "
                        "creditaccountid_tbldoc, "
                        "accountvalue_tbldoc, "
                        "accountduedate_tbldoc "
                        "FROM quotation_tbldoc "
                        "JOIN quotation_tbldoc_kind "
                        "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                        "WHERE docid_tbldoc=%s ",
                        [pk])

        doc = cursor1.fetchall()
        for x in doc:
            creatorid = x[11]
            debitaccountid = x[25]
            creditaccountid = x[26]

        cursor10 = connection.cursor()
        cursor10.execute("SELECT id, "
                         "first_name, "
                         "last_name, "
                         "email, "
                         "subscriptiontext_tblauth_user "
                         "FROM auth_user "
                         "WHERE id=%s ", [creatorid])
        creatordata = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT accountid_tblchartofaccounts, "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts")
        chartofaccounts = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts "
                         "WHERE accountid_tblchartofaccounts=%s",
                         [debitaccountid])
        debitaccountname = cursor10.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT "
                         "nameHU_tblchartofaccounts "
                         "FROM quotation_tblchartofaccounts "
                         "WHERE accountid_tblchartofaccounts=%s",
                         [creditaccountid])
        creditaccountname = cursor10.fetchall()

        return render(request, 'quotation/accountentry.html', {'doc': doc,
                                                               'chartofaccounts': chartofaccounts,
                                                               'debitaccountname': debitaccountname,
                                                               'creditaccountname': creditaccountname,
                                                               'creatordata': creatordata})
    '''
    return redirect('quotationform', pk=60)