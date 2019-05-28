from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from array import *
import simplejson as json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
import subprocess
import os
# import pdb;
# pdb.set_trace()

def purchaseorderpre(request):
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
                    "`Qty_tblDoc_details` as customerqty, "
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
                    "supplierdescription_tblProduct_ctblDoc_details, "
                    "COALESCE(purchaseorderset.purchaseQty,0) as purchaseqty2, "
                    "obsolete_tbldoc, "
                    "(Qty_tblDoc_details-COALESCE(purchaseorderset.purchaseQty,0)) as tosorqty "
                    "FROM quotation_tbldoc_details as DD "
                    "JOIN quotation_tblcompanies as S ON DD.suppliercompanyid_tbldocdetails = S.companyid_tblcompanies "
                    "JOIN quotation_tbldoc as D ON D.Docid_tblDoc=DD.Docid_tblDoc_details_id "
                    "JOIN quotation_tbldoc_kind as DK ON D.Doc_kindid_tblDoc_id = DK.Doc_kindid_tblDoc_kind "
                    
                    "LEFT OUTER JOIN "
                    "   (SELECT podetailslink_tbldocdetails, sum(Qty_tblDoc_details) as purchaseqty "
                    "   FROM quotation_tbldoc_details "
                    "   JOIN quotation_tbldoc as D2 "
                    "   ON D2.Docid_tblDoc=quotation_tbldoc_details.Docid_tblDoc_details_id "
                    "   WHERE obsolete_tbldoc=0 " 
                    "   GROUP BY podetailslink_tbldocdetails) as purchaseorderset "
                    "ON DD.Doc_detailsid_tblDoc_details=purchaseorderset.podetailslink_tbldocdetails "
                    "HAVING Doc_kindid_tblDoc_id=2 and obsolete_tbldoc=0 and customerqty > COALESCE(purchaseqty2, 0) "
                    "order by docnumber_tbldoc,firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details")
    customerorders = cursor3.fetchall()
    customerordersnumber = len(customerorders)

    return render(request, 'quotation/purchaseorderpre.html', {'customerorders': customerorders,
                                                               'customerordersnumber': customerordersnumber})

def purchaseordermake(request):
    if request.method == 'POST':
        docdetailslistraw = request.POST['docdetailslist']
        docdetailslist = json.loads(docdetailslistraw)
    #import pdb;
    #pdb.set_trace()

    creatorid = request.user.id

    pk=60
    toinoperatordocdetails=""
    for x in range(0,len(docdetailslist),2):
        toinoperatordocdetails = toinoperatordocdetails + docdetailslist[x] + ","
    toinoperatordocdetails = toinoperatordocdetails[: -1]
    #import pdb;
    #pdb.set_trace()

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "suppliercompanyid_tbldocdetails, "
                    "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details "
                    "FROM quotation_tbldoc_details "
                    "WHERE Doc_detailsid_tblDoc_details IN (" + toinoperatordocdetails + ") "
                    "Group by suppliercompanyid_tbldocdetails, currencyisocode_tblcurrency_ctblproduct_ctblDoc_details ")
    purchaseorders = cursor1.fetchall()

    for x in purchaseorders:
        suppliercompanyid = x[0]
        currencyisocode = x[1]


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
            currencycodeinreport = currencyisocode
            currencyrateinreport = x[11]
            accountcurrencycode = x[12]

        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT contactid_tblcontacts, companyname_tblcompanies, Companyid_tblCompanies, "
            "Firstname_tblcontacts, "
            "lastname_tblcontacts, "
            "title_tblcontacts, "
            "mobile_tblcontacts, "
            "email_tblcontacts, "
            "pcd_tblcompanies, "
            "town_tblcompanies, "
            "address_tblcompanies "
            "FROM quotation_tblcontacts "
            "JOIN quotation_tblcompanies "
            "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
            "WHERE Companyid_tblCompanies =%s and purchaseordercontact_tblcontacts=1", [suppliercompanyid])
        companyandcontactdata = cursor1.fetchall()
        if len(companyandcontactdata) == 0:
            return HttpResponse("Is not default contact for purchase orders?")
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

        if results[0][0] is not None: # only if there is not doc yet (this would be the first instance)
            for x in results:
                docnumber = x[0]
                docnumber += 1
        else:
                docnumber = 80 # arbitrary number

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
                        "unit_tbldocdetails, " #23
                        "suppliercompanyid_tbldocdetails, "
                        "supplierdescription_tblProduct_ctblDoc_details "
                        "FROM quotation_tbldoc_details "
                        "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                        "ON "
                        "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "
                        "WHERE Doc_detailsid_tblDoc_details IN (" + toinoperatordocdetails + ") and suppliercompanyid_tbldocdetails=%s and currencyisocode_tblcurrency_ctblproduct_ctblDoc_details=%s"
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                        [suppliercompanyid, currencyisocode])
        docdetails = cursor3.fetchall()

        for x in docdetails:
            podetailslink=x[0]
            for y in range(0, len(docdetailslist), 2): # qty set according to remnants in purhaseorderpre.html form
                if int(docdetailslist[y]) == podetailslink:
                    qty=docdetailslist[y+1]
            #import pdb;
            #pdb.set_trace()

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
            supplierdescriptionclone = x[25]

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
                "podetailslink_tbldocdetails, "
                "supplierdescription_tblProduct_ctblDoc_details) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

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
                 podetailslink,
                 supplierdescriptionclone])

    return render(request, 'quotation/purchaseorderpreredirecturl.html',
                      {'maxdocid': maxdocid})


