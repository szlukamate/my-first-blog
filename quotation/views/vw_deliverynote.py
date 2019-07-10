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
import time

# import pdb;
# pdb.set_trace()


def deliverynoteform(request, pk):
        if request.method == "POST":
                fieldvalue = request.POST['fieldvalue']
                rowid = request.POST['rowid']
                docid = request.POST['docid']
                fieldname = request.POST['fieldname']
                tbl = request.POST['tbl']
                if tbl == "tblDoc_details":
                        cursor22 = connection.cursor()
                        cursor22.callproc("spquotationdocdetailsfieldsupdate", [fieldname, fieldvalue, rowid])
                        results23 = cursor22.fetchall()
                        print(results23)
                        #import pdb;
                        #pdb.set_trace()

                        json_data = json.dumps(results23)

                        return HttpResponse(json_data, content_type="application/json")

                elif tbl == "tblDoc":
                        cursor22 = connection.cursor()
                        cursor22.callproc("spquotationdocfieldsupdate", [fieldname, fieldvalue, docid])
                        results23 = cursor22.fetchall()
                        print(results23)

                        json_data = json.dumps(results23)

                        return HttpResponse(json_data, content_type="application/json")

        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "D.Docid_tblDoc, "
                        "D.Contactid_tblDoc_id, "
                        "D.Doc_kindid_tblDoc_id, "
                        "D.companyname_tblcompanies_ctbldoc, "
                        "D.firstname_tblcontacts_ctbldoc, "
                        "D.lastname_tblcontacts_ctbldoc, "
                        "D.prefacetextforquotation_tblprefaceforquotation_ctbldoc, "
                        "D.backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
                        "D.prefacespecforquotation_tbldoc, "
                        "D.subject_tbldoc, "
                        "D.docnumber_tbldoc, "
                        "D.creatorid_tbldoc, "
                        "D.creationtime_tbldoc, "
                        "D.title_tblcontacts_ctbldoc, "
                        "D.mobile_tblcontacts_ctbldoc, "
                        "D.email_tblcontacts_ctbldoc, "
                        "D.pcd_tblcompanies_ctbldoc, "
                        "D.town_tblcompanies_ctbldoc, "
                        "D.address_tblcompanies_ctbldoc, "
                        "D.total_tbldoc, "
                        "D.deliverydays_tbldoc, "
                        "D.paymenttextforquotation_tblpayment_ctbldoc, "
                        "D.currencycodeinreport_tbldoc, "
                        "D.currencyrateinreport_tbldoc, "
                        "D.accountcurrencycode_tbldoc, "
                        "pretag_tbldockind, " #25
                        "D.wherefromdocid_tbldoc, "
                        "D.wheretodocid_tbldoc, "
                        "Dfrom.companyname_tblcompanies_ctbldoc as companywherefromdeno, "
                        "Dto.companyname_tblcompanies_ctbldoc as companywheretodeno, "
                        "D.stocktakingdeno_tbldoc, " #30
                        "D.denoenabledflag_tbldoc "

                        "FROM quotation_tbldoc as D "
                        "JOIN quotation_tbldoc_kind as DK ON D.Doc_kindid_tblDoc_id = DK.Doc_kindid_tblDoc_kind "
                        "LEFT JOIN quotation_tbldoc as Dfrom "
                        "ON D.wherefromdocid_tbldoc = Dfrom.docid_tbldoc "
                        "LEFT JOIN quotation_tbldoc as Dto "
                        "ON D.wheretodocid_tbldoc = Dto.docid_tbldoc "
                        "WHERE D.docid_tbldoc=%s "
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
                        "round((((unitsalespriceACU_tblDoc_details-(purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details))/(unitsalespriceACU_tblDoc_details))*100),1) as unitsalespricemargin, " #20
                        "round((listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as listpriceACU, "
                        "(100-round(((unitsalespriceACU_tblDoc_details/(listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details))*100),1)) as discount, "
                        "unit_tbldocdetails, "
                        "companyname_tblcompanies, "
                        "supplierdescription_tblProduct_ctblDoc_details, "
                        "IF (serviceflag_tblproduct=1, 0, podocdetailsidforlabel_tbldocdetails) "
#                        "serviceflag_tblproduct "
                        
                        "FROM quotation_tbldoc_details as DD "
                        
                        "LEFT JOIN quotation_tblproduct as P "
                        "ON DD.Productid_tblDoc_details_id = P.Productid_tblProduct "
                        
                        "JOIN quotation_tblcompanies as C "
                        "ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "
                        
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

        if maxfourthnum == 0:
                if maxthirdnum == 0:
                        if maxsecondnum == 0:
                                nextchapternums[0] = nextchapternums[0] + 1
                        else:
                                nextchapternums[1] = nextchapternums[1] + 1
                else:
                        nextchapternums[2] = nextchapternums[2] + 1
        else:
                nextchapternums[3] = nextchapternums[3] + 1

        return render(request, 'quotation/deliverynote.html',{'doc': doc,
                                                              'docdetails': docdetails,
                                                              'companyid': companyid,
                                                              'nextchapternums': nextchapternums,
                                                              'creatordata': creatordata,
                                                              'currencycodes': currencycodes})

