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
                        "Dto.companyname_tblcompanies_ctbldoc as companywheretodeno "

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
def deliverynotepre(request, docid):

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT "
        "customerdescription_tblProduct_ctblDoc_details, "
        "DD.Productid_tblDoc_details_id, "
        "supplierdescription_tblProduct_ctblDoc_details, "
        "COALESCE(sum(Qty_tblDoc_details), 0) as ordered, "
        "COALESCE(sum(Denod.denodqty), 0) as denod, "
        "COALESCE(sum(onstockingoing.onstockingoingqty), 0) as onstockingoing, "
        "COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0) as onstockoutgoing, "
        "COALESCE(sum(onstockingoing.onstockingoingqty), 0)-COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0) as onstock, "
        "IF((COALESCE(sum(Qty_tblDoc_details), 0))<=(COALESCE(sum(onstockingoing.onstockingoingqty), 0)-COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0)), COALESCE(sum(Qty_tblDoc_details), 0), (COALESCE(sum(onstockingoing.onstockingoingqty), 0)-COALESCE(sum(onstockoutgoing.onstockoutgoingqty), 0)))" # if ordered<=onstock, ordered, onstock

        "FROM quotation_tbldoc_details as DD "

        
        "LEFT JOIN (SELECT "
        "           wheretodocid_tbldoc, "
        "           DD2.denodqty as denodqty, "
        "           DD2.Productid_tblDoc_details_id as productid"
        
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
        "           ) AS Denod "
        "ON (DD.Docid_tblDoc_details_id = Denod.wheretodocid_tbldoc and DD.Productid_tblDoc_details_id = Denod.productid) "
#ingoing

        "LEFT JOIN (SELECT "
        "           wheretodocid_tbldoc, "
        "           onstockingoing2.onstockingoingqty as onstockingoingqty, "
        "           onstockingoing2.productid as productid "
        
        "           FROM quotation_tbldoc "

                    "LEFT JOIN (SELECT "
                    "           Docid_tblDoc_details_id as docid, "
                    "           sum(Qty_tblDoc_details) as onstockingoingqty, "
                    "           Productid_tblDoc_details_id as productid "
                    
                    "           FROM quotation_tbldoc_details "
            
                    "           GROUP BY docid, productid "
                    "           ) AS onstockingoing2 "
        "           ON quotation_tbldoc.Docid_tblDoc = onstockingoing2.docid "

        "           WHERE obsolete_tbldoc = 0 "
        "           ) AS onstockingoing "
        "ON (788 = onstockingoing.wheretodocid_tbldoc and DD.Productid_tblDoc_details_id = onstockingoing.productid) "
#outgoing
        "LEFT JOIN (SELECT "
        "           wherefromdocid_tbldoc, "
        "           onstockoutgoing2.onstockoutgoingqty as onstockoutgoingqty, "
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
        "           ) AS onstockoutgoing "
        "ON (788 = onstockoutgoing.wherefromdocid_tbldoc and DD.Productid_tblDoc_details_id = onstockoutgoing.productid) "


        "WHERE docid_tbldoc_details_id=%s "
        "GROUP BY   customerdescription_tblProduct_ctblDoc_details, "
        "           DD.Productid_tblDoc_details_id, "
        "           supplierdescription_tblProduct_ctblDoc_details ",
        [docid])
    docdetails = cursor3.fetchall()
    rowsnumber = len(docdetails)

    return render(request, 'quotation/deliverynotepre.html', {'docdetails': docdetails,
                                                              'rowsnumber': rowsnumber})


def deliverynotemake(request):
    customerordernumber = request.POST['customerordernumber']
    productidlistraw = request.POST['productidlist']
    productidlist = json.loads(productidlistraw)


    creatorid = request.user.id

    cursor2 = connection.cursor()
    cursor2.execute("DROP TEMPORARY TABLE IF EXISTS denofromstock;")
    cursor2.execute("CREATE TEMPORARY TABLE IF NOT EXISTS denofromstock "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     productid INT(11) NOT NULL, "
                    "     productqty INT(11) NULL DEFAULT 12) "
                    "      ENGINE=INNODB "
                    "    ; ")

    for x11 in range(len(productidlist)):
        productid = productidlist[x11+0]

        cursor2.execute("INSERT INTO denofromstock "
                        "(productid) VALUES ('" + str(productid) + "');")


    cursor2.execute("SELECT *  "
                    "FROM denofromstock ")
    tables = cursor2.fetchall()

    import pdb;
    pdb.set_trace()

    for xx in tables:
        auxid = xx[0]
        podocid = xx[2]
        cordocid = xx[3]
        cursor2.execute("SELECT count(auxid) "
                        "FROM porows "
                        "WHERE podocid=%s and cordocid=%s "
                        "GROUP BY podocid, cordocid ", [podocid, cordocid])
        numberofitemstodenoresults = cursor2.fetchall()

        for x2 in numberofitemstodenoresults:
            numberofitemstodeno = x2[0]

        cursor2.execute("UPDATE porows SET "
                        "numberofitemstodeno= %s "
                        "WHERE auxid =%s ", [numberofitemstodeno, auxid])

    cursor2.execute("SELECT *  "
                    "FROM porows ")
    tables2 = cursor2.fetchall()
    docmakercounter = 0

    for x3 in tables2:
        podocdetailsid = x3[1]
        podocid = x3[2]
        cordocid = x3[3]
        numberofitemstodeno = x3[5]

        if docmakercounter == 0:
            docmakercounter = numberofitemstodeno

            pk = 60
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
                # import pdb;
                # pdb.set_trace()

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
                            "wheretodocid_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
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
                             cordocid,
                             accountcurrencycode,
                             podocid,
                             cordocid])

            #    cursor8 = connection.cursor()
            #    cursor8.execute("SELECT Doc_detailsid_tblDoc_details "
            #                    "FROM quotation_tbldoc_details "
            #                    "WHERE dateofarrival_tbldocdetails = %s",
            #                    [dateofarrival])
            #    docdetailstodeno = cursor8.fetchall()

            cursor3 = connection.cursor()
            cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
            results = cursor3.fetchall()
            for x in results:
                maxdocid = x[0]

        docmakercounter -= 1

        cursor2.execute("SELECT  `Doc_detailsid_tblDoc_details`, "
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

                        "WHERE obsolete_tbldoc=0 and Doc_detailsid_tblDoc_details=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                        [podocdetailsid])
        docdetails = cursor2.fetchall()
        # import pdb;
        # pdb.set_trace()

        for x in docdetails:
            denotopodetailslink = x[0]
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
                "denotopodetailslink_tbldocdetails, "
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
                 denotopodetailslink,
                 supplierdescriptionclone])

    return render(request, 'quotation/pohandlerreceptionredirecturl.html', {})
