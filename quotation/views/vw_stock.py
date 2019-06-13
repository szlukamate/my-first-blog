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

def stockmain(request):

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT "
        "P.customerdescription_tblProduct, "
        "DD.Productid_tblDoc_details_id, "
        "supplierdescription_tblProduct, "
        "onstockingoing.onstockingoingqty as onstockingoing, "
        "onstockoutgoing.onstockoutgoingqty as onstockoutgoing, "
        "COALESCE(onstockingoing.onstockingoingqty,0)-COALESCE(onstockoutgoing.onstockoutgoingqty,0) as onstock, "
        "unit_tblproduct, "
        "purchase_price_tblproduct, "
        "margin_tblproduct, "
        "round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as listprice, "
        "companyname_tblcompanies as supplier, " #10
        "currencyisocode_tblcurrency_ctblproduct "
        

        "FROM quotation_tbldoc_details as DD "

        
#ingoing

        "LEFT JOIN (SELECT "
        "           wheretodocid_tbldoc, "
        "           sum(onstockingoing2.onstockingoingqty) as onstockingoingqty, "
        "           onstockingoing2.productid as productid "
        
        "           FROM quotation_tbldoc "

                    "JOIN (SELECT "
                    "           Docid_tblDoc_details_id as docid, "
                    "           sum(Qty_tblDoc_details) as onstockingoingqty, "
                    "           Productid_tblDoc_details_id as productid "
                    
                    "           FROM quotation_tbldoc_details "
            
                    "           GROUP BY docid, productid "
                    "           ) AS onstockingoing2 "
        "           ON quotation_tbldoc.Docid_tblDoc = onstockingoing2.docid "

        "           WHERE obsolete_tbldoc = 0 "
        "           GROUP BY wheretodocid_tbldoc, productid "

        "           ) AS onstockingoing "
        "ON (788 = onstockingoing.wheretodocid_tbldoc and DD.Productid_tblDoc_details_id = onstockingoing.productid) "
#outgoing
        "LEFT JOIN (SELECT "
        "           wherefromdocid_tbldoc, "
        "           sum(onstockoutgoing2.onstockoutgoingqty) as onstockoutgoingqty, "
        "           onstockoutgoing2.productid as productid "
       
        "           FROM quotation_tbldoc "

                    "JOIN (SELECT "
                    "           Docid_tblDoc_details_id as docid, "
                    "           sum(Qty_tblDoc_details) as onstockoutgoingqty, "
                    "           Productid_tblDoc_details_id as productid "
                    
                    "           FROM quotation_tbldoc_details "
            
                    "           GROUP BY docid, productid "
                    "           ) AS onstockoutgoing2 "
        "           ON quotation_tbldoc.Docid_tblDoc = onstockoutgoing2.docid "

                    "WHERE obsolete_tbldoc=0 "
        "           GROUP BY wherefromdocid_tbldoc, productid "

        "           ) AS onstockoutgoing "
        "ON (788 = onstockoutgoing.wherefromdocid_tbldoc and DD.Productid_tblDoc_details_id = onstockoutgoing.productid) "

        "LEFT JOIN quotation_tbldoc "
        "ON DD.Docid_tblDoc_details_id = quotation_tbldoc.Docid_tblDoc "

        "LEFT JOIN quotation_tblproduct as P "
        "ON DD.Productid_tblDoc_details_id = P.Productid_tblProduct "

        "JOIN quotation_tblcompanies "
        "ON companyid_tblcompanies = suppliercompanyid_tblproduct "

        "WHERE obsolete_tbldoc=0 and Doc_kindid_tblDoc_id=2 "
        "GROUP BY   DD.Productid_tblDoc_details_id, "
        "           supplierdescription_tblProduct, "
        "           onstockingoing, "
        "           onstockoutgoing ")

    docdetails = cursor3.fetchall()
    #import pdb;
    #pdb.set_trace()

    rowsnumber = len(docdetails)
    customerordernumber = 1
    return render(request, 'quotation/stock.html', {'docdetails': docdetails,
                                                              'customerordernumber': customerordernumber,
                                                              'rowsnumber': rowsnumber})
def stocklabellist(request):
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
            "DDingoing.podocdetailsidforlabel_tbldocdetails as labelid, "
            "sum(DDingoing.Qty_tblDoc_details) as inqty, "
            "sum(DDoutgoing.outqty) as outqty, "
            "COALESCE(sum(DDingoing.Qty_tblDoc_details),0)-COALESCE(sum(DDoutgoing.outqty),0) as onstock "
    
            "FROM quotation_tbldoc_details as DDingoing "
    
            "LEFT JOIN (SELECT podocdetailsidforlabel_tbldocdetails as outlabel, "
            "           Docid_tblDoc_details_id, "
            "           sum(Qty_tblDoc_details) as outqty "
    
            "           FROM quotation_tbldoc_details as DD2 "
    
            "           JOIN quotation_tbldoc as D2"
            "           ON DD2.Docid_tblDoc_details_id = D2.Docid_tblDoc "
            "           WHERE obsolete_tbldoc=0 and wherefromdocid_tbldoc=788 and Productid_tblDoc_details_id=%s "
            "           GROUP BY outlabel, Docid_tblDoc_details_id "
            
            "           ) as DDoutgoing "
            "ON DDingoing.podocdetailsidforlabel_tbldocdetails = DDoutgoing.outlabel " #and outqty <> DDoutgoing.outqty "
    
            "LEFT JOIN quotation_tbldoc as D "
            "ON DDingoing.Docid_tblDoc_details_id = D.Docid_tblDoc "
    
            "WHERE obsolete_tbldoc=0 and wheretodocid_tbldoc=788 and DDingoing.Productid_tblDoc_details_id=%s " #and DDoutgoing.podocdetailsidforlabel_tbldocdetails is null "
            "GROUP BY labelid "
            "order by DDingoing.podocdetailsidforlabel_tbldocdetails desc "
            , [productid, productid])


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