def deliverynoteprint(request, docid):
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

    return render(request, 'quotation/deliverynoteprint.html', {'doc': doc, 'docdetails': docdetails,
                                                             'docdetailscount': docdetailscount,
                                                             'creatordata': creatordata})
def deliverynotebackpage(request):


    if request.method == 'POST':
        deliverynoteid = request.POST['deliverynoteid']
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
        [deliverynoteid])

    doc = cursor0.fetchall()
    json_data = json.dumps(doc)

    return HttpResponse(json_data, content_type="application/json")
def deliverynotepre(request):

    customerorderid = request.POST['customerorderid']
    selectedstockid = request.POST['selectedstockid']

    cursor44 = connection.cursor()
    cursor44.execute(
        "SELECT  "
        "Companyid_tblCompanies, "
        "companyname_tblcompanies "
        
        "FROM quotation_tblcompanies "
        
        "WHERE Companyid_tblCompanies=%s",
        [selectedstockid])
    stockdetails = cursor44.fetchall()
# stockresults to temptable start
    cursor222 = connection.cursor()
    cursor222.execute("DROP TEMPORARY TABLE IF EXISTS stockresultstemp;")
    cursor222.execute("CREATE TEMPORARY TABLE IF NOT EXISTS stockresultstemp "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     stockid INT(11) NOT NULL, "
                    "     productid INT(11) NULL, " 
                    "     labelid INT(11) NULL, "
                    "     inqty DECIMAL(10,1) NULL,"
                    "     outqty DECIMAL(10,1) NULL)"
                    "      ENGINE=INNODB "
                    "    ; ")

    cursor222.callproc("spstock", [])
    docdetailsstock = cursor222.fetchall()


    for x in docdetailsstock:
        stockid = x[6]
        productid = x[1]
        labelid = x[3]
        inqty = x[4]
        outqty = x[5]

        if outqty == None:
            outqty=0.0

        cursor222.execute("INSERT INTO stockresultstemp "
                        "(stockid, "
                        "productid, "
                        "labelid, "
                        "inqty,"
                        "outqty) VALUES ('" + str(stockid) + "', "
                                                    "'" + str(productid) + "', "
                                                    "'" + str(labelid) + "', "
                                                    "'" + str(inqty) + "', "
                                                    "'" + str(outqty) + "');")

    #import pdb;
    #pdb.set_trace()

    # stockresults to temptable end


    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT "
        "customerdescription_tblProduct_ctblDoc_details, "
        "DD.Productid_tblDoc_details_id, "
        "supplierdescription_tblProduct_ctblDoc_details, "
        "COALESCE(sum(DD.Qty_tblDoc_details), 0) as ordered, "
        "COALESCE(sum(Denod.denodqty), 0) as denod "
#        "COALESCE(sum(onstockingoing.onstockingoingqty), 0) as onstockingoing, "
#        "COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0) as onstockoutgoing, "
#        "COALESCE(sum(onstockingoing.onstockingoingqty), 0)-COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0) as onstock " #7

        "FROM quotation_tbldoc_details as DD "

#denod        
        "LEFT JOIN (SELECT "
        "           wheretodocid_tbldoc, "
        "           sum(DD2.denodqty) as denodqty, "
        "           DD2.Productid_tblDoc_details_id as productid "
        
        "           FROM quotation_tbldoc "
        
        "           LEFT JOIN   (SELECT "
        "                       Docid_tblDoc_details_id as docid, "
        "                       sum(Qty_tblDoc_details) as denodqty, "
        "                       Productid_tblDoc_details_id "
 
        "                       FROM quotation_tbldoc_details"
                                    
        "                       GROUP BY docid, Productid_tblDoc_details_id  "
        "                       ) as DD2 "
        "           ON quotation_tbldoc.Docid_tblDoc = DD2.docid "

        "           WHERE obsolete_tbldoc = 0 "
        "           GROUP BY wheretodocid_tbldoc, productid "
        "           ) AS Denod "
        "ON (DD.Docid_tblDoc_details_id = Denod.wheretodocid_tbldoc and DD.Productid_tblDoc_details_id = Denod.productid) "

        "WHERE docid_tbldoc_details_id=%s "

        "GROUP BY   customerdescription_tblProduct_ctblDoc_details, "
        "           DD.Productid_tblDoc_details_id, "
        "           supplierdescription_tblProduct_ctblDoc_details ",
        [customerorderid])

    docdetailspre = cursor3.fetchall()
#    todocdetailspre = []
    todocdetails = []
    docdetails = []

    for instancesingle in docdetailspre:
        customerdescription = instancesingle[0]
        productid = instancesingle[1]
        supplierdescription = instancesingle[2]
        ordered = instancesingle[3]
        denod = instancesingle[4]

        cursor222.execute("SELECT "

                        "COALESCE(sum(inqty),0.0), "
                        "COALESCE(sum(outqty),0.0) "
                          
                        "FROM stockresultstemp "
                          
                        " WHERE stockid=%s and productid=%s ",
                        [selectedstockid, productid])
        stockresultstemps = cursor222.fetchall()

        for instancesingle in stockresultstemps:
            inqty = instancesingle[0]
            outqty = instancesingle[1]

        #import pdb;
        #pdb.set_trace()

        onstock = inqty - outqty

        if ordered <= denod:
            todeno = 0.0
        else:
            if ordered <= onstock:
                todeno = ordered-denod
            else:
                todeno = onstock

