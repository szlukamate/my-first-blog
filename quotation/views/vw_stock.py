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
        "customerdescription_tblProduct_ctblDoc_details, "
        "DD.Productid_tblDoc_details_id, "
        "supplierdescription_tblProduct_ctblDoc_details, "
        "onstockingoing.onstockingoingqty as onstockingoing, "
        "onstockoutgoing.onstockoutgoingqty as onstockoutgoing, "
        "COALESCE(onstockingoing.onstockingoingqty,0)-COALESCE(onstockoutgoing.onstockoutgoingqty,0) as onstock "

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

        "WHERE obsolete_tbldoc=0 and Doc_kindid_tblDoc_id=2 "
        "GROUP BY   customerdescription_tblProduct_ctblDoc_details, "
        "           DD.Productid_tblDoc_details_id, "
        "           supplierdescription_tblProduct_ctblDoc_details, "
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


