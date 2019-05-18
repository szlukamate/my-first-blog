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
def pohandlerframe(request):

    return render(request, 'quotation/pohandlerframe.html', {})

def pohandlerfieldsupdate(request):
    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        fieldname = request.POST['fieldname']
        cursor22 = connection.cursor()
        cursor22.callproc("sppohandlerfieldsupdate", [fieldname, fieldvalue, rowid])
        results23 = cursor22.fetchall()
        print(results23)
        #import pdb;
        #pdb.set_trace()

        json_data = json.dumps(results23, indent=4, sort_keys=True, default=str)

        return HttpResponse(json_data, content_type="application/json")
def pohandlersearchresults(request):
#    docnumber = request.POST['docnumber']
#    dockindname = request.POST['dockindname']
    fromdate = request.POST['fromdate']
    todate = request.POST['todate']
#    company = request.POST['company']


#    if docnumber != '':
#        docnumber = "and docnumber_tbldoc='" + docnumber + "' "
#    if dockindname != '':
#        dockindname = "and Doc_kind_name_tblDoc_kind='" + dockindname + "' "

    #datephrase = "and creationtime_tbldoc BETWEEN '" + fromdate + "' and '" + todate + "' "
    datephrase = "and DATE(creationtime_tbldoc) >= '" + fromdate + "' and DATE(creationtime_tbldoc) <= '" + todate + "' "
    #datephrase = "and DATE(creationtime_tbldoc) = '2019-04-19'"

#    if company != '':
#        company = "and companyname_tblcompanies_ctbldoc='" + company + "'"

    #import pdb;
    #pdb.set_trace()
    searchphrase= datephrase + " "


    cursor3 = connection.cursor()
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
                    "DD.supplierdescription_tblProduct_ctblDoc_details, "  # 25
    
                    "DD2.cordocdetailsid, "
                    "DD2.cordocid, "
                    "DD2.cordetailsqty, "
                    "DD2.cordocnumber, "
                    "DD2.corpretag, "
                    "DD2.corcompany, "  # 31
    
                    "DD.dateofarrival_tbldocdetails, "
                    "companyname_tblcompanies_ctbldoc as supplier,"
                    "Docid_tblDoc as podocid, "
                    "pretag_tbldockind as popretag, "
                    "docnumber_tbldoc as podocnumber, "
                    "DD.denotopodetailslink_tbldocdetails "    
    
                    "FROM quotation_tbldoc_details as DD "
    
                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x ON DD.Productid_tblDoc_details_id = x.Productid_tblProduct "
                    "JOIN quotation_tblcompanies as C ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "
    
                    "JOIN quotation_tbldoc "
                    "ON quotation_tbldoc.Docid_tblDoc=DD.Docid_tblDoc_details_id "
    
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
    
                    "JOIN (SELECT (Doc_detailsid_tblDoc_details) as cordocdetailsid, "
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
    
                    "WHERE Doc_kindid_tblDoc_id=7 and obsolete_tbldoc = 0 "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details")
    pos = cursor3.fetchall()
    #    import pdb;
    #    pdb.set_trace()

    return render(request, 'quotation/pohandler.html', {'pos': pos})
def pohandlerrowsourceforarrivaldates(request):
    cursor0 = connection.cursor()
    cursor0.execute(
            "SELECT dateofarrival_tbldocdetails "
            "FROM quotation_tbldoc_details as DD "
    
            "JOIN quotation_tbldoc "
            "ON quotation_tbldoc.Docid_tblDoc=DD.Docid_tblDoc_details_id "
    
            "WHERE dateofarrival_tbldocdetails is not null and obsolete_tbldoc = 0 "
            "GROUP BY dateofarrival_tbldocdetails "
            "ORDER BY dateofarrival_tbldocdetails desc")

    arrivaldates = cursor0.fetchall()

    rownmbs=len(arrivaldates)
    #import pdb;
    #pdb.set_trace()

    return render(request, 'quotation/pohandlerrowsourceforarrivaldates.html', {'arrivaldates': arrivaldates, 'rownmbs': rownmbs})


def pohandlerreception(request):
    dateofarrival = request.POST['dateofarrival']

    creatorid = request.user.id

    pk=60
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
                    "accountcurrencycode_tbldoc " #12

                    "companyname_tblcompanies_ctbldoc, "
                    "firstname_tblcontacts_ctbldoc, "
                    "lastname_tblcontacts_ctbldoc, "
                    "title_tblcontacts_ctbldoc, "
                    "mobile_tblcontacts_ctbldoc, "
                    "email_tblcontacts_ctbldoc, "
                    "pcd_tblcompanies_ctbldoc, "
                    "town_tblcompanies_ctbldoc, "
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

        companynameclone = x[12]
 #       companyid = instancesingle[2]
        firstnameclone = x[13]
        lastnameclone = x[14]
        titleclone = x[15]
        mobileclone = x[16]
        emailclone = x[17]
        pcdclone = x[18]
        townclone = x[19]
        addressclone = x[20]

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
                    "accountcurrencycode_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
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
                     pk,
                     accountcurrencycode])

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
                    "WHERE dateofarrival_tbldocdetails = %s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [dateofarrival])
    docdetails = cursor3.fetchall()

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

    return render(request, 'quotation/pohandlerreceptionredirecturl.html',{})