#        if ordered <= denod, 0.0, ( if ordered <= onstock, ordered-ondeno, onstock)

#        appendvar = (customerdescription, productid, supplierdescription, ordered, denod, onstockingoing, onstockoutgoing, onstock, todeno )
        appendvar = (productid, customerdescription, supplierdescription, ordered, denod, todeno, inqty, outqty, onstock )
        todocdetails.append(appendvar)

    docdetails = todocdetails

    #import pdb;
    #pdb.set_trace()


    rowsnumber = len(docdetails)
    customerordernumber = customerorderid
    return render(request, 'quotation/deliverynotepre.html', {'docdetails': docdetails,
                                                              'customerordernumber': customerordernumber,
                                                              'stockdetails': stockdetails,
                                                              'rowsnumber': rowsnumber})


def deliverynotepredelete(request):
    customerorderid = request.POST['customerorderid']
    selectedstockid = request.POST['selectedstockid']

    cursor44 = connection.cursor()
    cursor44.execute(
        "SELECT  "
        "Companyid_tblCompanies, "
        "companyname_tblcompanies "

        "FROM quotation_tblcompanies "

        "WHERE Companyid_tblCompanies=%s",
        [selectedstockid])
    stockdetails = cursor44.fetchall()

    # import pdb;
    # pdb.set_trace()

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT "
        "customerdescription_tblProduct_ctblDoc_details, "
        "DD.Productid_tblDoc_details_id, "
        "supplierdescription_tblProduct_ctblDoc_details, "
        "COALESCE(sum(DD.Qty_tblDoc_details), 0) as ordered, "
        "COALESCE(sum(Denod.denodqty), 0) as denod, "
        "COALESCE(sum(onstockingoing.onstockingoingqty), 0) as onstockingoing, "
        "COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0) as onstockoutgoing, "
        "COALESCE(sum(onstockingoing.onstockingoingqty), 0)-COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0) as onstock "  # 7

        "FROM quotation_tbldoc_details as DD "

        # denod        
        "LEFT JOIN (SELECT "
        "           wheretodocid_tbldoc, "
        "           sum(DD2.denodqty) as denodqty, "
        "           DD2.Productid_tblDoc_details_id as productid "

        "           FROM quotation_tbldoc "

        "           LEFT JOIN   (SELECT "
        "                       Docid_tblDoc_details_id as docid, "
        "                       sum(Qty_tblDoc_details) as denodqty, "
        "                       Productid_tblDoc_details_id "

        "                       FROM quotation_tbldoc_details"

        "                       GROUP BY docid, Productid_tblDoc_details_id  "
        "                       ) as DD2 "
        "           ON quotation_tbldoc.Docid_tblDoc = DD2.docid "

        "           WHERE obsolete_tbldoc = 0 "
        "           GROUP BY wheretodocid_tbldoc, productid "
        "           ) AS Denod "
        "ON (DD.Docid_tblDoc_details_id = Denod.wheretodocid_tbldoc and DD.Productid_tblDoc_details_id = Denod.productid) "
        # ingoing

        "LEFT JOIN (SELECT "
        "           D2.wheretodocid_tbldoc as wheretodocid, "
        "           sum(onstockingoing2.onstockingoingqty) as onstockingoingqty, "
        "           onstockingoing2.productid as productid, "
        "           D3.Contactid_tblDoc_id as contactid2 "

        "           FROM quotation_tbldoc D2 "

        "JOIN (SELECT "
        "      Docid_tblDoc_details_id as docid, "
        "      sum(Qty_tblDoc_details) as onstockingoingqty, "
        "      Productid_tblDoc_details_id as productid "

        "      FROM quotation_tbldoc_details "

        "      GROUP BY docid, productid "
        "     ) AS onstockingoing2 "
        "           ON D2.Docid_tblDoc = onstockingoing2.docid "

        "LEFT JOIN quotation_tbldoc as D3"  # D3 contains all where wheredoc is not null
        "           ON D2.wheretodocid_tbldoc = D3.Docid_tblDoc"

        "           WHERE D2.obsolete_tbldoc = 0 and D3.Contactid_tblDoc_id=9 "
        "           GROUP BY D2.wheretodocid_tbldoc, "
        "                       productid, "
        "                       contactid2 "

        "           ) AS onstockingoing "
        "ON (DD.Productid_tblDoc_details_id = onstockingoing.productid) "
        # outgoing

        "LEFT JOIN (SELECT "
        "           wherefromdocid_tbldoc, "
        "           sum(onstockoutgoing2.onstockoutgoingqty) as onstockoutgoingqty, "
        "           onstockoutgoing2.productid as productid "

        "           FROM quotation_tbldoc "

        "LEFT JOIN (SELECT "
        "           Docid_tblDoc_details_id as docid, "
        "           sum(Qty_tblDoc_details) as onstockoutgoingqty, "
        "           Productid_tblDoc_details_id as productid "

        "           FROM quotation_tbldoc_details "

        "           GROUP BY docid, productid "
        "           ) AS onstockoutgoing2 "
        "           ON quotation_tbldoc.Docid_tblDoc = onstockoutgoing2.docid "

        "           WHERE obsolete_tbldoc = 0 "
        "           GROUP BY wherefromdocid_tbldoc, productid "

        "           ) AS onstockoutgoing "
        "ON (788 = onstockoutgoing.wherefromdocid_tbldoc and DD.Productid_tblDoc_details_id = onstockoutgoing.productid) "

        "WHERE docid_tbldoc_details_id=%s "
        "GROUP BY   customerdescription_tblProduct_ctblDoc_details, "
        "           DD.Productid_tblDoc_details_id, "
        "           supplierdescription_tblProduct_ctblDoc_details ",
        #        "           onstockingoing, "
        #        "           onstockoutgoing, "
        #        "           onstock ",
        [customerorderid])

    docdetailspre = cursor3.fetchall()
    #    todocdetailspre = []
    todocdetails = []
    docdetails = []

    for instancesingle in docdetailspre:
        customerdescription = instancesingle[0]
        productid = instancesingle[1]
        supplierdescription = instancesingle[2]
        ordered = instancesingle[3]
        denod = instancesingle[4]
        onstockingoing = instancesingle[5]
        onstockoutgoing = instancesingle[6]
        onstock = instancesingle[7]

        if ordered <= denod:
            todeno = 0.0
        else:
            if ordered <= onstock:
                todeno = ordered - denod
            else:
                todeno = onstock

        #        if ordered <= denod, 0.0, ( if ordered <= onstock, ordered-ondeno, onstock)

        appendvar = (
        customerdescription, productid, supplierdescription, ordered, denod, onstockingoing, onstockoutgoing, onstock,
        todeno)
        todocdetails.append(appendvar)

    docdetails = todocdetails

    # import pdb;
    # pdb.set_trace()

    rowsnumber = len(docdetails)
    customerordernumber = customerorderid
    return render(request, 'quotation/deliverynotepre.html', {'docdetails': docdetails,
                                                              'customerordernumber': customerordernumber,
                                                              'stockdetails': stockdetails,
                                                              'rowsnumber': rowsnumber})




