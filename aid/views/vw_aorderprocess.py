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
import paypalrestsdk
import logging
import re
from django.core.mail import EmailMessage

# import pdb;
# pdb.set_trace()
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
def aorderprocesspaypalpayment(request):
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "AcTczGRsMLRWW0dxFloKmk1QwEDYEoU82MqbUWihnAwbX3gKP6xvKBVZsTNPfkVGhwVCnqAr98EHvl0E",
        "client_secret": "ECUunsjZzU6QGgi7vGoD88e2W3U63XfbiE8_AxVBuAj7SC6R-kZWG7r3NNTEr0Jt3-yOjGNypE3nxTYu"})

    paypalamounttotal = '217'
    paypalamountcurrency = 'USD'

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://google.com",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "amount": {
                "total": "" + paypalamounttotal + "",
                "currency": "" + paypalamountcurrency + ""},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print("Payment created successfully")
        print("paymentid: " + payment.id)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                print("Redirect for approval: %s" % (redirect_url))
    else:
        print(payment.error)
    ectoken = re.search('token=(.+)', redirect_url).group(1)

# aorderdocadd begin
    dockindidfornewdoc = '2'
    contactidfornewdoc = '13'
    creatorid = 2

    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT contactid_tblacontacts, "
        "companyname_tblacompanies, "
        "Companyid_tblaCompanies, "
        "Firstname_tblacontacts, "
        "lastname_tblacontacts, "
        "title_tblacontacts, "
        "mobile_tblacontacts, "
        "email_tblacontacts, "
        "pcd_tblacompanies, "
        "town_tblacompanies, "
        "address_tblacompanies "

        "FROM aid_tblacontacts "

        "JOIN aid_tblacompanies "
        "ON aid_tblacompanies.companyid_tblacompanies = aid_tblacontacts.companyid_tblacontacts_id "

        "WHERE contactid_tblacontacts =%s", [contactidfornewdoc])
    companyandcontactdata = cursor1.fetchall()
    for instancesingle in companyandcontactdata:
        companynameclone = instancesingle[1]
        companyid = instancesingle[2]  # for the lookup the default values in the tblcompanies (i.e. defaultpreface)
        firstnameclone = instancesingle[3]
        lastnameclone = instancesingle[4]
        titleclone = instancesingle[5]
        mobileclone = instancesingle[6]
        emailclone = instancesingle[7]
        pcdclone = instancesingle[8]
        townclone = instancesingle[9]
        addressclone = instancesingle[10]

    cursor5 = connection.cursor()
    cursor5.execute(
        "SELECT defaultbackpageidforquotation_tblacompanies, "
        "defaultprefaceidforquotation_tblacompanies, "
        "defaultpaymentid_tblacompanies "

        "FROM aid_tblacompanies "

        "WHERE Companyid_tblaCompanies = %s", [companyid])
    defaultsfromtblcompanies = cursor5.fetchall()
    for instancesingle in defaultsfromtblcompanies:
        defaultbackpageidforquotation = instancesingle[0]
        defaultprefaceidforquotation = instancesingle[1]
        defaultpaymentid = instancesingle[2]

    cursor6 = connection.cursor()
    cursor6.execute(
        "SELECT paymenttextforquotation_tblpayment "
        "FROM quotation_tblpayment "
        "WHERE paymentid_tblpayment = %s", [defaultpaymentid])
    paymentset = cursor6.fetchall()
    for instancesingle in paymentset:
        paymenttextcloneforquotation = instancesingle[0]

    cursor6 = connection.cursor()
    cursor6.execute(
        "SELECT backpagetextforquotation_tblbackpageforquotation "
        "FROM quotation_tblbackpageforquotation "
        "WHERE backpageidforquotation_tblbackpageforquotation = %s", [defaultbackpageidforquotation])
    backpageset = cursor6.fetchall()
    for instancesingle in backpageset:
        backpagetextcloneforquotation = instancesingle[0]

    cursor7 = connection.cursor()
    cursor7.execute(
        "SELECT prefacetextforquotation_tblprefaceforquotation "
        "FROM quotation_tblprefaceforquotation "
        "WHERE prefaceidforquotation_tblprefaceforquotation = %s", [defaultprefaceidforquotation])
    prefaceset = cursor7.fetchall()
    for instancesingle in prefaceset:
        prefacecloneforquotation = instancesingle[0]

    cursor7 = connection.cursor()
    cursor7.execute(
        "SELECT currencyisocode_tblcurrency "
        "FROM quotation_tblcurrency "
        "WHERE accountcurrency_tblcurrency = 1")
    results = cursor7.fetchall()
    for instancesingle in results:
        accountcurrencycodeclone = instancesingle[0]

    cursor8 = connection.cursor()
    cursor8.execute("SELECT max(docnumber_tblaDoc) FROM aid_tbladoc "
                    "WHERE Doc_kindid_tblaDoc_id = %s", [dockindidfornewdoc])
    results = cursor8.fetchall()
    resultslen = len(results)
    # import pdb;
    # pdb.set_trace()

    if results[0][0] is not None:  # only if there is not doc yet (this would be the first instance)
        for x in results:
            docnumber = x[0]
            docnumber += 1
    else:
        docnumber = 80  # arbitrary number

    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO aid_tbladoc "
                    "( Doc_kindid_tblaDoc_id, "
                    "Contactid_tblaDoc_id,"
                    "companyname_tblcompanies_ctbladoc, "
                    "firstname_tblcontacts_ctbladoc, "
                    "lastname_tblcontacts_ctbladoc, "
                    "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                    "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                    "docnumber_tblaDoc, "
                    "creatorid_tbladoc, "
                    "title_tblcontacts_ctbladoc, "
                    "mobile_tblcontacts_ctbladoc, "
                    "email_tblcontacts_ctbladoc, "
                    "pcd_tblcompanies_ctbladoc, "
                    "town_tblcompanies_ctbladoc, "
                    "address_tblcompanies_ctbladoc, "
                    "paymenttextforquotation_tblpayment_ctbladoc, "
                    "accountcurrencycode_tbladoc, "
                    "paypalpaymentid_tbladoc, "
                    "paypalectoken_tbladoc, "
                    "paypalamounttotal_tbladoc, "
                    "paypalamountcurrency_tbladoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [dockindidfornewdoc, contactidfornewdoc, companynameclone, firstnameclone, lastnameclone,
                     prefacecloneforquotation, backpagetextcloneforquotation, docnumber, creatorid,
                     titleclone,
                     mobileclone,
                     emailclone,
                     pcdclone,
                     townclone,
                     addressclone,
                     paymenttextcloneforquotation,
                     accountcurrencycodeclone,
                     payment.id,
                     ectoken,
                     paypalamounttotal,
                     paypalamountcurrency])

    cursor3 = connection.cursor()
    cursor3.execute("SELECT max(Docid_tblaDoc) FROM aid_tbladoc")
    results = cursor3.fetchall()
    for x in results:
        maxdocid = x[0]

    cursor4 = connection.cursor()
    cursor4.execute(
        "INSERT INTO aid_tbladoc_details ( Docid_tblaDoc_details_id) VALUES (%s)",
        [maxdocid])


    # aorderdocadd end
    datavar = ectoken
    json_data = json.dumps(datavar)

    return HttpResponse(json_data, content_type="application/json")

