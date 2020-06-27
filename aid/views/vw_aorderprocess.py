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
from aid.forms import aorderprocessringtoneorderprecheckoutformclasstemplate, SignUpForm
import aid

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

def aorderprocessringtoneordersearch(request):
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

    return render(request, 'aid/aorderprocessringtoneordersearch.html',
                  {'enabledproductstoorderprocess': enabledproductstoorderprocess})


def aorderprocessringtoneordersearchcontent(request):
    BASE_DIR = settings.BASE_DIR
    STATIC_URL = settings.STATIC_URL
    STATIC_ROOT = settings.STATIC_ROOT
    print("STATIC_URL: " + STATIC_URL)
    print("STATIC_ROOT: " + STATIC_ROOT)

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
                    "ringtonemasterfileid_tblaringtonemasterfiles, "
                    "title_tblaringtonemasterfiles "

                    "FROM aid_tblaringtonemasterfiles ")

#                    "HAVING D1.obsolete_tbladoc = 0 " + searchphraseformainresults + ""
#                    "order by D1.docid_tbladoc desc ")
    ringtonemasterfiles = cursor1.fetchall()

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
    return render(request, 'aid/aorderprocessringtoneordersearchcontent.html', {'ringtonemasterfiles': ringtonemasterfiles,
                                                          'companiesrowsources': companiesrowsources,
                                                          'dockindrowsources': dockindrowsources})
def aorderprocessringtoneorderpaypalpayment(request):
    BASE_DIR = settings.BASE_DIR

    ringtonemasterfileid = request.POST['ringtonemasterfileid']
    emailtosend = request.POST['emailtosend']
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": "AcTczGRsMLRWW0dxFloKmk1QwEDYEoU82MqbUWihnAwbX3gKP6xvKBVZsTNPfkVGhwVCnqAr98EHvl0E",
        "client_secret": "ECUunsjZzU6QGgi7vGoD88e2W3U63XfbiE8_AxVBuAj7SC6R-kZWG7r3NNTEr0Jt3-yOjGNypE3nxTYu"})

#webprofile handling in Paypal begin
    #getting old (existing) webprofile from paypal
    profiles = paypalrestsdk.WebProfile.all()
#    import pdb;
#    pdb.set_trace()

    result = []
    result = [profile.to_dict() for profile in profiles]
    print("webprofile: " + result[0]['id'])

    #    #deleting old webprofile
#    profilex = paypalrestsdk.WebProfile.find(result[0]['id'])
#    profilex.delete()
#    import pdb;
#    pdb.set_trace()
    '''
    #creating new webprofile
    web_profile = paypalrestsdk.WebProfile({
        "name": 'aidWeb_Profile_Name2',
        "presentation": {
            "brand_name": "BusinessName",
            "logo_image": "https://drive.google.com/file/d/1O82aq97ZY0p2JtGik44OdZA_lcKgMTBr/view?usp=sharing",
        "locale_code": "US"
    },
        "input_fields": {
                            "allow_note": 1,
                            "no_shipping": 1,
                            "address_override": 1
                        },
                        "flow_config": {
        "landing_page_type": "Login"
    }
    })
    web_profile.create()  # Will return True or False
    '''
