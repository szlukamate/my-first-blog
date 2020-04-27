from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required, user_passes_test
from collections import namedtuple
from django.db import connection, transaction
from array import *
import simplejson as json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import shutil
# import pdb;
# pdb.set_trace()
def group_required(group_name, login_url=None):
    """
    Decorator for views that checks whether a user belongs to a particular
    group, redirecting to the log-in page if necessary.
    """
    def check_group(user):
        # First check if the user belongs to the group
        if user.groups.filter(name=group_name).exists():
            return True
    return user_passes_test(check_group, login_url=login_url)
@group_required("manager")
@login_required
def emailadd (request, pk):


    BASE_DIR = settings.BASE_DIR
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



#
    #import pdb;
    #pdb.set_trace()

    emailsubject = "Customer Quotation - Subject: " + originaldocsubject + " - Ref.: " + pretag + str(originaldocnumber) + " EMAIL-" + str(docnumber)
    addresseeemail = request.POST['addresseeemail']
    cc = request.POST['cc']

    pdffilename = request.POST['pdffilename']

    emailbodytextmodifiedbyuser = request.POST['emailbodytext']
    #import pdb;
    #pdb.set_trace()

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
                    "emailbodytextmodifiedbyuser_tbldoc, "
                    "cc_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [5, contactidclone, companynameclone, firstnameclone, lastnameclone, docnumber, creatorid,
                    titleclone,
                    mobileclone,
                    addresseeemail,
                    pcdclone,
                    townclone,
                    addressclone,
                    pk,
                    emailsubject,
                    emailbodytextmodifiedbyuser,
                    cc])
    #import pdb;
    #pdb.set_trace()


    cursor3 = connection.cursor()
    cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
    results = cursor3.fetchall()
    for x in results:
        maxdocid = x[0]

    def attachmentwrite(maxdocid, pdffilename):

        cursor4 = connection.cursor()
        cursor4.execute(
            "INSERT INTO quotation_tbldoc_details "
            "( Docid_tblDoc_details_id, "
            "attachmentname_tbldocdetails) VALUES (%s,%s)",
            [maxdocid, pdffilename])

        cursor4.execute("SELECT max(Doc_detailsid_tblDoc_details) "
                        ""
                        "FROM quotation_tbldoc_details DD "
                        ""
                        "JOIN quotation_tbldoc D "
                        "ON DD.Docid_tblDoc_details_id = D.Docid_tblDoc "
                        ""
                        "WHERE Docid_tblDoc=%s", [maxdocid])
        results = cursor4.fetchall()
        for x in results:
            maxdocdetailsid = x[0]
        #import pdb;
        #pdb.set_trace()
#d
        return maxdocdetailsid

    def attachmentstacking(filenameparameter, maxdocdetailsparameter):

        oldname = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + filenameparameter
        newname = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + str(maxdocdetailsparameter) + '.pdf'
        os.rename(oldname, newname)

        oldpath = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + str(maxdocdetailsparameter) + '.pdf'
        newpath = BASE_DIR + '/emailattachments/' + str(maxdocdetailsparameter) + '.pdf'
        shutil.move(oldpath, newpath)
        return


    howmanyattachedfiles=0
    for x in request.FILES:
        howmanyattachedfiles=howmanyattachedfiles+1
    if howmanyattachedfiles==0: #only doc as pdf attached
        maxdocdetailsid0 = attachmentwrite(maxdocid, pdffilename)

    elif howmanyattachedfiles==1: #doc as pdf +1 attachment
        maxdocdetailsid0 = attachmentwrite(maxdocid, pdffilename) #0

        myfile = request.FILES['myfile'] #1
        with open(BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + myfile.name, 'wb+') as destination: #save to disk from memory
            for chunk in myfile.chunks():
                destination.write(chunk)
        maxdocdetailsid1 = attachmentwrite(maxdocid, myfile.name)

    elif howmanyattachedfiles == 2: #doc as pdf +2 attachments
        maxdocdetailsid0 = attachmentwrite(maxdocid, pdffilename) #0

        myfile = request.FILES['myfile'] #1
        with open(BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + myfile.name, 'wb+') as destination: #save to disk from memory
            for chunk in myfile.chunks():
                destination.write(chunk)
        maxdocdetailsid1 = attachmentwrite(maxdocid, myfile.name)

        myfile2 = request.FILES['myfile2'] #2
        with open(BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + myfile2.name, 'wb+') as destination: #save to disk from memory
            for chunk in myfile2.chunks():
                destination.write(chunk)
        maxdocdetailsid2 = attachmentwrite(maxdocid, myfile2.name)

    docaspdffullpathfilename = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + pdffilename

    fs = FileSystemStorage()

    if fs.exists(docaspdffullpathfilename):

        email = EmailMessage(
            emailsubject, emailbodytextmodifiedbyuser, 'from@me.com', [addresseeemail], cc=[cc])

        if howmanyattachedfiles == 0:
            email.attach_file(docaspdffullpathfilename)
            attachmentstacking(pdffilename, maxdocdetailsid0) #docpdf renaming and moving

        if howmanyattachedfiles == 1:
            email.attach_file(docaspdffullpathfilename) #0
            attachmentstacking(pdffilename, maxdocdetailsid0) #docpdf renaming and moving

            filenamefullpathfilename = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + myfile.name #1
            email.attach_file(filenamefullpathfilename)
            attachmentstacking(myfile.name, maxdocdetailsid1) #attached file1 renaming and moving


        if howmanyattachedfiles == 2:
            email.attach_file(docaspdffullpathfilename) #0
            attachmentstacking(pdffilename, maxdocdetailsid0) #docpdf renaming and moving

            filenamefullpathfilename = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + myfile.name #1
            email.attach_file(filenamefullpathfilename)
            attachmentstacking(myfile.name, maxdocdetailsid1) #attached file1 renaming and moving

            filename2fullpathfilename = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + myfile2.name #1
            email.attach_file(filename2fullpathfilename)
            attachmentstacking(myfile2.name, maxdocdetailsid2) #attached file1 renaming and moving


        email.send()


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
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')
@group_required("manager")
@login_required
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
                        "emailbodytextmodifiedbyuser_tbldoc, "
                        "cc_tbldoc "
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
            "order by Doc_detailsid_tblDoc_details",
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
@group_required("manager")
@login_required
def emailviewattachment(request, pk):
    BASE_DIR = settings.BASE_DIR


    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT  "
        "`Doc_detailsid_tblDoc_details`, "
        "attachmentname_tbldocdetails "

        "FROM quotation_tbldoc_details "
        "WHERE Doc_detailsid_tblDoc_details=%s ",
        [pk])
    docdetails = cursor3.fetchall()
    for x in docdetails:
        docdetailsid = x[0]
        attachmentname = x[1]

    fs = FileSystemStorage()
    storedfilename = BASE_DIR + '/emailattachments/' + str(docdetailsid) + '.pdf'
    if fs.exists(storedfilename):
        with fs.open(storedfilename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="output.pdf"'
            return response
    else:
        return HttpResponseNotFound("The requested pdf was not found in our server.")
@group_required("manager")
@login_required
def emailviewattachmentcandidate(request, pdffilename):
    creatorid = request.user.id
    BASE_DIR = settings.BASE_DIR

    fs = FileSystemStorage()
 #   filename = 'output.pdf'
    filename2 = BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '/' + pdffilename
    #import pdb;
    #pdb.set_trace()

    if fs.exists(filename2):
        with fs.open(filename2) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="output.pdf"'
            return response
    else:
        return HttpResponseNotFound('The requested pdf was not found in our server.')