def deliverynotemake(request): #from deliverynotepre form (buttonpress comes here)
    customerordernumber = request.POST['customerordernumber']
    selectedstockid = request.POST['selectedstockid']
    productidlistraw = request.POST['productidlist']
    productidlist = json.loads(productidlistraw)

    cursor44 = connection.cursor()
    cursor44.execute(
        "SELECT  Docid_tblDoc, "
        "        lateststocktaking.companyid "

        "FROM quotation_tbldoc "

        "JOIN (SELECT "
                         "lateststocktaking_tblcompanies as lateststocktaking, " 
                         "C.Companyid_tblContacts_id as companyid, " 
                         "C.Contactid_tblContacts as contactid "  

                         "FROM quotation_tblcontacts as C "

                         "JOIN quotation_tblcompanies as companies "
                         "ON C.Companyid_tblContacts_id = companies.Companyid_tblCompanies "

                   ") as lateststocktaking "
        "ON quotation_tbldoc.Contactid_tblDoc_id = lateststocktaking.contactid "


        "WHERE lateststocktaking.companyid=%s and denoenabledflag_tbldoc=1 and stocktakingdeno_tbldoc=1 and obsolete_tbldoc=0 ",
        [selectedstockid])
    results = cursor44.fetchall()

    for instancesingle in results:
        laststocktakingdocid = instancesingle[0]
    # import pdb;
    # pdb.set_trace()

    creatorid = request.user.id

    cursor2 = connection.cursor()
    cursor2.execute("DROP TEMPORARY TABLE IF EXISTS denofromstock;")
    cursor2.execute("CREATE TEMPORARY TABLE IF NOT EXISTS denofromstock "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     productid INT(11) NOT NULL, "
                    "     productqty INT(11) NULL DEFAULT 12) "
                    "      ENGINE=INNODB "
                    "    ; ")

    for x11 in range(0,len(productidlist),2):
        productid = productidlist[x11+0]
        productqty = productidlist[x11+1]

        cursor2.execute("INSERT INTO denofromstock "
                        "(productid, productqty) VALUES ('" + str(productid) + "', "
                                            "'" + str(productqty) + "');")


    cursor2.execute("SELECT *  "
                    "FROM denofromstock ")
    tables = cursor2.fetchall()
    #import pdb;
    #pdb.set_trace()

    pk = customerordernumber
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
                    "accountcurrencycode_tbldoc, "

                    "companyname_tblcompanies_ctbldoc, "
                    "firstname_tblcontacts_ctbldoc, "
                    "lastname_tblcontacts_ctbldoc, "
                    "title_tblcontacts_ctbldoc, "
                    "mobile_tblcontacts_ctbldoc, "
                    "email_tblcontacts_ctbldoc, "
                    "pcd_tblcompanies_ctbldoc, "
                    "town_tblcompanies_ctbldoc, "  # 20
                    "address_tblcompanies_ctbldoc "

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

        companynameclone = x[13]
        firstnameclone = x[14]
        lastnameclone = x[15]
        titleclone = x[16]
        mobileclone = x[17]
        emailclone = x[18]
        pcdclone = x[19]
        townclone = x[20]
        addressclone = x[21]

        #import pdb;
        #pdb.set_trace()

    cursor8 = connection.cursor()
    cursor8.execute("SELECT max(docnumber_tblDoc) FROM quotation_tbldoc "
                    "WHERE Doc_kindid_tblDoc_id = 8")
    results = cursor8.fetchall()
    resultslen = len(results)

    if results[0][0] is not None:  # only if there is not doc yet (this would be the first instance)
        for x in results:
            docnumber = x[0]
            docnumber += 1
    else:
        docnumber = 80  # arbitrary number

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
                    "accountcurrencycode_tbldoc, "
                    "wherefromdocid_tbldoc, " 
                    "wheretodocid_tbldoc,"
                    "denoenabledflag_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [8, contactid,
                     companynameclone,
                     firstnameclone,
                     lastnameclone,
                     prefacetext,
                     backpagetext,
                     prefacespectext,
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
                     customerordernumber,
                     accountcurrencycode,
                     laststocktakingdocid,
                     customerordernumber,
                     1])

    cursor3 = connection.cursor()
    cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
    results = cursor3.fetchall()
    for x in results:
        maxdocid = x[0]

    for x3 in tables:
        productid = x3[1]
        productqty = x3[2]

        cursor3 = connection.cursor()
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
                        "unit_tbldocdetails, "  # 23
                        "suppliercompanyid_tbldocdetails, "
                        "supplierdescription_tblProduct_ctblDoc_details "

                        "FROM quotation_tbldoc_details "

                        "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                        "ON "
                        "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "

                        "JOIN quotation_tbldoc as D "
                        "ON D.Docid_tblDoc=quotation_tbldoc_details.Docid_tblDoc_details_id "

                        "WHERE Docid_tblDoc_details_id=%s and Productid_tblDoc_details_id=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details LIMIT 1",
                        [customerordernumber, productid])
        docdetails = cursor3.fetchall()

        for x in docdetails:
            denotopodetailslink = x[0]