def purchaseorderform(request, pk):

    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        docid = request.POST['docid']
        fieldname = request.POST['fieldname']
        tbl = request.POST['tbl']
        if tbl == "tblDoc_details":
            cursor22 = connection.cursor()
            cursor22.callproc("sppurchaseordertbldocdetailsfieldsupdate", [fieldname, fieldvalue, rowid])
            results23 = cursor22.fetchall()
            print(results23)

            json_data = json.dumps(results23)

            return HttpResponse(json_data, content_type="application/json")

        elif tbl == "tblDoc":
            cursor22 = connection.cursor()
            cursor22.callproc("sppurchaseordertbldocfieldsupdate", [fieldname, fieldvalue, docid])
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

    cursor3.execute("SELECT  DD.Doc_detailsid_tblDoc_details, "
                    "DD.Qty_tblDoc_details, "
                    "DD.Docid_tblDoc_details_id, "
                    "DD.customerdescription_tblProduct_ctblDoc_details, "
                    "DD.firstnum_tblDoc_details, "
                    "DD.fourthnum_tblDoc_details, "
                    "DD.secondnum_tblDoc_details, "
                    "DD.thirdnum_tblDoc_details, "
                    "DD.Note_tblDoc_details, "
                    "DD.creationtime_tblDoc_details, "
                    "DD.purchase_price_tblproduct_ctblDoc_details, "
                    "DD.listprice_tblDoc_details, "
                    "DD.currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
                    "DD.Productid_tblDoc_details_id, "
                    "DD.Doc_detailsid_tblDoc_details, "
                    "COALESCE(Productid_tblProduct, 0), "
                    "DD.currencyrate_tblcurrency_ctblDoc_details, "
                    "round((((DD.listprice_tblDoc_details-DD.purchase_price_tblproduct_ctblDoc_details)/(DD.listprice_tblDoc_details))*100),1) as listpricemargin, "
                    "DD.unitsalespriceACU_tblDoc_details, "
                    "round((DD.purchase_price_tblproduct_ctblDoc_details * DD.currencyrate_tblcurrency_ctblDoc_details),2) as purchasepriceACU, "
                    "round((((DD.unitsalespriceACU_tblDoc_details-(DD.purchase_price_tblproduct_ctblDoc_details * DD.currencyrate_tblcurrency_ctblDoc_details))/(DD.unitsalespriceACU_tblDoc_details))*100),1) as unitsalespricemargin, "
                    "round((DD.listprice_tblDoc_details * DD.currencyrate_tblcurrency_ctblDoc_details),2) as listpriceACU, "
                    "(100-round(((DD.unitsalespriceACU_tblDoc_details/(DD.listprice_tblDoc_details * DD.currencyrate_tblcurrency_ctblDoc_details))*100),1)) as discount, "
                    "DD.unit_tbldocdetails, "
                    "companyname_tblcompanies, "
                    "DD.supplierdescription_tblProduct_ctblDoc_details, " #25
                    
                    "DD2.cordocdetailsid, "
                    "DD2.cordocid, "
                    "DD2.cordetailsqty, "
                    "DD2.cordocnumber, "
                    "DD2.corpretag, "
                    "DD2.corcompany "
                    
                    "FROM quotation_tbldoc_details as DD "
                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x ON DD.Productid_tblDoc_details_id = x.Productid_tblProduct "
                    "JOIN quotation_tblcompanies as C ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "

                    "LEFT JOIN (SELECT (Doc_detailsid_tblDoc_details) as cordocdetailsid, "
                    "           (docid) as cordocid,"
                    "           (Qty_tblDoc_details) as cordetailsqty, "
                    "           (docnumber_tbldoc) as cordocnumber, "
                    "           (pretag_tbldockind) as corpretag, "
                    "           (companyname_tblcompanies_ctbldoc) as corcompany "
                    "           FROM quotation_tbldoc_details as DDx "
                    "           JOIN (SELECT docnumber_tbldoc, "
                    "                       companyname_tblcompanies_ctbldoc, "
                    "                       (COALESCE(Docid_tblDoc, 0)) as docid, "
                    "                       pretag_tbldockind "
                    "                       FROM quotation_tbldoc "
                    "                       JOIN quotation_tbldoc_kind "
                    "                       ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                    
                    "                       WHERE obsolete_tbldoc = 0"
                    "                ) as D"
                    "           ON D.docid=DDx.Docid_tblDoc_details_id "

                    "           ) as DD2 "
                    "ON DD.podetailslink_tbldocdetails=DD2.cordocdetailsid "

                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [pk])
    docdetails = cursor3.fetchall()

    cursor14 = connection.cursor()
    cursor14.execute("SELECT DD.Doc_detailsid_tblDoc_details, "
                     "DD2.denodocdetails, "
                     "DD2.denodocdetailsqty, "
                     "DD2.denodocnumber, "
                     "DD2.denopretag, "
                     "DD2.denodocid, "

                     "DD3.sumdenodocdetailsqty "
                     "FROM quotation_tbldoc_details as DD "
                     "LEFT JOIN    (SELECT (Doc_detailsid_tblDoc_details) as denodocdetails, "
                     "               denotopodetailslink_tbldocdetails, "
                     "               (Qty_tblDoc_details) as denodocdetailsqty, "
                     "               (docnumber_tbldoc) as denodocnumber, "
                     "               (pretag_tbldockind) as denopretag, "
                     "               (docid) as denodocid "
                     "               FROM quotation_tbldoc_details as DDx "

                     "               JOIN (SELECT docnumber_tbldoc, "
                     "                            (COALESCE(Docid_tblDoc, 0)) as docid, "
                     "                             pretag_tbldockind "
                     "                       FROM quotation_tbldoc"
                     "                       JOIN quotation_tbldoc_kind "
                     "                       ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                     "                       WHERE obsolete_tbldoc = 0"
                     "                    ) as D"
                     "               ON D.docid=DDx.Docid_tblDoc_details_id "
                     "            ) as DD2 "
                     "ON DD.Doc_detailsid_tblDoc_details=DD2.denotopodetailslink_tbldocdetails "

                     "LEFT JOIN    (SELECT denotopodetailslink_tbldocdetails, sum(Qty_tblDoc_details) as sumdenodocdetailsqty "
                     "               FROM quotation_tbldoc_details as DDxx "

                     "               JOIN quotation_tbldoc as Dxx "
                     "               ON Dxx.Docid_tblDoc=DDxx.Docid_tblDoc_details_id "
                     "               WHERE obsolete_tbldoc=0 "
                     "               GROUP BY denotopodetailslink_tbldocdetails) as DD3 "
                     "ON DD.Doc_detailsid_tblDoc_details=DD3.denotopodetailslink_tbldocdetails "

                     "WHERE DD.docid_tbldoc_details_id=%s", [pk])
    denotopolinks = cursor14.fetchall()

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

    return render(request, 'quotation/purchaseorder.html', {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums' : nextchapternums,
                                                            'creatordata': creatordata,
                                                            'denotopolinks': denotopolinks,

                                                            'currencycodes': currencycodes})


