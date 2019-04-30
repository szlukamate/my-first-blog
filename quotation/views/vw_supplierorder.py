from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from array import *
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
import subprocess
import os
# import pdb;
# pdb.set_trace()

def supplierorderpre(request):
    cursor3 = connection.cursor()
    cursor3.execute("SELECT  "
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
                    "accountcurrencycode_tbldoc, "
                    "pretag_tbldockind, "

                    "`Doc_detailsid_tblDoc_details`, "
                    "`Qty_tblDoc_details`, "
                    "`Docid_tblDoc_details_id`, "
                    "`customerdescription_tblProduct_ctblDoc_details`, "
                    "`firstnum_tblDoc_details`, "
                    "`fourthnum_tblDoc_details`, "
                    "`secondnum_tblDoc_details`, "
                    "`thirdnum_tblDoc_details`, "
                    "`Note_tblDoc_details`, "
                    "`creationtime_tblDoc_details`, "
                    "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
                    "Productid_tblDoc_details_id, "
                    "Doc_detailsid_tblDoc_details, "
                    "unit_tbldocdetails, "
                    "S.companyname_tblcompanies as supplier, "
                    "suppliercompanyid_tbldocdetails, "

                    "supplierdescription_tblProduct_ctblDoc_details "
                    "FROM quotation_tbldoc_details as DD "
                    "JOIN quotation_tblcompanies as S ON DD.suppliercompanyid_tbldocdetails = S.companyid_tblcompanies "
                    "JOIN quotation_tbldoc as D ON D.Docid_tblDoc=DD.Docid_tblDoc_details_id "
                    "JOIN quotation_tbldoc_kind as DK ON D.Doc_kindid_tblDoc_id = DK.Doc_kindid_tblDoc_kind "
                    "LEFT OUTER JOIN (SELECT cordetailslink_tbldocdetails FROM quotation_tbldoc_details JOIN quotation_tbldoc as D2 ON D2.Docid_tblDoc=quotation_tbldoc_details.Docid_tblDoc_details_id WHERE obsolete_tbldoc=0) as supplierorderset ON DD.Doc_detailsid_tblDoc_details=supplierorderset.cordetailslink_tbldocdetails "
                    "WHERE Doc_kindid_tblDoc_id=2 and obsolete_tbldoc=0 and supplierorderset.cordetailslink_tbldocdetails is null "
                    "order by docnumber_tbldoc,firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details")
    customerorders = cursor3.fetchall()
    customerordersnumber = len(customerorders)

    return render(request, 'quotation/supplierorderpre.html', {'customerorders': customerorders,
                                                               'customerordersnumber': customerordersnumber})