def aorderprocesspaymentcheck(request):

    ectoken = request.POST['ectoken']
    print("ectoken from check: " + ectoken)

    cursor3 = connection.cursor()
    cursor3.execute("SELECT "

                    "paypalpaymentid_tbladoc "

                    "FROM aid_tbladoc "
                    ""
                    "WHERE paypalectoken_tbladoc=%s ",
                    [ectoken])
    results = cursor3.fetchall()
    for x in results:
        paymentidfromsql = x[0]
    print("paymentid from check: " + paymentidfromsql)

    payment = paypalrestsdk.Payment.find(paymentidfromsql)
    #orderid = payment.transactions[0].related_resources[0].order.id
    print("from check: " + str(payment.payer.status))
    print("paymentdetails from check with single quotes: " + str(payment))
    paymentwithdoublequotes = str(payment).replace("\'", "\"")
    print("paymentdetails from check with double quotes: " + paymentwithdoublequotes)
    parsed = json.loads(paymentwithdoublequotes)
    #import pdb;
    #pdb.set_trace()
    print("parsedpayment: " + json.dumps(parsed, indent=4, sort_keys=True))

    print("paymenttransactionwithsinglequotes: " + payment.transactions[0]["amount"].currency)
    print("paymenttransactionwithsinglequotes: " + payment.transactions[0]["amount"].total)
    #paymenttransactionwithdoublequotes = str(payment.transactions["description"]).replace("\'", "\"")
    #print("paymenttransactionwithdoublequotes: " + paymenttransactionwithdoublequotes)
    #parsedpaymenttransactionwithdoublequotes = json.loads(paymenttransactionwithdoublequotes)
    #print("parsedpaymenttransactionwithdoublequotes: " + json.dumps(parsedpaymenttransactionwithdoublequotes, indent=4, sort_keys=True))

    #print("paym enttotal: " + payment.transactions.amount.total)
          #+ payment.transactions.amount.currency )
    #print("paymentdetails from check: " + str(payment))


    #    order = Order.find(paymentidfromsql)