def purchaseorderprint(request, docid):
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
                    "currencyrateinreport_tbldoc "

                    "FROM quotation_tbldoc "
                    "WHERE docid_tbldoc=%s "
                    "order by docid_tbldoc desc",
                    [docid])
    doc = cursor1.fetchall()
    for x in doc:
        creatorid = x[11]

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT  `Doc_detailsid_tblDoc_details`, "
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
        "unit_tbldocdetails, "
        "currencyrateinreport_tbldoc "
        "unitsalespriceACU_tblDoc_details, "
        "round((unitsalespriceACU_tblDoc_details/currencyrateinreport_tbldoc),2) as unitsalespricetoreport, "
        "round((unitsalespriceACU_tblDoc_details/currencyrateinreport_tbldoc),2)*Qty_tblDoc_details as salespricetoreport, "
        "round((purchase_price_tblproduct_ctblDoc_details),2) as unitpurchasepricetoreport, "
        "round((purchase_price_tblproduct_ctblDoc_details),2)*Qty_tblDoc_details as purchasepricetoreport "

        "FROM quotation_tbldoc_details "
        "LEFT JOIN quotation_tbldoc "
        "ON "
        "quotation_tbldoc_details.Docid_tblDoc_details_id = quotation_tbldoc.Docid_tblDoc "
        "WHERE docid_tbldoc_details_id=%s "
        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
        [docid])
    docdetails = cursor3.fetchall()

    cursor4 = connection.cursor()
    cursor4.execute(
        "SELECT  COUNT(Doc_detailsid_tblDoc_details) AS numberofrows "
        "FROM quotation_tbldoc_details "
        "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
        "ON "
        "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "
        "WHERE docid_tbldoc_details_id=%s "
        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
        [docid])
    results = cursor4.fetchall()

    for instancesingle in results:
        docdetailscount = instancesingle[0]

    cursor5 = connection.cursor()
    cursor5.execute("SELECT id, "
                    "first_name, "
                    "last_name, "
                    "email, "
                    "subscriptiontext_tblauth_user "
                    "FROM auth_user "
                    "WHERE id=%s ", [creatorid])
    creatordata = cursor5.fetchall()

    return render(request, 'quotation/purchaseorderprint.html', {'doc': doc, 'docdetails': docdetails,
                                                             'docdetailscount': docdetailscount,
                                                             'creatordata': creatordata})