#            qty = x[1]

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
            #the product get service and discreteflags start

            cursor3 = connection.cursor()
            cursor3.execute("SELECT serviceflag_tblproduct, "
                            "       discreteflag_tblproduct "
                            "FROM quotation_tblproduct "
                            "WHERE Productid_tblProduct=%s", [productid])
            results = cursor3.fetchall()
            for x in results:
                serviceflag = x[0]
                discreteflag = x[1]

            #the product get service and discreteflags end

            # oldestlabelid determination start
            def oldestlabel():

                cursor0 = connection.cursor()
                cursor0.execute(
                    "SELECT "
                    "DDingoing.podocdetailsidforlabel_tbldocdetails as labelid, "
                    "sum(DDingoing.Qty_tblDoc_details) as inqty, "
                    #            "sum(DDoutgoing.outqty) as outqty, "
                    #            "COALESCE(sum(DDingoing.Qty_tblDoc_details),0)-COALESCE(sum(DDoutgoing.outqty),0) as onstock 
                    "D4.contactid as contactid "

                    "FROM quotation_tbldoc_details as DDingoing "

                    #            "LEFT JOIN (SELECT podocdetailsidforlabel_tbldocdetails as outlabel, "
                    #            "           Docid_tblDoc_details_id, "
                    #            "           sum(Qty_tblDoc_details) as outqty "

                    #            "           FROM quotation_tbldoc_details as DD2 "

                    #            "           JOIN quotation_tbldoc as D2"
                    #            "           ON DD2.Docid_tblDoc_details_id = D2.Docid_tblDoc "
                    #            "           WHERE obsolete_tbldoc=0 and wherefromdocid_tbldoc=788 and Productid_tblDoc_details_id=%s "
                    #            "           GROUP BY outlabel, Docid_tblDoc_details_id "

                    #            "           ) as DDoutgoing "
                    #            "ON DDingoing.podocdetailsidforlabel_tbldocdetails = DDoutgoing.outlabel " #and outqty <> DDoutgoing.outqty "

                    "JOIN (SELECT "
                    "       D.Docid_tblDoc, "
                    "       D2.Contactid_tblDoc_id as contactid, "
                    "       D.obsolete_tbldoc as obsolete"
                    ""
                    "       FROM quotation_tbldoc as D "

                    "JOIN quotation_tbldoc as D2 "  # contactid lookup
                    "ON D.wheretodocid_tblDoc = D2.Docid_tblDoc "
                    "       WHERE D2.Contactid_tblDoc_id=9 "

                    "     ) as D4 "

                    "ON DDingoing.Docid_tblDoc_details_id = D4.Docid_tblDoc "

                    "WHERE D4.obsolete=0 and DDingoing.Productid_tblDoc_details_id=%s   "
                    "GROUP BY labelid, contactid "
                    "order by DDingoing.podocdetailsidforlabel_tbldocdetails desc "
                    , [productid])

                resultspre = cursor0.fetchall()
                toresults = []
                results = []

                for instancesingle in resultspre:
                    labelid = instancesingle[0]
                    inqty = instancesingle[1]