#    print("ordersuccess " + order.success())

    return render(request, 'aid/awelcome.html', {})

def aorderprocessmidiordersearch(request):
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

    return render(request, 'aid/aorderprocessmidiordersearch.html',
                  {'enabledproductstoorderprocess': enabledproductstoorderprocess})


def aorderprocessmidiordersearchcontent(request):
    docnumber = request.POST['docnumber']
    dockindname = request.POST['dockindname']
    fromdate = request.POST['fromdate']
    todate = request.POST['todate']
    company = request.POST['company']

    if docnumber != '':
        docnumberformainresults = "and D1.docnumber_tbladoc='" + docnumber + "' "
    else:
        docnumberformainresults = ""
        docnumberforrowsources = ""

    if dockindname != '':
        dockindnameformainresults = "and Doc_kind_name_tblaDoc_kind='" + dockindname + "' "
        dockindnameforrowsources = "and Doc_kind_name_tblaDoc_kind='" + dockindname + "' "
    else:
        dockindnameformainresults = ""
        dockindnameforrowsources = ""

    # datephrase = "and creationtime_tbldoc BETWEEN '" + fromdate + "' and '" + todate + "' "
    #    datephrase = "and DATE(quotation_tbldoc.creationtime_tbldoc) >= '" + fromdate + "' and DATE('D.creationtime_tbldoc') <= '" + todate + "' "
    #    datephrase = "and D.creationtime_tbldoc >= '" + fromdate + "' and D.creationtime_tbldoc <= '" + todate + "' "
    # datephrase = "and DATE(creationtime_tbldoc) = '2019-04-19'"
    datephraseformainresults = ''
    datephraseforrowsources = ''
    if company != '':
        companyformainresults = "and companyname_tblcompanies_ctbladoc='" + company + "'"
        companyforrowsources = "and companyname_tblcompanies_ctbladoc='" + company + "'"
    else:
        companyformainresults = ""
        companyforrowsources = ""

    # import pdb;
    # pdb.set_trace()
    searchphraseformainresults = docnumberformainresults + dockindnameformainresults + datephraseformainresults + companyformainresults + " "
    searchphraseforrowsources = dockindnameforrowsources + companyforrowsources + " "

    cursor1 = connection.cursor()
    # import pdb;
    # pdb.set_trace()

    cursor1.execute("SELECT "
                    "midifileid_tblamidifiles, "
                    "title_tblamidifiles "

                    "FROM aid_tblamidifiles ")

#                    "HAVING D1.obsolete_tbladoc = 0 " + searchphraseformainresults + ""
#                    "order by D1.docid_tbladoc desc ")
    midifiles = cursor1.fetchall()
    # import pdb;
    # pdb.set_trace()

    cursor2 = connection.cursor()
    cursor2.execute("SELECT "
                    "companyname_tblcompanies_ctbldoc "

                    "FROM quotation_tbldoc "

                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                    "WHERE quotation_tbldoc.obsolete_tbldoc = 0 " + searchphraseforrowsources + ""
                                                                                                "GROUP BY companyname_tblcompanies_ctbldoc ")

    companiesrowsources = cursor2.fetchall()
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Doc_kind_name_tblDoc_kind "

                    "FROM quotation_tbldoc "

                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                    "WHERE quotation_tbldoc.obsolete_tbldoc = 0 " + searchphraseforrowsources + ""
                                                                                                "GROUP BY Doc_kind_name_tblDoc_kind ")

    dockindrowsources = cursor1.fetchall()
    return render(request, 'aid/aorderprocessmidiordersearchcontent.html', {'midifiles': midifiles,
                                                          'companiesrowsources': companiesrowsources,
                                                          'dockindrowsources': dockindrowsources})