def supplierordermake(request):
    if request.method == 'POST':
        docdetailslistraw = request.POST['docdetailslist']
        docdetailslist = json.loads(docdetailslistraw)
    #import pdb;
    #pdb.set_trace()

    creatorid = request.user.id

    pk=60
    toinoperatordocdetails=""
    for x in range(len(docdetailslist)):
        print(x)
        toinoperatordocdetails = toinoperatordocdetails + docdetailslist[x] + ","
    toinoperatordocdetails = toinoperatordocdetails[: -1]

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "suppliercompanyid_tbldocdetails "
                    "FROM quotation_tbldoc_details "
                    "WHERE Doc_detailsid_tblDoc_details IN (" + toinoperatordocdetails + ") "
                    "Group by suppliercompanyid_tbldocdetails ")
    supplierorders = cursor1.fetchall()

    for x in supplierorders:
        suppliercompanyid = x[0]


        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tblDoc, "
                        "Contactid_tblDoc_id, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbldoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
                        "prefacespecforquotation_tbldoc, "
                        "subject_tbldoc, "
                        "docnumber_tbldoc, "
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
        doc = cursor1.fetchall()
        for x in doc:
            contactid = x[1]
            prefacetext = x[2]
            backpagetext = x[3]
            prefacespectext = x[4]
            subject = x[5]
            total = x[7]
            deliverydays = x[8]
            paymenttext = x[9]
            currencycodeinreport = x[10]
            currencyrateinreport = x[11]
            accountcurrencycode = x[12]

        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT contactid_tblcontacts, companyname_tblcompanies, Companyid_tblCompanies, "
            "Firstname_tblcontacts, lastname_tblcontacts, "
            "title_tblcontacts, "
            "mobile_tblcontacts, "
            "email_tblcontacts, "
            "pcd_tblcompanies, "
            "town_tblcompanies, "
            "address_tblcompanies "
            "FROM quotation_tblcontacts "
            "JOIN quotation_tblcompanies "
            "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
            "WHERE Companyid_tblCompanies =%s", [suppliercompanyid])
        companyandcontactdata = cursor1.fetchall()
        for instancesingle in companyandcontactdata:
            companynameclone = instancesingle[1]
            companyid = instancesingle[2] # for the lookup the default values in the tblcompanies (i.e. defaultpreface)
            firstnameclone = instancesingle[3]
            lastnameclone = instancesingle[4]
            titleclone = instancesingle[5]
            mobileclone = instancesingle[6]
            emailclone = instancesingle[7]
            pcdclone = instancesingle[8]
            townclone = instancesingle[9]
            addressclone = instancesingle[10]

        cursor8 = connection.cursor()
        cursor8.execute("SELECT max(docnumber_tblDoc) FROM quotation_tbldoc "
                        "WHERE Doc_kindid_tblDoc_id = 7")
        results = cursor8.fetchall()
        resultslen = len(results)
        for x in results:
            docnumber = x[0]
            docnumber += 1

        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO quotation_tbldoc "
                        "( Doc_kindid_tblDoc_id, "
                        "Contactid_tblDoc_id, "
                        "companyname_tblcompanies_ctbldoc, "
                        "firstname_tblcontacts_ctbldoc, "
                        "lastname_tblcontacts_ctbldoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbldoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
                        "prefacespecforquotation_tbldoc, "
                        "subject_tbldoc, "
                        "docnumber_tblDoc, "
                        "total_tbldoc, "
                        "deliverydays_tbldoc, "
                        "creatorid_tbldoc, "
                        "title_tblcontacts_ctbldoc, "
                        "mobile_tblcontacts_ctbldoc, "
                        "email_tblcontacts_ctbldoc, "
                        "pcd_tblcompanies_ctbldoc, "
                        "town_tblcompanies_ctbldoc, "
                        "address_tblcompanies_ctbldoc, "
                        "paymenttextforquotation_tblpayment_ctbldoc, "
                        "currencycodeinreport_tbldoc, "
                        "currencyrateinreport_tbldoc, "
                        "doclinkparentid_tbldoc, "
                        "accountcurrencycode_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [7, contactid, companynameclone, firstnameclone, lastnameclone, prefacetext, backpagetext, prefacespectext,
                        subject,
                        docnumber,
                        total,
                        deliverydays,
                        creatorid,
                        titleclone,
                        mobileclone,
                        emailclone,
                        pcdclone,
                        townclone,
                        addressclone,
                        paymenttext,
                        currencycodeinreport,
                        currencyrateinreport,
                        pk,
                        accountcurrencycode])

        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        cursor3.execute("SELECT  `Doc_detailsid_tblDoc_details`, "
                        "`Qty_tblDoc_details`, "
                        "`Docid_tblDoc_details_id`, "
                        "`customerdescription_tblProduct_ctblDoc_details`, "
                        "`firstnum_tblDoc_details`, "
                        "`fourthnum_tblDoc_details`, "
                        "`secondnum_tblDoc_details`, "
                        "`thirdnum_tblDoc_details`, "
                        "`Note_tblDoc_details`, "
                        "`creationtime_tblDoc_details`, "
                        "purchase_price_tblproduct_ctblDoc_details, "
                        "listprice_tblDoc_details, "
                        "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
                        "Productid_tblDoc_details_id, "
                        "Doc_detailsid_tblDoc_details, "
                        "COALESCE(Productid_tblProduct, 0), "
                        "currencyrate_tblcurrency_ctblDoc_details, "
                        "round((((listprice_tblDoc_details-purchase_price_tblproduct_ctblDoc_details)/(listprice_tblDoc_details))*100),1) as listpricemargin, "
                        "unitsalespriceACU_tblDoc_details, "
                        "round((purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as purchasepriceACU, "
                        "round((((unitsalespriceACU_tblDoc_details-(purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details))/(unitsalespriceACU_tblDoc_details))*100),1) as unitsalespricemargin, "
                        "round((listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as listpriceACU, "
                        "(100-round(((unitsalespriceACU_tblDoc_details/(listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details))*100),1)) as discount, "
                        "unit_tbldocdetails, "
                        "suppliercompanyid_tbldocdetails "
                        "FROM quotation_tbldoc_details "
                        "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                        "ON "
                        "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "
                        "WHERE Doc_detailsid_tblDoc_details IN (" + toinoperatordocdetails + ") and suppliercompanyid_tbldocdetails=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                        [suppliercompanyid])
        docdetails = cursor3.fetchall()
    #import pdb;
    #pdb.set_trace()

        for x in docdetails:
            cordetailslink=x[0]
            qty = x[1]
            firstnum = x[4]
            fourthnum = x[5]
            secondnum = x[6]
            thirdnum = x[7]
            note = x[8]
            productid = x[13]
            currencyrate = x[16]
            suppliercompanyid = x[24]

            purchase_priceclone = x[10]
            customerdescriptionclone = x[3]
            currencyisocodeclone = x[12]
            listpricecomputed = x[11]
            currencyrateclone = x[16]
            unitclone = x[23]
            unitsalespriceACU = x[18]

            cursor4 = connection.cursor()
            cursor4.execute(
                "INSERT INTO quotation_tbldoc_details "
                "( Docid_tblDoc_details_id, "
                "`Qty_tblDoc_details`, "
                "`customerdescription_tblProduct_ctblDoc_details`, "
                "firstnum_tblDoc_details, "
                "`fourthnum_tblDoc_details`, "
                "`secondnum_tblDoc_details`, "
                "`thirdnum_tblDoc_details`, "
                "`Note_tblDoc_details`, "
                "purchase_price_tblproduct_ctblDoc_details, "
                "listprice_tblDoc_details, "
                "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
                "Productid_tblDoc_details_id, "
                "currencyrate_tblcurrency_ctblDoc_details, "
                "unitsalespriceACU_tblDoc_details, "
                "unit_tbldocdetails, "
                "suppliercompanyid_tbldocdetails, "
                "cordetailslink_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

                [maxdocid,
                 qty,
                 customerdescriptionclone,
                 firstnum,
                 fourthnum,
                 secondnum,
                 thirdnum,
                 note,
                 purchase_priceclone,
                 listpricecomputed,
                 currencyisocodeclone,
                 productid,
                 currencyrate,
                 unitsalespriceACU,
                 unitclone,
                 suppliercompanyid,
                 cordetailslink])

    return render(request, 'quotation/supplierorderpreredirecturl.html',
                      {'maxdocid': maxdocid})


def supplierorderform(request, pk):

    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        docid = request.POST['docid']
        fieldname = request.POST['fieldname']
        tbl = request.POST['tbl']
        if tbl == "tblDoc_details":
            cursor22 = connection.cursor()
            cursor22.callproc("spsupplierordertbldocdetailsfieldsupdate", [fieldname, fieldvalue, rowid])
            results23 = cursor22.fetchall()
            print(results23)

            json_data = json.dumps(results23)

            return HttpResponse(json_data, content_type="application/json")

        elif tbl == "tblDoc":
            cursor22 = connection.cursor()
            cursor22.callproc("spsupplierordertbldocfieldsupdate", [fieldname, fieldvalue, docid])
            results23 = cursor22.fetchall()
            print(results23)

            json_data = json.dumps(results23)

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
                    "accountcurrencycode_tbldoc, "
                    "pretag_tbldockind "
                    "FROM quotation_tbldoc as D "
                    "JOIN quotation_tbldoc_kind as DK ON D.Doc_kindid_tblDoc_id = DK.Doc_kindid_tblDoc_kind "
                    "WHERE docid_tbldoc=%s "
                    "order by docid_tbldoc desc",
                    [pk])
    doc = cursor1.fetchall()
    for x in doc:
        contactid = x[1]
        creatorid = x[11]

    cursor4 = connection.cursor()
    cursor4.execute("SELECT companyid_tblcontacts_id "
                    "FROM quotation_tblcontacts "
                    "WHERE Contactid_tblContacts=%s ", [contactid])
    companyid = cursor4.fetchall()

    cursor3 = connection.cursor()
    cursor3 = connection.cursor()
    # if there is not such product already not show goto

    cursor3.execute("SELECT  `Doc_detailsid_tblDoc_details`, "
                    "`Qty_tblDoc_details`, "
                    "`Docid_tblDoc_details_id`, "
                    "`customerdescription_tblProduct_ctblDoc_details`, "
                    "`firstnum_tblDoc_details`, "
                    "`fourthnum_tblDoc_details`, "
                    "`secondnum_tblDoc_details`, "
                    "`thirdnum_tblDoc_details`, "
                    "`Note_tblDoc_details`, "
                    "`creationtime_tblDoc_details`, "
                    "purchase_price_tblproduct_ctblDoc_details, "
                    "listprice_tblDoc_details, "
                    "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
                    "Productid_tblDoc_details_id, "
                    "Doc_detailsid_tblDoc_details, "
                    "COALESCE(Productid_tblProduct, 0), "
                    "currencyrate_tblcurrency_ctblDoc_details, "
                    "round((((listprice_tblDoc_details-purchase_price_tblproduct_ctblDoc_details)/(listprice_tblDoc_details))*100),1) as listpricemargin, "
                    "unitsalespriceACU_tblDoc_details, "
                    "round((purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as purchasepriceACU, "
                    "round((((unitsalespriceACU_tblDoc_details-(purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details))/(unitsalespriceACU_tblDoc_details))*100),1) as unitsalespricemargin, "
                    "round((listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as listpriceACU, "
                    "(100-round(((unitsalespriceACU_tblDoc_details/(listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details))*100),1)) as discount, "
                    "unit_tbldocdetails, "
                    "companyname_tblcompanies, "
                    "supplierdescription_tblProduct_ctblDoc_details "
                    "FROM quotation_tbldoc_details as DD "
                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x ON DD.Productid_tblDoc_details_id = x.Productid_tblProduct "
                    "JOIN quotation_tblcompanies as C ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "
                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
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

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT currencyid_tblcurrency, currencyisocode_tblcurrency FROM quotation_tblcurrency")
    currencycodes = cursor3.fetchall()
    transaction.commit()


    cursor5 = connection.cursor()
    cursor5.execute("SELECT `firstnum_tblDoc_details`, "
                    "`secondnum_tblDoc_details`,`thirdnum_tblDoc_details`,`fourthnum_tblDoc_details` "
                    "FROM quotation_tbldoc_details "
                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details desc,secondnum_tblDoc_details desc,thirdnum_tblDoc_details desc,fourthnum_tblDoc_details desc "
                    "LIMIT 1"
                    , [pk])

    maxchapternums = cursor5.fetchall()
#    import pdb;
#    pdb.set_trace()

    for x in maxchapternums:
        maxfirstnum = x[0]
        maxsecondnum = x[1]
        maxthirdnum = x[2]
        maxfourthnum = x[3]

        nextchapternums = array('i', [1, 0, 0, 0])

        nextchapternums[0] = maxfirstnum
        nextchapternums[1] = maxsecondnum
        nextchapternums[2] = maxthirdnum
        nextchapternums[3] = maxfourthnum

    if maxfourthnum ==0:
        if maxthirdnum == 0:
            if maxsecondnum == 0:
                nextchapternums[0]=nextchapternums[0]+1
            else:
                nextchapternums[1]=nextchapternums[1]+1
        else:
            nextchapternums[2]=nextchapternums[2]+1
    else:
        nextchapternums[3]=nextchapternums[3]+1

    return render(request, 'quotation/supplierorder.html', {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums' : nextchapternums,
                                                        'creatordata': creatordata,
                                                        'currencycodes': currencycodes})