#                    outqty = instancesingle[2]
#                    onstockqty = instancesingle[3]

                    if inqty > 0:
                        productqtyoldestlabel = inqty
                        podocdetailsidforlabel = labelid
                        break
                    else:
                        productqtyoldestlabel = 'nomore'
                        podocdetailsidforlabel = 'nomore'



                #import pdb;
                #pdb.set_trace()

                return productqtyoldestlabel, podocdetailsidforlabel
            # oldestlabelid determination end

            def docdetailsinsert(productqtyoldestlabel, podocdetailsidforlabel):

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
                    "denotopodetailslink_tbldocdetails, "
                    "supplierdescription_tblProduct_ctblDoc_details, "
                    "podocdetailsidforlabel_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

                    [maxdocid,
                     productqtyoldestlabel,
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
                     denotopodetailslink,
                     supplierdescriptionclone,
                     podocdetailsidforlabel])
            #import pdb;
            #pdb.set_trace()
                return
            if discreteflag == 0: #indiscrete
                productqtyoldestlabel, podocdetailsidforlabel = oldestlabel()
                if productqty <= productqtyoldestlabel:
                    docdetailsinsert(productqty, podocdetailsidforlabel)
                    remnantqty = 0

                #                    import pdb;
#                    pdb.set_trace()

                else:
                    docdetailsinsert(productqtyoldestlabel, podocdetailsidforlabel)
                    remnantqty = productqty - productqtyoldestlabel
                    #import pdb;
                    #pdb.set_trace()

                while remnantqty > 0:
                    productqtyoldestlabel, podocdetailsidforlabel = oldestlabel()
                    #import pdb;
                    #pdb.set_trace()

#                    time.sleep(2)
                    print(remnantqty)
                    if productqtyoldestlabel == 'nomore':
                        break


                    if remnantqty <= productqtyoldestlabel:
                        docdetailsinsert(remnantqty, podocdetailsidforlabel)
                        remnantqty = 0
                    else:
                        docdetailsinsert(productqtyoldestlabel, podocdetailsidforlabel)
                        remnantqty = remnantqty - productqtyoldestlabel

 #                   import pdb;
 #                   pdb.set_trace()

            else: #discrete
                for x6 in range(productqty):
                    productqtyoldestlabel, podocdetailsidforlabel = oldestlabel()
                    docdetailsinsert(1, podocdetailsidforlabel)

    return render(request, 'quotation/deliverynotepreredirecturl.html', {'pk': pk})
def deliverynotenewrowadd(request):
    if request.method == "POST":
        docdetailsid = request.POST['docdetailsid']
        deliverynoteid = request.POST['deliverynoteid']
        nextfirstnumonhtml= request.POST['nextfirstnumonhtml']
        nextsecondnumonhtml = request.POST['nextsecondnumonhtml']
        nextthirdnumonhtml = request.POST['nextthirdnumonhtml']
        nextfourthnumonhtml = request.POST['nextfourthnumonhtml']

        nextchapternumset = array('i', [int(nextfirstnumonhtml), int(nextsecondnumonhtml), int(nextthirdnumonhtml), int(nextfourthnumonhtml)])

    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT Productid_tblProduct, "
        "purchase_price_tblproduct, "
        "margin_tblproduct, "
        "round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as listprice, "
        "customerdescription_tblProduct, "
        "currencyisocode_tblcurrency_ctblproduct, "
        "supplierdescription_tblProduct "
        "FROM quotation_tblproduct "
        "WHERE obsolete_tblproduct=0 ")
    products = cursor1.fetchall()
    transaction.commit()
    #return redirect('quotationform', pk=1)

    return render(request, 'quotation/deliverynotenewrowadd.html',{'products': products, 'docid': deliverynoteid, 'nextchapternumset': nextchapternumset, 'docdetailsid' : docdetailsid })