def aorderprocessmidiorderpaypalpayment(request):
    midifileid = request.POST['midifileid']
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "AcTczGRsMLRWW0dxFloKmk1QwEDYEoU82MqbUWihnAwbX3gKP6xvKBVZsTNPfkVGhwVCnqAr98EHvl0E",
        "client_secret": "ECUunsjZzU6QGgi7vGoD88e2W3U63XfbiE8_AxVBuAj7SC6R-kZWG7r3NNTEr0Jt3-yOjGNypE3nxTYu"})

    paypalamounttotal = '0.89'
    paypalamountcurrency = 'USD'

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://google.com",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "amount": {
                "total": "" + paypalamounttotal + "",
                "currency": "" + paypalamountcurrency + ""},
            "description": "" + midifileid + ""}]})

    if payment.create():
        print("Payment created successfully")
        print("paymentid: " + payment.id)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                print("Redirect for approval: %s" % (redirect_url))
    else:
        print(payment.error)
    ectoken = re.search('token=(.+)', redirect_url).group(1)

# aorderdocadd begin
    dockindidfornewdoc = '2'
    contactidfornewdoc = '13'
    creatorid = 2

    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT contactid_tblacontacts, "
        "companyname_tblacompanies, "
        "Companyid_tblaCompanies, "
        "Firstname_tblacontacts, "
        "lastname_tblacontacts, "
        "title_tblacontacts, "
        "mobile_tblacontacts, "
        "email_tblacontacts, "
        "pcd_tblacompanies, "
        "town_tblacompanies, "
        "address_tblacompanies "

        "FROM aid_tblacontacts "

        "JOIN aid_tblacompanies "
        "ON aid_tblacompanies.companyid_tblacompanies = aid_tblacontacts.companyid_tblacontacts_id "

        "WHERE contactid_tblacontacts =%s", [contactidfornewdoc])
    companyandcontactdata = cursor1.fetchall()
    for instancesingle in companyandcontactdata:
        companynameclone = instancesingle[1]
        companyid = instancesingle[2]  # for the lookup the default values in the tblcompanies (i.e. defaultpreface)
        firstnameclone = instancesingle[3]
        lastnameclone = instancesingle[4]
        titleclone = instancesingle[5]
        mobileclone = instancesingle[6]
        emailclone = instancesingle[7]
        pcdclone = instancesingle[8]
        townclone = instancesingle[9]
        addressclone = instancesingle[10]

    cursor5 = connection.cursor()
    cursor5.execute(
        "SELECT defaultbackpageidforquotation_tblacompanies, "
        "defaultprefaceidforquotation_tblacompanies, "
        "defaultpaymentid_tblacompanies "

        "FROM aid_tblacompanies "

        "WHERE Companyid_tblaCompanies = %s", [companyid])
    defaultsfromtblcompanies = cursor5.fetchall()
    for instancesingle in defaultsfromtblcompanies:
        defaultbackpageidforquotation = instancesingle[0]
        defaultprefaceidforquotation = instancesingle[1]
        defaultpaymentid = instancesingle[2]

    cursor6 = connection.cursor()
    cursor6.execute(
        "SELECT paymenttextforquotation_tblpayment "
        "FROM quotation_tblpayment "
        "WHERE paymentid_tblpayment = %s", [defaultpaymentid])
    paymentset = cursor6.fetchall()
    for instancesingle in paymentset:
        paymenttextcloneforquotation = instancesingle[0]

    cursor6 = connection.cursor()
    cursor6.execute(
        "SELECT backpagetextforquotation_tblbackpageforquotation "
        "FROM quotation_tblbackpageforquotation "
        "WHERE backpageidforquotation_tblbackpageforquotation = %s", [defaultbackpageidforquotation])
    backpageset = cursor6.fetchall()
    for instancesingle in backpageset:
        backpagetextcloneforquotation = instancesingle[0]

    cursor7 = connection.cursor()
    cursor7.execute(
        "SELECT prefacetextforquotation_tblprefaceforquotation "
        "FROM quotation_tblprefaceforquotation "
        "WHERE prefaceidforquotation_tblprefaceforquotation = %s", [defaultprefaceidforquotation])
    prefaceset = cursor7.fetchall()
    for instancesingle in prefaceset:
        prefacecloneforquotation = instancesingle[0]

    cursor7 = connection.cursor()
    cursor7.execute(
        "SELECT currencyisocode_tblcurrency "
        "FROM quotation_tblcurrency "
        "WHERE accountcurrency_tblcurrency = 1")
    results = cursor7.fetchall()
    for instancesingle in results:
        accountcurrencycodeclone = instancesingle[0]

    cursor8 = connection.cursor()
    cursor8.execute("SELECT max(docnumber_tblaDoc) FROM aid_tbladoc "
                    "WHERE Doc_kindid_tblaDoc_id = %s", [dockindidfornewdoc])
    results = cursor8.fetchall()
    resultslen = len(results)
    # import pdb;
    # pdb.set_trace()

    if results[0][0] is not None:  # only if there is not doc yet (this would be the first instance)
        for x in results:
            docnumber = x[0]
            docnumber += 1
    else:
        docnumber = 80  # arbitrary number

    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO aid_tbladoc "
                    "( Doc_kindid_tblaDoc_id, "
                    "Contactid_tblaDoc_id,"
                    "companyname_tblcompanies_ctbladoc, "
                    "firstname_tblcontacts_ctbladoc, "
                    "lastname_tblcontacts_ctbladoc, "
                    "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                    "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                    "docnumber_tblaDoc, "
                    "creatorid_tbladoc, "
                    "title_tblcontacts_ctbladoc, "
                    "mobile_tblcontacts_ctbladoc, "
                    "email_tblcontacts_ctbladoc, "
                    "pcd_tblcompanies_ctbladoc, "
                    "town_tblcompanies_ctbladoc, "
                    "address_tblcompanies_ctbladoc, "
                    "paymenttextforquotation_tblpayment_ctbladoc, "
                    "accountcurrencycode_tbladoc, "
                    "paypalpaymentid_tbladoc, "
                    "paypalectoken_tbladoc, "
                    "paypalamounttotal_tbladoc, "
                    "paypalamountcurrency_tbladoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [dockindidfornewdoc, contactidfornewdoc, companynameclone, firstnameclone, lastnameclone,
                     prefacecloneforquotation, backpagetextcloneforquotation, docnumber, creatorid,
                     titleclone,
                     mobileclone,
                     emailclone,
                     pcdclone,
                     townclone,
                     addressclone,
                     paymenttextcloneforquotation,
                     accountcurrencycodeclone,
                     payment.id,
                     ectoken,
                     paypalamounttotal,
                     paypalamountcurrency])

    cursor3 = connection.cursor()
    cursor3.execute("SELECT "
                    "Docid_tblaDoc "

                    "FROM aid_tbladoc "
                    "WHERE paypalectoken_tbladoc=%s",[ectoken])
    results = cursor3.fetchall()
    for x in results:
        thisdocid = x[0]

    cursor4 = connection.cursor()
    cursor4.execute(
        "INSERT INTO aid_tbladoc_details ( Docid_tblaDoc_details_id) VALUES (%s)",
        [thisdocid])


    # aorderdocadd end
    datavar = ectoken
    json_data = json.dumps(datavar)

    return HttpResponse(json_data, content_type="application/json")
