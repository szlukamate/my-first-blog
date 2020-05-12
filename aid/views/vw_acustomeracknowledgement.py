from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required, user_passes_test
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

# import pdb;
# pdb.set_trace()
def group_required(group_name, login_url=None):
    """
    Decorator for views that checks whether a user belongs to a particular
    group, redirecting to the log-in page if necessary.
    """
    def check_group(user):
        # First check if the user belongs to the group
        if user.groups.filter(name=group_name).exists():
            return True
    return user_passes_test(check_group, login_url=login_url)

@group_required("manager")
@login_required
def acustomeracknowledgementform(request, pk):

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
#            import pdb;
#            pdb.set_trace()

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
                    "Docid_tblaDoc, "
                    "Contactid_tblaDoc_id, "
                    "Doc_kindid_tblaDoc_id, "
                    "companyname_tblcompanies_ctbladoc, "
                    "firstname_tblcontacts_ctbladoc, "
                    "lastname_tblcontacts_ctbladoc, "
                    "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                    "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                    "prefacespecforquotation_tbladoc, "
                    "subject_tbladoc, "
                    "docnumber_tbladoc, "#10
                    "creatorid_tbladoc, "
                    "creationtime_tbladoc, "
                    "title_tblcontacts_ctbladoc, "
                    "mobile_tblcontacts_ctbladoc, "
                    "email_tblcontacts_ctbladoc, "
                    "pcd_tblcompanies_ctbladoc, "
                    "town_tblcompanies_ctbladoc, "
                    "address_tblcompanies_ctbladoc, "
                    "total_tbladoc, "
                    "deliverydays_tbladoc, "#20
                    "paymenttextforquotation_tblpayment_ctbladoc, "
                    "currencycodeinreport_tbladoc, "
                    "currencyrateinreport_tbladoc, "
                    "accountcurrencycode_tbladoc, "
                    "pretag_tbladockind, "
                    "deferredpaymentdaysinquotation_tbladoc "

                    "FROM aid_tbladoc as D "
                    "JOIN aid_tbladoc_kind as DK ON D.Doc_kindid_tblaDoc_id = DK.Doc_kindid_tblaDoc_kind "
                    "WHERE docid_tbladoc=%s "
                    "order by docid_tbladoc desc",
                    [pk])
    doc = cursor1.fetchall()
    for x in doc:
        contactid = x[1]
        creatorid = x[11]

    cursor4 = connection.cursor()
    cursor4.execute("SELECT companyid_tblacontacts_id "
                    "FROM aid_tblacontacts "
                    "WHERE Contactid_tblaContacts=%s ", [contactid])
    companyid = cursor4.fetchall()

    cursor3 = connection.cursor()
    cursor3 = connection.cursor()
    # if there is not such product already not show goto

    cursor3.execute("SELECT  `Doc_detailsid_tblaDoc_details`, "
                    "`Qty_tblaDoc_details`, "
                    "`Docid_tblaDoc_details_id`, "
                    "`customerdescription_tblProduct_ctblaDoc_details`, "
                    "`firstnum_tblaDoc_details`, "
                    "`fourthnum_tblaDoc_details`, "
                    "`secondnum_tblaDoc_details`, "
                    "`thirdnum_tblaDoc_details`, "
                    "`Note_tblaDoc_details`, "
                    "`creationtime_tblaDoc_details`, "
                    "purchase_price_tblproduct_ctblaDoc_details, "
                    "listprice_tblaDoc_details, "
                    "currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details, "
                    "Productid_tblaDoc_details_id, "
                    "Doc_detailsid_tblaDoc_details, "
                    "COALESCE(Productid_tblaProduct, 0), "
                    "currencyrate_tblcurrency_ctblaDoc_details, "
                    "round((((listprice_tblaDoc_details-purchase_price_tblproduct_ctblaDoc_details)/(listprice_tblaDoc_details))*100),1) as listpricemargin, "
                    "unitsalespriceACU_tblaDoc_details, "
                    "round((purchase_price_tblproduct_ctblaDoc_details * currencyrate_tblcurrency_ctblaDoc_details),2) as purchasepriceACU, "
                    "round((((unitsalespriceACU_tblaDoc_details-(purchase_price_tblproduct_ctblaDoc_details * currencyrate_tblcurrency_ctblaDoc_details))/(unitsalespriceACU_tblaDoc_details))*100),1) as unitsalespricemargin, "
                    "round((listprice_tblaDoc_details * currencyrate_tblcurrency_ctblaDoc_details),2) as listpriceACU, "
                    "(100-round(((unitsalespriceACU_tblaDoc_details/(listprice_tblaDoc_details * currencyrate_tblcurrency_ctblaDoc_details))*100),1)) as discount, "
                    "unit_tbladocdetails, "
                    "companyname_tblacompanies, "
                    "supplierdescription_tblProduct_ctblaDoc_details "

                    "FROM aid_tbladoc_details as DD "

                    "LEFT JOIN (SELECT Productid_tblaProduct FROM aid_tblaproduct WHERE obsolete_tblaproduct = 0) as x ON DD.Productid_tblaDoc_details_id = x.Productid_tblaProduct "
                    "JOIN aid_tblacompanies as C ON DD.suppliercompanyid_tbladocdetails = C.companyid_tblacompanies "
                    "WHERE docid_tbladoc_details_id=%s "

                    "order by firstnum_tblaDoc_details,secondnum_tblaDoc_details,thirdnum_tblaDoc_details,fourthnum_tblaDoc_details",
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
        "SELECT currencyid_tblacurrency, currencyisocode_tblacurrency FROM aid_tblacurrency")
    currencycodes = cursor3.fetchall()
    transaction.commit()


    cursor5 = connection.cursor()
    cursor5.execute("SELECT `firstnum_tblaDoc_details`, "
                    "`secondnum_tblaDoc_details`,`thirdnum_tblaDoc_details`,`fourthnum_tblaDoc_details` "

                    "FROM aid_tbladoc_details "

                    "WHERE docid_tbladoc_details_id=%s "
                    "order by firstnum_tblaDoc_details desc,secondnum_tblaDoc_details desc,thirdnum_tblaDoc_details desc,fourthnum_tblaDoc_details desc "
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

    return render(request, 'aid/acustomeracknowledgement.html', {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums' : nextchapternums,
                                                        'creatordata': creatordata,
                                                        'currencycodes': currencycodes})