def purchaseorderemail(request, docid):
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "docid_tbldoc, "
                    "email_tblcontacts_ctbldoc, "
                    "creatorid_tbldoc, "
                    "pretag_tbldockind, "
                    "Doc_kind_name_tblDoc_kind, "
                    "docnumber_tbldoc, "
                    "subject_tbldoc, "
                    "title_tblcontacts_ctbldoc, "
                    "lastname_tblcontacts_ctbldoc, "
                    "emailbodytextmodifiedbyuser_tbldoc "
                    "FROM quotation_tbldoc "
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                    "WHERE docid_tbldoc=%s ",
                    [docid])
    doc = cursor1.fetchall()
    for x in doc:
        creatorid = x[2]
        pretag = x[3]
        dockindname = x[4]
        docnumber = x[5]
        subject = x[6]

    #import pdb;
    #pdb.set_trace()

    cursor10 = connection.cursor()
    cursor10.execute("SELECT id, "
                     "first_name, "
                     "last_name, "
                     "email, "
                     "subscriptiontext_tblauth_user, "
                     "emailbodytext_tblauth_user "
                     "FROM auth_user "
                    "WHERE id=%s ", [creatorid])
    creatordata = cursor10.fetchall()
    for x in creatordata:
        emailbodytext = x[5]

    pdffilename = dockindname + '_' + pretag + str(docnumber) + '_Subject:_' + subject + '.pdf'
    os.system('google-chrome --headless --print-to-pdf='+ pdffilename + ' http://127.0.0.1:8000/quotation/quotationprint/' + docid + '/')

    return render(request, 'quotation/emailadd.html', {'doc': doc,
                                                       'pdffilename': pdffilename,
                                                       'emailbodytext': emailbodytext,
                                                       'creatordata': creatordata
                                                       })
def purchaseorderrowremove(request, pk):
    cursor2 = connection.cursor()
    cursor2.execute(
        "SELECT Docid_tblDoc_details_id FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [pk])
    results = cursor2.fetchall()
    for x in results:
        na = x[0]
    transaction.commit()

    cursor1 = connection.cursor()
    cursor1.execute(
        "DELETE FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [pk])
    transaction.commit()

    return redirect('purchaseorderform', pk=na)
def purchaseorderbackpage(request):


    if request.method == 'POST':
        purchaseorderid = request.POST['purchaseorderid']
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT "
        "Docid_tblDoc, "
        "backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
        "docnumber_tbldoc, "
        "creatorid_tbldoc, "
        "deliverydays_tbldoc "
        "FROM quotation_tbldoc "
        "WHERE docid_tbldoc=%s ",
        [purchaseorderid])

    doc = cursor0.fetchall()
    json_data = json.dumps(doc)

    return HttpResponse(json_data, content_type="application/json")