def aorderprocessmidiorderpaymentcheck(request):

    ectoken = request.POST['ectoken']
    print("ectoken from check: " + ectoken)

    cursor3 = connection.cursor()
    cursor3.execute("SELECT "

                    "paypalpaymentid_tbladoc "

                    "FROM aid_tbladoc "
                    ""
                    "WHERE paypalectoken_tbladoc=%s ",
                    [ectoken])
    results = cursor3.fetchall()
    for x in results:
        paymentidfromsql = x[0]
    print("paymentid from check: " + paymentidfromsql)

    payment = paypalrestsdk.Payment.find(paymentidfromsql)
    print("from check: " + str(payment.payer.status))
    print("paymentdetails from check with single quotes: " + str(payment))
    paymentwithdoublequotes = str(payment).replace("\'", "\"")
    print("paymentdetails from check with double quotes: " + paymentwithdoublequotes)
    parsed = json.loads(paymentwithdoublequotes)
    print("parsedpayment: " + json.dumps(parsed, indent=4, sort_keys=True))

    print("paymentcurrency: " + payment.transactions[0]["amount"].currency)
    print("paymenttotal: " + payment.transactions[0]["amount"].total)
    payeremail = payment.payer.payer_info.email
    payerfirstname = payment.payer.payer_info.first_name
    midifileid = payment.transactions[0]["description"] #midifileid from paypal description

    print("payeremail: " + payeremail)

    BASE_DIR = settings.BASE_DIR
    fullmidifilename = BASE_DIR + '/midifiles/' + midifileid + '.mid'
    print("fullmidifilename from check: " + fullmidifilename)
