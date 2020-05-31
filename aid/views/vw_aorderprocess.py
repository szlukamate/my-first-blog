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

    #print("paymenttotal: " + payment.transactions.amount.total)
          #+ payment.transactions.amount.currency )
    #print("paymentdetails from check: " + str(payment))


    #    order = Order.find(paymentidfromsql)
#    print("ordersuccess " + order.success())

    return render(request, 'aid/awelcome.html', {})