def deliverynotenewrow(request, pkdocid, pkproductid, pkdocdetailsid, nextfirstnumonhtml, nextsecondnumonhtml,
                    nextthirdnumonhtml, nextfourthnumonhtml):
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT `Productid_tblProduct`, "
        "`purchase_price_tblproduct`, `"
        "customerdescription_tblProduct`, "
        "`margin_tblproduct`, "
        "`currencyisocode_tblcurrency_ctblproduct`, "
        "currencyrate_tblcurrency, "
        "unit_tblproduct, "
        "supplierdescription_tblProduct, "
        "suppliercompanyid_tblProduct "
        "FROM `quotation_tblproduct` "
        "LEFT JOIN quotation_tblcurrency "
        "ON quotation_tblproduct.currencyisocode_tblcurrency_ctblproduct=quotation_tblcurrency.currencyisocode_tblcurrency "
        "WHERE Productid_tblProduct= %s", [pkproductid])
    results = cursor0.fetchall()
    for instancesingle in results:
        purchase_priceclone = instancesingle[1]
        customerdescriptionclone = instancesingle[2]
        currencyisocodeclone = instancesingle[4]
        marginfromproducttable = instancesingle[3]
        listpricecomputed = round((100 * purchase_priceclone) / (100 - marginfromproducttable), 2)
        currencyrateclone = instancesingle[5]
        unitclone = instancesingle[6]
        supplierdescriptionclone = instancesingle[7]
        suppliercompanyidclone = instancesingle[8]

        unitsalespriceACU = listpricecomputed * currencyrateclone
    # import pdb;
    # pdb.set_trace()

    if int(pkdocdetailsid) != 0:  # only modifying row
        cursor2 = connection.cursor()
        cursor2.execute(
            "UPDATE quotation_tbldoc_details SET "
            "Productid_tblDoc_details_id= %s, "
            "firstnum_tblDoc_details=%s, "
            "secondnum_tblDoc_details=%s, "
            "thirdnum_tblDoc_details=%s, "
            "fourthnum_tblDoc_details=%s, "
            "purchase_price_tblproduct_ctblDoc_details=%s, "
            "customerdescription_tblProduct_ctblDoc_details=%s, "
            "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details=%s, "
            "listprice_tblDoc_details=%s, "
            "currencyrate_tblcurrency_ctblDoc_details=%s, "
            "unitsalespriceACU_tblDoc_details=%s, "
            "unit_tbldocdetails=%s, "
            "supplierdescription_tblProduct_ctblDoc_details=%s, "
            "suppliercompanyid_tblDocdetails=%s "
            "WHERE doc_detailsid_tbldoc_details =%s ",
            [pkproductid, nextfirstnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml, nextfourthnumonhtml,
             purchase_priceclone, customerdescriptionclone, currencyisocodeclone, listpricecomputed, currencyrateclone,
             unitsalespriceACU,
             unitclone,
             supplierdescriptionclone,
             suppliercompanyidclone,
             pkdocdetailsid])

    else:
        cursor1 = connection.cursor()  # new row needed
        cursor1.execute(
            "INSERT INTO quotation_tbldoc_details "
            "(`Qty_tblDoc_details`, "
            "`Docid_tblDoc_details_id`, "
            "`Productid_tblDoc_details_id`, "
            "`firstnum_tblDoc_details`, "
            "`fourthnum_tblDoc_details`, "
            "`secondnum_tblDoc_details`, "
            "`thirdnum_tblDoc_details`, "
            "`Note_tblDoc_details`, "
            "`purchase_price_tblproduct_ctblDoc_details`, "
            "`customerdescription_tblProduct_ctblDoc_details`, "
            "`currencyisocode_tblcurrency_ctblproduct_ctblDoc_details`, "
            "listprice_tblDoc_details, "
            "currencyrate_tblcurrency_ctblDoc_details, "
            "unitsalespriceACU_tblDoc_details, "
            "unit_tbldocdetails, "
            "`supplierdescription_tblProduct_ctblDoc_details`, "
            "suppliercompanyid_tblDocdetails) "

            "VALUES (1, %s, %s, %s,%s,%s,%s,'Defaultnote', %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [pkdocid, pkproductid, nextfirstnumonhtml, nextfourthnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml,
             purchase_priceclone, customerdescriptionclone, currencyisocodeclone,
             listpricecomputed,
             currencyrateclone,
             unitsalespriceACU,
             unitclone,
             supplierdescriptionclone,
             suppliercompanyidclone])
        transaction.commit()

    return redirect('deliverynoteform', pk=pkdocid)
def deliverynoterowremove(request, pk):
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

    return redirect('deliverynoteform', pk=na)
def deliverynotenewlabel(request):
    newlabelid = request.POST['newlabelid']
#    deliverynotedocid = request.POST['deliverynotedocid']

    cursor3 = connection.cursor()
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
                    "suppliercompanyid_tbldocdetails, "
                    "podetailslink_tbldocdetails "

                    "FROM quotation_tbldoc_details "

                    "JOIN quotation_tbldoc as D "
                    "ON quotation_tbldoc_details.Docid_tblDoc_details_id = D.Docid_tblDoc "

                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                    "ON "
                    "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "

                    "WHERE Doc_detailsid_tblDoc_details=%s and Doc_kindid_tblDoc_id=7 and obsolete_tbldoc=0 "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [newlabelid])
    docdetails = cursor3.fetchall()
    docdetailslen = len(docdetails)
    if docdetailslen != 0:

        for x in docdetails:
            productid = x[13]


            cursor5 = connection.cursor()
            cursor5.execute("SELECT  "
                            "discreteflag_tblproduct, "
                            "serviceflag_tblproduct "
                            ""
                            "FROM quotation_tblproduct "
                            ""
                            "WHERE Productid_tblProduct=%s ",
                            [productid])
            docdetails2 = cursor5.fetchall()
            # import pdb;
            # pdb.set_trace()


            for x in docdetails2:
                discreteflag = x[0]
                serviceflag = x[1]
            if serviceflag == 0:
                if discreteflag == 1:

                    parametertostocktaking = 'discreteproduct'

                else:
                    parametertostocktaking = 'indiscreteproduct'
            else:
                parametertostocktaking = 'serviceproduct'
    else:


        parametertostocktaking = 'noneproduct'





#    pk=deliverynotedocid

    return render(request, 'quotation/deliverynoteparameterstostocktaking.html', {'parametertostocktaking': parametertostocktaking})
def deliverynoteafternewlabel(request):
    newlabelid = request.POST['newlabelid']
    deliverynotedocid = request.POST['deliverynotedocid']
    indiscreteqty = request.POST['indiscreteqty']
    parametertostocktaking = request.POST['parametertostocktaking']
    #import pdb;
    #pdb.set_trace()

    cursor3 = connection.cursor()
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
                    "suppliercompanyid_tbldocdetails, "
                    "podetailslink_tbldocdetails "

                    "FROM quotation_tbldoc_details "

                    "JOIN quotation_tbldoc as D "
                    "ON quotation_tbldoc_details.Docid_tblDoc_details_id = D.Docid_tblDoc "

                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                    "ON "
                    "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "

                    "WHERE Doc_detailsid_tblDoc_details=%s and Doc_kindid_tblDoc_id=7 "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [newlabelid])
    docdetails = cursor3.fetchall()

    for x in docdetails:
#        qty = x[1]
        firstnum = x[4]
        fourthnum = x[5]
        secondnum = x[6]
        thirdnum = x[7]
        note = x[8]
        productid = x[13]
        currencyrate = x[16]
        suppliercompanyid = x[24]
        podetailslink = x[25]

        purchase_priceclone = x[10]
        customerdescriptionclone = x[3]
        currencyisocodeclone = x[12]
        listpricecomputed = x[11]
        currencyrateclone = x[16]
        unitclone = x[23]
        unitsalespriceACU = x[18]

    if parametertostocktaking == 'discreteproduct':
        qty = 1.0
    elif parametertostocktaking == 'indiscreteproduct':
        qty = indiscreteqty

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
        "podocdetailsidforlabel_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

        [int(deliverynotedocid),
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
         int(newlabelid)])


        #import pdb;
        #pdb.set_trace()






    pk=deliverynotedocid

    return render(request, 'quotation/deliverynotenewlabelredirecturl.html', {'pk': pk})


def deliverynotechoosestock(request):  # labels on stockform for particular product
    productid = request.POST['productid']

    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT "
        "discreteflag_tblproduct "

        "FROM quotation_tblproduct as P "

        "WHERE Productid_tblProduct=%s "
        , [productid])

    results22 = cursor1.fetchall()
    for x14 in results22:
        discreteflag = x14[0]

        cursor0 = connection.cursor()
        cursor0.execute(
            "SELECT "
            "Dingoing.inlabel as labelid, "
            "Dingoing.inqty as inqty, "
            "DDoutgoing.outqty as outqty, "
            "COALESCE(Dingoing.inqty,0)-COALESCE(DDoutgoing.outqty,0) as onstock "

            "FROM quotation_tbldoc_details as DD "
            # ingoing
            "JOIN (SELECT "
            "       D.Docid_tblDoc as docid, "
            "       DDingoing.inlabel as inlabel, "
            "       D.obsolete_tbldoc as obsolete, "
            "       sum(DDingoing.inqty) as inqty "
            ""
            "       FROM quotation_tbldoc as D "
            "   "
            "JOIN (SELECT podocdetailsidforlabel_tbldocdetails as inlabel, "
            "           Docid_tblDoc_details_id, "
            "           sum(Qty_tblDoc_details) as inqty "

            "           FROM quotation_tbldoc_details as DD2 "

            "           JOIN quotation_tbldoc as D2"
            "           ON DD2.Docid_tblDoc_details_id = D2.Docid_tblDoc "

            "           WHERE D2.obsolete_tbldoc=0 "
            "           GROUP BY inlabel, Docid_tblDoc_details_id "

            "           ) as DDingoing "
            "ON D.Docid_tblDoc = DDingoing.Docid_tblDoc_details_id "


            "JOIN quotation_tbldoc as D2 "  # contactid lookup
            "ON D.wheretodocid_tblDoc = D2.Docid_tblDoc "

            "       WHERE D2.Contactid_tblDoc_id=9 and D2.obsolete_tbldoc = 0 "
            "           GROUP BY docid, "
            "                       inlabel, "
            "                       obsolete "
            ""

            "     ) as Dingoing "

            "ON DD.Docid_tblDoc_details_id = Dingoing.docid "

            # outgoing    
            "LEFT JOIN (SELECT podocdetailsidforlabel_tbldocdetails as outlabel, "
            "           Docid_tblDoc_details_id, "
            "           sum(Qty_tblDoc_details) as outqty "

            "           FROM quotation_tbldoc_details as DD2 "

            "           JOIN quotation_tbldoc as D2"
            "           ON DD2.Docid_tblDoc_details_id = D2.Docid_tblDoc "

            "           WHERE obsolete_tbldoc=0 and wherefromdocid_tbldoc=788  "
            "           GROUP BY outlabel, Docid_tblDoc_details_id "

            "           ) as DDoutgoing "
            "ON DD.podocdetailsidforlabel_tbldocdetails = DDoutgoing.outlabel "  # and outqty <> DDoutgoing.outqty "

            "JOIN quotation_tbldoc as D "
            "ON DD.Docid_tblDoc_details_id = D.Docid_tblDoc "


            "WHERE DD.Productid_tblDoc_details_id=%s and D.obsolete_tbldoc=0   "
            "GROUP BY labelid, inqty, outqty, onstock  "
            "order by labelid desc "
            , [productid])

        resultspre = cursor0.fetchall()
        toresults = []
        results = []

        for instancesingle in resultspre:
            labelid = instancesingle[0]
            inqty = instancesingle[1]
            outqty = instancesingle[2]
            onstockqty = instancesingle[3]

            if onstockqty > 0:
                appendvar = (
                    labelid, inqty, outqty, onstockqty)
                toresults.append(appendvar)

        results = toresults

    return render(request, 'quotation/ajax_stocklabellist.html', {'results': results, 'productid': productid})