#preparing midifile to send begin (to send Spice_Girls_Wannabe.mid instead of 3.mid - filename preparation)
    subprocess.call('if [ ! -d "' + BASE_DIR + '/midifilestosend/' + ectoken + '" ]; then mkdir ' + BASE_DIR + '/midifilestosend/' + ectoken + '  ;else rm -rf ' + BASE_DIR + '/midifilestosend/' + ectoken + ' && mkdir ' + BASE_DIR + '/midifilestosend/' + ectoken + ';  fi', shell=True)
    subprocess.call('find ' + BASE_DIR + '/midifilestosend/* -mtime +2 -exec rm -rf {} \;', shell=True) #delete older than 2 day /midifilestosend/ directories (with midi files into those)

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "midifileid_tblamidifiles, "
                    "title_tblamidifiles "

                    "FROM aid_tblamidifiles "
                    "WHERE midifileid_tblamidifiles = %s", [midifileid])
    midifiles = cursor1.fetchall()
    for x in midifiles:
        midifiletitle = x[1]

 # get cornumber from cor begin
        cursor3 = connection.cursor()
        cursor3.execute("SELECT "
                        "Docid_tblaDoc "

                        "FROM aid_tbladoc "
                        "WHERE paypalectoken_tbladoc=%s", [ectoken])
        results = cursor3.fetchall()
        for x in results:
            cornumber = x[0]
 # get cornumber from cor end

 # making midifilewithtitle begin

    midifilenamewithid = BASE_DIR + '/midifiles/' + str(midifileid) + '.mid'
    file = open(midifilenamewithid, 'rb')
    midifilecontent = file.read()
    file.close()

    midifilenamewithtitle = BASE_DIR + '/midifilestosend/' + ectoken + '/' + midifiletitle + '_wwwdotaiddotcom_cor' + str(cornumber) + '.mid'
    file = open(midifilenamewithtitle, 'wb')
    file.write(midifilecontent)
    file.close()

 # making midifilewithtitle begin

# preparing midifile to send end


    subject = 'Your midi file from Aid'
    message = render_to_string('aid/amidifilesendingemail.html', {
        'payerfirstname': payerfirstname,
    })
    email = EmailMessage(
        subject, message, 'szluka.mate@gmail.com',
        [payeremail])  # , cc=[cc])
    email.attach_file(midifilenamewithtitle)
    email.content_subtype = "html"
    email.send()

    return render(request, 'aid/awelcome.html', {})
def aorderprocessmidiordercheckoutform(request, midifileid):
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "midifileid_tblamidifiles, "
                    "title_tblamidifiles "

                    "FROM aid_tblamidifiles "
                    "WHERE midifileid_tblamidifiles = %s", [midifileid])

    midifiles = cursor1.fetchall()

    return render(request, 'aid/aorderprocessmidiordercheckout.html', {'midifiles': midifiles})


