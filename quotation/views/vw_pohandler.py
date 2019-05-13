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
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "companyname_tblcompanies_ctbldoc "
                    "FROM quotation_tbldoc "
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                    "WHERE obsolete_tbldoc = 0 "
                    "GROUP BY companyname_tblcompanies_ctbldoc ")
    companies = cursor1.fetchall()

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Doc_kind_name_tblDoc_kind "
                    "FROM quotation_tbldoc "
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                    "WHERE obsolete_tbldoc = 0 "
                    "GROUP BY Doc_kind_name_tblDoc_kind ")
    dockindnames = cursor1.fetchall()

    return render(request, 'quotation/pohandlerframe.html', {'companies': companies,
                                                        'dockindnames':dockindnames})

def pohandler(request):
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
                    "DD2.corcompany, " #31
                    
                    "DD.dateofarrival_tbldocdetails, "
                    "companyname_tblcompanies_ctbldoc as supplier,"
                    "Docid_tblDoc as podocid "


                    "FROM quotation_tbldoc_details as DD "
                    
                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x ON DD.Productid_tblDoc_details_id = x.Productid_tblProduct "
                    "JOIN quotation_tblcompanies as C ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "

                    "JOIN quotation_tbldoc "
                    "ON quotation_tbldoc.Docid_tblDoc=DD.Docid_tblDoc_details_id "


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