# webprofile handling in Paypal end
    #import pdb;
    #pdb.set_trace()

    paypalamounttotal = '0.89'
    paypalamountcurrency = 'USD'
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "experience_profile_id": result[0]['id'],
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://google.com",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "amount": {
                "total": "" + paypalamounttotal + "",
                "currency": "" + paypalamountcurrency + ""},
            "description": "" + ringtonemasterfileid + ", " + emailtosend + "",
            "item_list": {
                             "shipping_address": {
                                 "city": "Budapestx",
                                 "country_code": "HU",
                                 "line1": "a@v.vv Erzs\\uFFFDbet t\\uFFFDr 9-10",
                                 "postal_code": "1051",
                                 "recipient_name": "John Doe",
                                 "state": "Magyarorszag"
                             }
                         }}]})

    if payment.create():
        print("Payment created successfully")
        print("paymentid: " + payment.id)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = link.href
                #print("Redirect for approval: %s" % (redirect_url))
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
def aorderprocessringtoneorderpaymentcheck(request):
    APP_PATH = os.path.dirname(aid.__file__)
    print("APP_PATH: " + APP_PATH)

    ectoken = request.POST['ectoken']
    print("ectoken from check: " + ectoken)

    cursor3 = connection.cursor()
    cursor3.execute("SELECT "

                    "paypalpaymentid_tbladoc, "
                    "Docid_tbladoc "

                    "FROM aid_tbladoc "
                    ""
                    "WHERE paypalectoken_tbladoc=%s ",
                    [ectoken])
    results = cursor3.fetchall()
    for x in results:
        paymentidfromsql = x[0]
        cordocid = x[1]
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
    description = payment.transactions[0]["description"] #ringtonemasterfileid from paypal description
    descriptionsplitted = description.split(", ")
    ringtonemasterfileid = descriptionsplitted[0]
    emailtosend = descriptionsplitted[1]
    print("payeremail: " + payeremail)
    print("ringtonemasterfileid: " + ringtonemasterfileid)
    print("emailtosend: " + emailtosend)

    BASE_DIR = settings.BASE_DIR

    #preparing ringtonemodifiedfile to send begin (to send Spice_Girls_Wannabe.mid instead of 3.mid - filename preparation)
    subprocess.call('if [ ! -d "' + BASE_DIR + '/ringtonemodifiedfiles/' + ectoken + '" ]; then mkdir ' + BASE_DIR + '/ringtonemodifiedfiles/' + ectoken + '  ;else rm -rf ' + BASE_DIR + '/ringtonemodifiedfiles/' + ectoken + ' && mkdir ' + BASE_DIR + '/ringtonemodifiedfiles/' + ectoken + ';  fi', shell=True)
    subprocess.call('find ' + BASE_DIR + '/ringtonemodifiedfiles/* -mmin +59 -exec rm -rf {} \;', shell=True) #delete older than 1 hour /ringtonemodifiedfiles/ directories (with ringtonemodified files into those)

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "ringtonemasterfileid_tblaringtonemasterfiles, "
                    "title_tblaringtonemasterfiles "

                    "FROM aid_tblaringtonemasterfiles "
                    "WHERE ringtonemasterfileid_tblaringtonemasterfiles = %s", [ringtonemasterfileid])
    ringtonemasterfiles = cursor1.fetchall()
    for x in ringtonemasterfiles:
        ringtonemasterfiletitle = x[1]

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

 # making ringtonemodifiedfilewithtitle begin

    ringtonemasterfilenamewithid = APP_PATH + '/static/ringtonemasterfiles/' + str(ringtonemasterfileid) + '.mp3'
    file = open(ringtonemasterfilenamewithid, 'rb')
    ringtonemasterfilecontent = file.read()
    file.close()

    ringtonemodifiedfilepathandtitle = BASE_DIR + '/ringtonemodifiedfiles/' + ectoken + '/' + ringtonemasterfiletitle + '_wwwdotaiddotcom_cor' + str(cornumber) + '.mp3'
    file = open(ringtonemodifiedfilepathandtitle, 'wb')
    file.write(ringtonemasterfilecontent)
    file.close()

    ringtonemodifiedfiletitle = ringtonemasterfiletitle + '_wwwdotaiddotcom_cor' + str(cornumber) + '.mp3'
 # making ringtonemodifiedfilewithtitle end

# preparing ringtonemodifiedfile to send end


    subject = 'Your ringtone file from Aid'
    message = render_to_string('aid/aringtonemodifiedfilesendingemail.html', {
        'payerfirstname': payerfirstname,
    })
    email = EmailMessage(
        subject, message, 'szluka.mate@gmail.com',
        [emailtosend])  # , cc=[cc])
    email.attach_file(ringtonemodifiedfilepathandtitle)
    email.content_subtype = "html"
    email.send()

    return render(request, 'aid/aorderprocessringtoneorderthankyouredirecturl.html', {'emailtosend': emailtosend,'cordocid': cordocid, 'ringtonemodifiedfiletitle': ringtonemodifiedfiletitle })

def aorderprocessringtoneordercheckoutform(request, ringtonemasterfileid, emailtosend):
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "ringtonemasterfileid_tblaringtonemasterfiles, "
                    "title_tblaringtonemasterfiles "

                    "FROM aid_tblaringtonemasterfiles "
                    "WHERE ringtonemasterfileid_tblaringtonemasterfiles = %s", [ringtonemasterfileid])

    ringtonemasterfiles = cursor1.fetchall()

    return render(request, 'aid/aorderprocessringtoneordercheckout.html', {'ringtonemasterfiles': ringtonemasterfiles, 'emailtosend': emailtosend })
def aorderprocessringtoneorderprecheckoutform(request, ringtonemasterfileid):
    if request.method == 'POST':
        form = aorderprocessringtoneorderprecheckoutformclasstemplate(request.POST)
        if form.is_valid():
            '''
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Aid Account'
            message = render_to_string('aid/aaccount_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                subject, message, 'szluka.mate@gmail.com',
                [user.email])  # , cc=[cc])
            email.content_subtype = "html"
            email.send()
            '''
            emailtosend = form.cleaned_data['email']
            return redirect('aorderprocessringtoneordercheckoutform', ringtonemasterfileid = ringtonemasterfileid, emailtosend = emailtosend)
    else:
        form = aorderprocessringtoneorderprecheckoutformclasstemplate()


    return render(request, 'aid/aorderprocessringtoneorderprecheckout.html', {'form': form})

def aorderprocessringtoneorderthankyou(request,emailtosend,cordocid,ringtonemodifiedfiletitle):
    cursor3 = connection.cursor()
    cursor3.execute("SELECT "
                    "Docid_tblaDoc, "
                    "docnumber_tbladoc "

                    "FROM aid_tbladoc "
                    "WHERE Docid_tblaDoc=%s", [cordocid])
    results = cursor3.fetchall()

    for x in results:
        cordocnumber = x[1]

    return render(request, 'aid/aorderprocessringtoneorderthankyou.html', {'emailtosend': emailtosend,'cordocnumber': cordocnumber, 'ringtonemodifiedfiletitle': ringtonemodifiedfiletitle })

