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
from django.core.files.storage import FileSystemStorage

# import pdb;
# pdb.set_trace()

def emailadd (request, pk):
    creatorid = request.user.id

    cursor0 = connection.cursor()
    cursor0.execute("SELECT "
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
                    "accountcurrencycode_tbldoc "

                    "FROM quotation_tbldoc "
                    "WHERE docid_tbldoc=%s "
                    "order by docid_tbldoc desc",
                    [pk])
    doc = cursor0.fetchall()
    for instancesingle in doc:
        contactidclone = instancesingle[1]
        companynameclone = instancesingle[3]
        firstnameclone = instancesingle[4]
        lastnameclone = instancesingle[5]
        creatoridclone = instancesingle[11]
        titleclone = instancesingle[13]
        mobileclone = instancesingle[14]
        emailclone = instancesingle[15]
        pcdclone = instancesingle[16]
        townclone = instancesingle[17]
        addressclone = instancesingle[18]

    #import pdb;
    #pdb.set_trace()

    cursor8 = connection.cursor()
    cursor8.execute("SELECT max(docnumber_tblDoc) FROM quotation_tbldoc "
                    "WHERE Doc_kindid_tblDoc_id = 5")
    results = cursor8.fetchall()

    if results[0][0] is not None: # only if there is not doc yet (this would be the first instance)
        for x in results:
            docnumber = x[0]
            docnumber += 1
    else:
            docnumber = 80 # arbitrary number

    cursor = connection.cursor()
    cursor.execute("SELECT  quotation_tbldoc_kind.Doc_kindid_tbldoc_kind, "
                   "quotation_tbldoc_kind.Doc_kind_name_tblDoc_kind, "
                   "quotation_tbldoc_kind.pretag_tbldockind, "
                   "quotation_tbldoc.subject_tbldoc, "
                   "quotation_tbldoc.docnumber_tbldoc "
                   "FROM quotation_tbldoc "
                   "JOIN quotation_tbldoc_kind "
                   "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                   "WHERE quotation_tbldoc.docid_tbldoc=%s ", [pk])
    results = cursor.fetchall()
    for x in results:
        dockindname = x[1]
        pretag = x[2]
        originaldocsubject = x[3]
        originaldocnumber = x[4]




    #import pdb;
    #pdb.set_trace()

    emailsubject="Customer Quotation - Subject: " + originaldocsubject + " - Ref.: " + pretag + str(originaldocnumber) + " EMAIL-" + str(docnumber)
    addresseeemail = request.POST['addresseeemail']
    cc = request.POST['cc']
    pdffilename = request.POST['pdffilename']
    emailbodytextmodifiedbyuser = request.POST['emailbodytext']

    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO quotation_tbldoc "
                    "( Doc_kindid_tblDoc_id, "
                    "Contactid_tblDoc_id,"
                    "companyname_tblcompanies_ctbldoc, "
                    "firstname_tblcontacts_ctbldoc, "
                    "lastname_tblcontacts_ctbldoc, "
                    "docnumber_tblDoc, "
                    "creatorid_tbldoc, "
                    "title_tblcontacts_ctbldoc, "
                    "mobile_tblcontacts_ctbldoc, "
                    "email_tblcontacts_ctbldoc, "
                    "pcd_tblcompanies_ctbldoc, "
                    "town_tblcompanies_ctbldoc, "
                    "address_tblcompanies_ctbldoc, "
                    "doclinkparentid_tbldoc, "
                    "subject_tbldoc, "
                    "emailbodytextmodifiedbyuser_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [5, contactidclone, companynameclone, firstnameclone, lastnameclone, docnumber, creatorid,
                    titleclone,
                    mobileclone,
                    emailclone,
                    pcdclone,
                    townclone,
                    addressclone,
                    pk,
                    emailsubject,
                    emailbodytextmodifiedbyuser])

    cursor3 = connection.cursor()
    cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
    results = cursor3.fetchall()
    for x in results:
        maxdocid = x[0]


    def pdfeddocattachmentwrite(maxdocid, pdffilename):
        with open('/home/szluka/djangogirls/' + pdffilename, 'rb') as file:
            attachmentcontent = file.read()
        fs = FileSystemStorage()
        #fs.delete(pdffilename)

        cursor4 = connection.cursor()
        cursor4.execute(
            "INSERT INTO quotation_tbldoc_details "
            "( Docid_tblDoc_details_id, "
            "attachmentname_tbldocdetails,"
            "attachmentcontent_tbldocdetails) VALUES (%s,%s,%s)",
            [maxdocid,
             pdffilename,
             attachmentcontent])

        return
    def attachment1write(maxdocid):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        if fs.exists(myfile.name):
            fs.delete(myfile.name)
        global filename
        filename = fs.save(myfile.name, myfile)

        with open('/home/szluka/djangogirls/' + filename, 'rb') as file:
            attachmentcontent = file.read()
        #fs.delete(myfile.name)

        cursor4 = connection.cursor()
        cursor4.execute(
            "INSERT INTO quotation_tbldoc_details "
            "( Docid_tblDoc_details_id, "
            "attachmentname_tbldocdetails,"
            "attachmentcontent_tbldocdetails) VALUES (%s,%s,%s)",
            [maxdocid,
             filename,
             attachmentcontent])

        return
    def attachment2write(maxdocid):

        myfile2 = request.FILES['myfile2']
        fs2 = FileSystemStorage()
        if fs2.exists(myfile2.name):
            fs2.delete(myfile2.name)
        global filename2
        filename2 = fs2.save(myfile2.name, myfile2)
        with open('/home/szluka/djangogirls/' + filename2, 'rb') as file:
            attachmentcontent = file.read()
        #fs2.delete(myfile2.name)

        cursor4 = connection.cursor()
        cursor4.execute(
            "INSERT INTO quotation_tbldoc_details "
            "( Docid_tblDoc_details_id, "
            "attachmentname_tbldocdetails,"
            "attachmentcontent_tbldocdetails) VALUES (%s,%s,%s)",
            [maxdocid,
             filename2,
             attachmentcontent])

        return

    #import pdb;
    #pdb.set_trace()

    howmanyattachedfiles=0
    for x in request.FILES:
        howmanyattachedfiles=howmanyattachedfiles+1
    if howmanyattachedfiles==0: #only doc as pdf attached
        pdfeddocattachmentwrite(maxdocid, pdffilename)
    elif howmanyattachedfiles==1: #doc as pdf +1 attachment
        pdfeddocattachmentwrite(maxdocid, pdffilename)
        attachment1write(maxdocid)

    elif howmanyattachedfiles == 2: #doc as pdf +2 attachments
        pdfeddocattachmentwrite(maxdocid, pdffilename)
        attachment1write(maxdocid)
        attachment2write(maxdocid)

    #import pdb;
    #pdb.set_trace()

    email = EmailMessage(
        emailsubject, emailbodytextmodifiedbyuser, 'from@me.com', [addresseeemail], cc=[cc])
    email.attach_file('/home/szluka/djangogirls/' + pdffilename)
    if howmanyattachedfiles==1:
        email.attach_file('/home/szluka/djangogirls/' + filename)
    if howmanyattachedfiles == 2:
        email.attach_file('/home/szluka/djangogirls/' + filename)
        email.attach_file('/home/szluka/djangogirls/' + filename2)
    email.send()

    fs = FileSystemStorage()
    if fs.exists(pdffilename) :
        fs.delete(pdffilename)

    try:
        filename
    except NameError:
        print
        "well, it WASN'T defined after all!"
    else:
        print
        "sure, it was defined."
        if fs.exists(filename):
            fs.delete(filename)

    try:
        filename2
    except NameError:
        print
        "well, it WASN'T defined after all!"
    else:
        print
        "sure, it was defined."
        if fs.exists(filename2):
            fs.delete(filename2)

    return redirect('emailform', pk=maxdocid)

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
                        "accountduedate_tbldoc, "
                        "emailbodytextmodifiedbyuser_tbldoc "
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

        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT  `Doc_detailsid_tblDoc_details`, "
            "`attachmentname_tbldocdetails` "
            "FROM quotation_tbldoc_details "
            "LEFT JOIN quotation_tbldoc "
            "ON "
            "quotation_tbldoc_details.Docid_tblDoc_details_id = quotation_tbldoc.Docid_tblDoc "
            "WHERE docid_tbldoc_details_id=%s "
            "order by firstnum_tblDoc_details",
            [pk])
        docdetails = cursor3.fetchall()

        cursor10 = connection.cursor()
        cursor10.execute("SELECT id, "
                         "first_name, "
                         "last_name, "
                         "email, "
                         "subscriptiontext_tblauth_user "
                         "FROM auth_user "
                         "WHERE id=%s ", [creatorid])
        creatordata = cursor10.fetchall()

        return render(request, 'quotation/email.html', {'doc': doc,
                                                        'docdetails': docdetails,
                                                        'creatordata': creatordata})

def emailviewattachment(request, pk):
    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT  `Doc_detailsid_tblDoc_details`, "
        "attachmentname_tbldocdetails, "
        "attachmentcontent_tbldocdetails "
        "FROM quotation_tbldoc_details "
        "WHERE Doc_detailsid_tblDoc_details=%s ",
        [pk])
    docdetails = cursor3.fetchall()
    for x in docdetails:
        attachmentname = x[1]
        attachmentcontent = x[2]
    #import pdb;
    #pdb.set_trace()

    with open(attachmentname, 'wb') as file:
        file.write(attachmentcontent)

    fs = FileSystemStorage()
 #   filename = 'output.pdf'
    if fs.exists(attachmentname):
        with fs.open(attachmentname) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="output.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')
