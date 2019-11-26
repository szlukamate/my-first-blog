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
def quotationform(request, pk):

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
                    "docnumber_tbldoc, "#10
                    "creatorid_tbldoc, "
                    "creationtime_tbldoc, "
                    "title_tblcontacts_ctbldoc, "
                    "mobile_tblcontacts_ctbldoc, "
                    "email_tblcontacts_ctbldoc, "
                    "pcd_tblcompanies_ctbldoc, "
                    "town_tblcompanies_ctbldoc, "
                    "address_tblcompanies_ctbldoc, "
                    "total_tbldoc, "
                    "deliverydays_tbldoc, "#20
                    "paymenttextforquotation_tblpayment_ctbldoc, "
                    "currencycodeinreport_tbldoc, "
                    "currencyrateinreport_tbldoc, "
                    "accountcurrencycode_tbldoc, "
                    "pretag_tbldockind, "
                    "deferredpaymentdaysinquotation_tbldoc "

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

    return render(request, 'quotation/quotation.html', {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums' : nextchapternums,
                                                        'creatordata': creatordata,
                                                        'currencycodes': currencycodes})
@group_required("manager")
@login_required
def quotationnewrow(request, pkdocid, pkproductid, pkdocdetailsid, nextfirstnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml, nextfourthnumonhtml ):
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
        marginfromproducttable=instancesingle[3]
        listpricecomputed=round((100*purchase_priceclone)/(100-marginfromproducttable),2)
        currencyrateclone=instancesingle[5]
        unitclone = instancesingle[6]
        supplierdescriptionclone = instancesingle[7]
        suppliercompanyidclone = instancesingle[8]

        unitsalespriceACU=listpricecomputed * currencyrateclone
    #import pdb;
    #pdb.set_trace()

    if int(pkdocdetailsid) != 0: # only modifying row
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
            "WHERE doc_detailsid_tbldoc_details =%s ", [pkproductid, nextfirstnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml, nextfourthnumonhtml,
                                                        purchase_priceclone,  customerdescriptionclone, currencyisocodeclone, listpricecomputed, currencyrateclone,
                                                        unitsalespriceACU,
                                                        unitclone,
                                                        supplierdescriptionclone,
                                                        suppliercompanyidclone,
                                                        pkdocdetailsid])

    else:
        cursor1 = connection.cursor() # new row needed
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
            [pkdocid, pkproductid, nextfirstnumonhtml, nextfourthnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml, purchase_priceclone, customerdescriptionclone, currencyisocodeclone,
             listpricecomputed,
             currencyrateclone,
             unitsalespriceACU,
             unitclone,
             supplierdescriptionclone,
             suppliercompanyidclone])
        transaction.commit()

    return redirect('quotationform', pk=pkdocid)
@group_required("manager")
@login_required
def quotationnewrowadd(request):
    if request.method == "POST":
        docdetailsid = request.POST['docdetailsid']
        quotationid = request.POST['quotationid']
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

    return render(request, 'quotation/quotationnewrowadd.html',{'products': products, 'docid': quotationid, 'nextchapternumset': nextchapternumset, 'docdetailsid' : docdetailsid })
@group_required("manager")
@login_required
def quotationrowremove(request, pk):
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

    return redirect('quotationform', pk=na)
@group_required("manager")
@login_required
def searchquotationcontacts(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
        docidinquotationjs = request.POST['docidinquotationjs']
    else:
        search_text = ""
    search_textmodified="%" + search_text + "%"
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT quotation_tblcontacts.contactid_tblcontacts, quotation_tblcompanies.companyname_tblcompanies,"
        "quotation_tblcontacts.firstname_tblcontacts, quotation_tblcontacts.lastname_tblcontacts "
        "FROM quotation_tblcontacts "
        "JOIN quotation_tblcompanies "
        "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
        "WHERE quotation_tblcompanies.companyname_tblcompanies like %s "
        "ORDER BY companyname_tblcompanies", [search_textmodified])

    results = cursor0.fetchall()
    transaction.commit()

    rownmbs=len(results)

    return render(request, 'quotation/ajax_search_quotation_contacts.html', {'results': results, 'rownmbs': rownmbs, 'docidinquotationjs': docidinquotationjs})
@group_required("manager")
@login_required
def quotationupdatecontact(request, pkdocid, pkcontactid):
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT quotation_tblcontacts.contactid_tblcontacts, quotation_tblcompanies.companyname_tblcompanies,"
        "quotation_tblcontacts.Firstname_tblcontacts, quotation_tblcontacts.lastname_tblcontacts, "
        "title_tblcontacts, "
        "mobile_tblcontacts, "
        "email_tblcontacts, "
        "pcd_tblcompanies, "
        "town_tblcompanies, "
        "address_tblcompanies "
        "FROM quotation_tblcontacts "
        "JOIN quotation_tblcompanies "
        "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
        "WHERE quotation_tblcontacts.contactid_tblcontacts= %s ", [pkcontactid])

    contactandcompanydata = cursor0.fetchall()
    for instancesingle in contactandcompanydata:
        companynameclone = instancesingle[1]
        firstnameclone = instancesingle[2]
        lastnameclone = instancesingle[3]
        titleclone = instancesingle[4]
        mobileclone = instancesingle[5]
        emailclone = instancesingle[6]
        pcdclone = instancesingle[7]
        townclone = instancesingle[8]
        addressclone = instancesingle[9]

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tbldoc SET "
                    "Contactid_tblDoc_id= %s, "
                    "companyname_tblcompanies_ctbldoc=%s, "
                    "firstname_tblcontacts_ctbldoc=%s, "
                    "lastname_tblcontacts_ctbldoc=%s, "
                    "title_tblcontacts_ctbldoc=%s, "
                    "mobile_tblcontacts_ctbldoc=%s, "
                    "email_tblcontacts_ctbldoc=%s, "
                    "pcd_tblcompanies_ctbldoc=%s, "
                    "town_tblcompanies_ctbldoc=%s, "
                    "address_tblcompanies_ctbldoc=%s "
                    "WHERE Docid_tblDoc =%s ", [pkcontactid, companynameclone, firstnameclone, lastnameclone,
                                                titleclone,
                                                mobileclone,
                                                emailclone,
                                                pcdclone,
                                                townclone,
                                                addressclone,
                                                pkdocid,])

    return redirect('quotationform', pk=pkdocid)

#@group_required("manager")
#@login_required
def quotationprint (request, docid):
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
        "purchase_price_tblproduct_ctblDoc_details, " #10
        "listprice_tblDoc_details, "
        "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
        "Productid_tblDoc_details_id, "
        "Doc_detailsid_tblDoc_details, "
        "unit_tbldocdetails, "
        "currencyrateinreport_tbldoc "
        "unitsalespriceACU_tblDoc_details, "
        "round((unitsalespriceACU_tblDoc_details/currencyrateinreport_tbldoc),2) as unitsalespricetoreport, "
        "round((unitsalespriceACU_tblDoc_details/currencyrateinreport_tbldoc),2)*Qty_tblDoc_details as salespricetoreport "
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



    return render(request, 'quotation/quotationprint.html', {'doc': doc, 'docdetails': docdetails,
                                                             'docdetailscount':docdetailscount,
                                                             'creatordata': creatordata})
@group_required("manager")
@login_required
def quotationuniversalselections (request):

    fieldvalue = request.POST['fieldvalue']
    quotationdocid = request.POST['quotationdocid']
    fieldname = request.POST['fieldname']

    cursor2 = connection.cursor()

    cursor2.execute("UPDATE quotation_tbldoc SET "
                    "" + fieldname + "= %s "
                    "WHERE Docid_tblDoc =%s ", [fieldvalue, quotationdocid])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT " + fieldname + " "
        "FROM quotation_tbldoc "
        "WHERE Docid_tblDoc =%s ", [quotationdocid])
    results = cursor3.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
@group_required("manager")
@login_required
def quotationbackpage(request):


    if request.method == 'POST':
        quotationid = request.POST['quotationid']
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
        [quotationid])

    doc = cursor0.fetchall()
    json_data = json.dumps(doc)

    return HttpResponse(json_data, content_type="application/json")
@group_required("manager")
@login_required
def quotationemail(request, docid):
    BASE_DIR = settings.BASE_DIR

#applicable ipaddress begin
    debugstate = settings.DEBUG

    if debugstate == True:
        wherephrase = 'ipaddressdebugtrue'
    else:
        wherephrase = 'ipaddressdebugfalse'

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "settingvalue_tblsettings "

                    "FROM quotation_tblsettings "

                    "WHERE settingname_tblsettings=%s ",
                    [wherephrase])
    results = cursor1.fetchall()
    for x in results:
        appliableipaddress = x[0]



    #import pdb;
    #pdb.set_trace()
# applicable ipaddress  end

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
    #import pdb;
    #pdb.set_trace()

    subprocess.call('if [ ! -d "' + BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '" ]; then mkdir ' + BASE_DIR + '/emailattachmentspre/' + str(creatorid) + '  ;else rm -rf ' + BASE_DIR + '/emailattachmentspre/' + str(creatorid) + ' && mkdir ' + BASE_DIR + '/emailattachmentspre/' + str(creatorid) + ';  fi', shell=True)
    subprocess.call('node ' + BASE_DIR + "/nodeapps/190809createpdf.js " + BASE_DIR + "/emailattachmentspre/" + str(creatorid) + '/ ' + pdffilename + ' ' + appliableipaddress + ' ' + docid +'', shell=True)

    return render(request, 'quotation/emailadd.html', {'doc': doc,
                                                       'pdffilename': pdffilename,
                                                       'emailbodytext': emailbodytext,
                                                       'creatordata': creatordata
                                                       })
@group_required("manager")
@login_required
def quotationsaveasmodern(request, pk):
    creatorid = request.user.id

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
            "WHERE contactid_tblcontacts =%s", [contactid])
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
                        "WHERE Doc_kindid_tblDoc_id = 1")
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
                        [1, contactid, companynameclone, firstnameclone, lastnameclone, prefacetext, backpagetext, prefacespectext,
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
                        "WHERE docid_tbldoc_details_id=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                        [pk])
        docdetails = cursor3.fetchall()
    for x in docdetails:
        qty = x[1]
        firstnum = x[4]
        fourthnum = x[5]
        secondnum = x[6]
        thirdnum = x[7]
        note = x[8]
        productid = x[13]
        currencyrate = x[16]
        suppliercompanyid = x[24]

        cursor0 = connection.cursor()
        cursor0.execute(
            "SELECT `Productid_tblProduct`, "
            "`purchase_price_tblproduct`, `"
            "customerdescription_tblProduct`, "
            "`margin_tblproduct`, "
            "`currencyisocode_tblcurrency_ctblproduct`, "
            "currencyrate_tblcurrency, "
            "unit_tblproduct "

            "FROM `quotation_tblproduct` "

            "LEFT JOIN quotation_tblcurrency "
            "ON quotation_tblproduct.currencyisocode_tblcurrency_ctblproduct=quotation_tblcurrency.currencyisocode_tblcurrency "

            "WHERE Productid_tblProduct= %s", [productid])
        results = cursor0.fetchall()
        for instancesingle in results:
            purchase_priceclone = instancesingle[1]
            customerdescriptionclone = instancesingle[2]
            currencyisocodeclone = instancesingle[4]

            marginfromproducttable = instancesingle[3]
            listpricecomputed = round((100 * purchase_priceclone) / (100 - marginfromproducttable), 2)
            currencyrateclone = instancesingle[5]
            unitclone = instancesingle[6]

            unitsalespriceACU = listpricecomputed * currencyrateclone

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
            "suppliercompanyid_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

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
             suppliercompanyid])
    return redirect('docselector', pk=maxdocid)
@group_required("manager")
@login_required
def quotationsaveasorder(request, pk):
    creatorid = request.user.id

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
        companynameclone = x[13]
        firstnameclone = x[14]
        lastnameclone = x[15]
        titleclone = x[16]
        mobileclone = x[17]
        emailclone = x[18]
        pcdclone = x[19]
        townclone = x[20]
        addressclone = x[21]


        cursor8 = connection.cursor()
        cursor8.execute("SELECT max(docnumber_tblDoc) FROM quotation_tbldoc "
                        "WHERE Doc_kindid_tblDoc_id = 2")
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
                        [2, contactid, companynameclone, firstnameclone, lastnameclone, prefacetext, backpagetext, prefacespectext,
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
                    "purchase_price_tblproduct_ctblDoc_details, " #10
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
                    "supplierdescription_tblProduct_ctblDoc_details " #25

                    "FROM quotation_tbldoc_details "

                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                    "ON "
                    "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "

                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [pk])
    docdetails = cursor3.fetchall()
    for x in docdetails:
        docdetailsid = x[0]
        qty = x[1]
        firstnum = x[4]
        fourthnum = x[5]
        secondnum = x[6]
        thirdnum = x[7]
        note = x[8]
        productid = x[13]
        currencyrate = x[16]
        suppliercompanyid = x[24]
        supplierdescriptionclone = x[25]

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
            "supplierdescription_tblProduct_ctblDoc_details, "
            "creatorid_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

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
             supplierdescriptionclone,
             creatorid])

        # update  redmine with ordereddetails begin
        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT max(Doc_detailsid_tblDoc_details) FROM quotation_tbldoc_details WHERE creatorid_tbldocdetails=%s",
            [creatorid])
        results = cursor3.fetchall()
        for x in results:
            maxdocdetailsid = x[0]

        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT pretag_tbldockind FROM quotation_tbldoc_kind WHERE Doc_kindid_tblDoc_kind = 2")
        results = cursor3.fetchall()
        for x in results:
            pretagfororder = x[0]

        # selecting timeentryid  for next query (#2 query) with the help of  quoteddocdetailsid
        cursor21 = connections['redmine'].cursor()
        cursor21.execute(
            "SELECT customized_id FROM custom_values WHERE custom_field_id = 4 and value = %s", [docdetailsid])
        results = cursor21.fetchall()
        for x in results:
            timeentryid = x[0]

        #2 query:
        cursor21 = connections['redmine'].cursor()
        cursor21.execute("UPDATE custom_values SET "
                        "value = %s "
                        "WHERE custom_field_id = 5 and customized_id = %s ", [maxdocdetailsid, timeentryid]) # 5 means this field in Redmine in custom_fields table

        # select orderdocnumber
        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT docnumber_tbldoc FROM quotation_tbldoc WHERE Docid_tblDoc=%s",
            [maxdocid])
        results = cursor3.fetchall()
        for x in results:
            orderdocnumber = x[0]

        assembleddocnumber = pretagfororder + str(orderdocnumber)

        cursor21 = connections['redmine'].cursor()
        cursor21.execute("UPDATE custom_values SET "
                        "value = %s "
                        "WHERE custom_field_id = 7 and customized_id = %s ", [assembleddocnumber, timeentryid]) # 7 means this field in Redmine in custom_fields table

        # update redmine with ordereddetails end

    return redirect('docselector', pk=maxdocid)
@group_required("manager")
@login_required
def quotationissuetrackingsystem(request):
    quotationid = request.POST['quotationid']
    # filtering options to Addfilter selectbox begin
    # Creates a list containing #h lists, each of #w items, all set to 0
    w, h = 2, 8;
    addfilterselectvaluesandoptions = [[0 for x in range(w)] for y in range(h)]

    addfilterselectvaluesandoptions[0][0] = 'Project Status'
    addfilterselectvaluesandoptions[0][1] = 'projectstatus'

    addfilterselectvaluesandoptions[1][0] = 'Quoted Docdetailsid'
    addfilterselectvaluesandoptions[1][1] = 'quoteddocdetailsid'

    addfilterselectvaluesandoptions[2][0] = 'Quoted Docnumber (with pretag)'
    addfilterselectvaluesandoptions[2][1] = 'quoteddocnumber'

    addfilterselectvaluesandoptions[3][0] = 'Activity Name'
    addfilterselectvaluesandoptions[3][1] = 'activityname'

    addfilterselectvaluesandoptions[4][0] = 'Date - Spent On'
    addfilterselectvaluesandoptions[4][1] = 'datespenton'

    addfilterselectvaluesandoptions[5][0] = 'Time Entry Id'
    addfilterselectvaluesandoptions[5][1] = 'timeentryid'

    addfilterselectvaluesandoptions[6][0] = 'Project Name'
    addfilterselectvaluesandoptions[6][1] = 'projectid'

    addfilterselectvaluesandoptions[7][0] = 'User Name'
    addfilterselectvaluesandoptions[7][1] = 'userid'

    # filtering options to Addfilter selectbox end

    #import pdb;
    #pdb.set_trace()


    return render(request, 'quotation/quotationtimeentries.html',{'docid': quotationid,
                                                                  'addfilterselectvaluesandoptions': addfilterselectvaluesandoptions})
@group_required("manager")
@login_required
def quotationissuetrackingsystemitemstoquotation(request):

    creatorid = request.user.id
    BASE_DIR = settings.BASE_DIR

    quotationdocid = request.POST['quotationdocid']
    quotationdocnumber = request.POST['quotationdocnumber']
    issuetrackingsystemnumberofitems = request.POST['issuetrackingsystemnumberofitems']
    itemdatalistraw = request.POST['itemdatalist']
    itemdatalist = json.loads(itemdatalistraw)

    for x in range(int(issuetrackingsystemnumberofitems)):

        timeentryid = itemdatalist[(9*x+0)]
        timeentryandissueid = itemdatalist[(9*x+1)]
        projectname = itemdatalist[9*x+2]
        username = itemdatalist[9*x+3]
        activityname = itemdatalist[9*x+4]
        hours = itemdatalist[9*x+5]
        comments = itemdatalist[9*x+6]
        spenton = itemdatalist[9*x+7]
        issuesubject = itemdatalist[9*x+8]

        firstnum = x + 1
        fourthnum = 0
        secondnum = 0
        thirdnum = 0
        note = 'Projectname: ' + projectname + '\nIssue Subject: ' + issuesubject + '\nSpent On: ' + spenton + '\nComment on Spent Time: ' + comments + '\nby ' + username + '\nTimeentry and Issue Id: ' + timeentryandissueid + ' '
# supplier  select begin
        if username == 'Redmine Admin':
            productid = 54
        elif username == 'ChiefGofri ChiefMaker':
            productid = 56
# supplier select end

        cursor0 = connection.cursor()
        cursor0.execute(
            "SELECT `Productid_tblProduct`, "
            "`purchase_price_tblproduct`, `"
            "customerdescription_tblProduct`, "
            "`margin_tblproduct`, "
            "`currencyisocode_tblcurrency_ctblproduct`, "
            "currencyrate_tblcurrency, " #5
            "unit_tblproduct,"
            "suppliercompanyid_tblproduct "

            "FROM `quotation_tblproduct` "

            "LEFT JOIN quotation_tblcurrency "
            "ON quotation_tblproduct.currencyisocode_tblcurrency_ctblproduct=quotation_tblcurrency.currencyisocode_tblcurrency "

            "WHERE Productid_tblProduct= %s", [productid])
        results = cursor0.fetchall()
        for instancesingle in results:
            purchase_priceclone = instancesingle[1]
            customerdescriptionclone = instancesingle[2]
            currencyisocodeclone = instancesingle[4]

            marginfromproducttable = instancesingle[3]
            listpricecomputed = round((100 * purchase_priceclone) / (100 - marginfromproducttable), 2)
            currencyrateclone = instancesingle[5]
            unitclone = instancesingle[6]
            suppliercompanyid = instancesingle[7]


            unitsalespriceACU = listpricecomputed * currencyrateclone


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
            "creatorid_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

            [quotationdocid,
             hours,
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
             currencyrateclone,
             unitsalespriceACU,
             unitclone,
             suppliercompanyid,
             creatorid])

        # update redmine table with docdetailsid begin
        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT max(Doc_detailsid_tblDoc_details) FROM quotation_tbldoc_details WHERE creatorid_tbldocdetails=%s",
            [creatorid])
        results = cursor3.fetchall()
        for x in results:
            maxdocdetailsid = x[0]

        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT max(Docid_tblDoc_details_id) FROM quotation_tbldoc_details WHERE creatorid_tbldocdetails=%s",
            [creatorid])
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT pretag_tbldockind FROM quotation_tbldoc_kind WHERE Doc_kindid_tblDoc_kind = 1")
        results = cursor3.fetchall()
        for x in results:
            pretagforquotation = x[0]
        #import pdb;
        #pdb.set_trace()

        cursor21 = connections['redmine'].cursor()
        cursor21.execute("UPDATE custom_values SET "
                        "value = %s "
                        "WHERE custom_field_id = 4 and customized_id = %s ", [maxdocdetailsid, timeentryid]) # 4 means this  field in Redmine in custom_fields table

        assembleddocnumber = pretagforquotation + str(quotationdocnumber)

        cursor21 = connections['redmine'].cursor()
        cursor21.execute("UPDATE custom_values SET "
                        "value = %s "
                        "WHERE custom_field_id = 6 and customized_id = %s ", [assembleddocnumber, timeentryid]) # 6 means this field in Redmine in custom_fields table

        # update redmine table with docdetailsid end

    return render(request, 'quotation/quotationissuetrackingsystemredirecturl.html', {'pk': quotationdocid})
@group_required("manager")
@login_required
def quotationissuetrackingsystempostitems(request):

#    creatorid = request.user.id
#    BASE_DIR = settings.BASE_DIR


#    quotationdocid = request.POST['quotationdocid']
    subprocess.call('curl -v -H "Content-Type: application/json" -H "X-Redmine-API-Key: 6a722899382b3495828b3f2d6c41f93d19adb5f6" -X POST -d \'{"time_entry": {"project_id": "4", "activity_id": "8", "hours": "11"}}\' http://13.58.18.245:3000//time_entries.json', shell=True)
    results23 = 1
    json_data = json.dumps(results23)

    return HttpResponse(json_data, content_type="application/json")

@group_required("manager")
@login_required
def quotationissuetrackingsystemsearchcontent(request):
    creatorid = request.user.id
    BASE_DIR = settings.BASE_DIR
    #import pdb;
    #pdb.set_trace()

    filteritemlistraw = request.POST['filteritemlist']
    filteritemlist = json.loads(filteritemlistraw)

    filteritemname = ''
    filteritemoperator = ''
    filteritemfirstinput = ''
    filteritemsecondinput = ''

    projectstatusphrase = ""
    quoteddocdetailsidphrase = ""
    quoteddocnumberphrase = ""
    datespentonphrase = ""
    timeentryidphrase = ""
    projectnamephrase = ""

    for x in range(0,len(filteritemlist),4):

        filteritemname = filteritemlist[(x+0)]
        filteritemoperator = filteritemlist[x+1]
        filteritemfirstinput = filteritemlist[x+2]
        filteritemsecondinput = filteritemlist[x+3]

        if filteritemname == 'projectstatus':
            if filteritemoperator == 'open':
                projectstatusphrase = "and projects.status = 1  "
            if filteritemoperator == 'closed':
                projectstatusphrase = "and projects.status = 5  "

        if filteritemname == 'quoteddocdetailsid':
            if filteritemoperator == 'hasnotvalue':
                quoteddocdetailsidphrase = "and quoteddocdetailsidtable.value is null or quoteddocdetailsidtable.value = '' "
            if filteritemoperator == 'hasvalue':
                quoteddocdetailsidphrase = "and quoteddocdetailsidtable.value is not null "

        if filteritemname == 'quoteddocnumber':
            if filteritemoperator == 'is':
                quoteddocnumberphrase = "and quoteddocnumbertable.value = '" + filteritemfirstinput + "' "

        if filteritemname == 'datespenton':
            if filteritemoperator == 'between':
                datespentonphrase = "and T.spent_on BETWEEN '" + filteritemfirstinput + "' AND '" + filteritemsecondinput + "' "

        if filteritemname == 'timeentryid':
            if filteritemoperator == 'is':
                timeentryidphrase = "and T.id = '" + filteritemfirstinput + "' "

        if filteritemname == 'projectid':
            if filteritemoperator == 'is':
                projectnamephrase = "and projects.id = '" + filteritemfirstinput + "' "

        if filteritemname == 'userid':
            if filteritemoperator == 'is':
                projectnamephrase = "and T.user_id = '" + filteritemfirstinput + "' "


    searchphraseformainresults = (projectstatusphrase + quoteddocdetailsidphrase + quoteddocnumberphrase + #(unquotedcheckboxphrase + onlyforopenprojectsphrase + timeentryidformainresults + projectnameformainresults +
                                  datespentonphrase + timeentryidphrase + projectnamephrase)
                                  #datephraseformainresults + companyformainresults + usernameformainresults +
                                  #activitynameformainresults + quoteddocnumberformainresults + " ")
    searchphraseforrowsources = ""# (unquotedcheckboxforrowsources + onlyforopenprojectsforrowsources + timeentryidforrowsource +
#                                 projectnameforrowsources + usernameforrowsources + activitynameforrowsources +
#                                 quoteddocnumberforrowsource + " ")
    #import pdb;
    #pdb.set_trace()

    cursor2 = connection.cursor()
    cursor21 = connections['redmine'].cursor()
    cursor21.execute("SELECT "
                     "T.id, "
                     "T.id, "
                     "projects.name, "
                     "T.issue_id, "
                     "CONCAT(users.firstname, ' ', users.lastname) AS username, "
                     "enumerations.name as activityname, " #5
                     "T.hours, "
                     "T.comments, "
                     "T.spent_on, "
                     "T.project_id, "
                     "T.user_id, " #10
                     "T.activity_id, "
                     "projects.status, "
                     "quoteddocdetailsidtable.value, "
                     "quoteddocnumbertable.value, "
                     "T.created_on, "   #15
                     "T.updated_on, "
                     "issues.subject "

                     "FROM time_entries as T "

                     "LEFT JOIN custom_values as quoteddocdetailsidtable "
                     "ON T.id = quoteddocdetailsidtable.customized_id and quoteddocdetailsidtable.custom_field_id = 4 "

                     "LEFT JOIN custom_values as quoteddocnumbertable "
                     "ON T.id = quoteddocnumbertable.customized_id and quoteddocnumbertable.custom_field_id = 6 "

                     "JOIN projects "
                     "ON T.project_id = projects.id "

                     "JOIN enumerations "
                     "ON T.activity_id = enumerations.id "

                     "JOIN users "
                     "ON T.user_id = users.id "

                     "JOIN issues "
                     "ON T.issue_id = issues.id "

                     "WHERE T.id is not null " + searchphraseformainresults + "")

    docs = cursor21.fetchall()

    #import pdb;
    #pdb.set_trace()

    issuetrackingsystemnumberofitems = len(docs)

    cursor23 = connections['redmine'].cursor()
    cursor23.execute("SELECT "
                     "projects.name "

                     "FROM time_entries as T "

                     "LEFT JOIN custom_values as quoteddocdetailsidtable "
                     "ON T.id = quoteddocdetailsidtable.customized_id and quoteddocdetailsidtable.custom_field_id = 4 "

                     "LEFT JOIN custom_values as quoteddocnumbertable "
                     "ON T.id = quoteddocnumbertable.customized_id and quoteddocnumbertable.custom_field_id = 6 "

                     "JOIN projects "
                     "ON T.project_id = projects.id "

                     "JOIN enumerations "
                     "ON T.activity_id = enumerations.id "

                     "JOIN users "
                     "ON T.user_id = users.id "

                     "WHERE T.id is not null " + searchphraseforrowsources + " "
                                                                             
                     "GROUP BY projects.name ")
    projectnamerowsources = cursor23.fetchall()

    cursor24 = connections['redmine'].cursor()
    cursor24.execute("SELECT "
                     "CONCAT(users.firstname, ' ', users.lastname) AS username, "
                     "T.user_id "

                     "FROM time_entries as T "

                     "LEFT JOIN custom_values as quoteddocdetailsidtable "
                     "ON T.id = quoteddocdetailsidtable.customized_id and quoteddocdetailsidtable.custom_field_id = 4 "

                     "LEFT JOIN custom_values as quoteddocnumbertable "
                     "ON T.id = quoteddocnumbertable.customized_id and quoteddocnumbertable.custom_field_id = 6 "

                     "JOIN projects "
                     "ON T.project_id = projects.id "

                     "JOIN enumerations "
                     "ON T.activity_id = enumerations.id "

                     "JOIN users "
                     "ON T.user_id = users.id "

                     "WHERE T.id is not null " + searchphraseforrowsources + " "
                                                                             
                     "GROUP BY username, T.user_id ")
    usernamerowsources = cursor24.fetchall()

    cursor25 = connections['redmine'].cursor()
    cursor25.execute("SELECT "
                     "enumerations.name as activityname, "
                     "T.activity_id "

                     "FROM time_entries as T "

                     "LEFT JOIN custom_values as quoteddocdetailsidtable "
                     "ON T.id = quoteddocdetailsidtable.customized_id and quoteddocdetailsidtable.custom_field_id = 4 "

                     "LEFT JOIN custom_values as quoteddocnumbertable "
                     "ON T.id = quoteddocnumbertable.customized_id and quoteddocnumbertable.custom_field_id = 6 "

                     "JOIN projects "
                     "ON T.project_id = projects.id "

                     "JOIN enumerations "
                     "ON T.activity_id = enumerations.id "

                     "JOIN users "
                     "ON T.user_id = users.id "

                     "WHERE T.id is not null " + searchphraseforrowsources + " "
                                                                             
                     "GROUP BY activityname, T.activity_id ")
    activitynamerowsources = cursor25.fetchall()
    #import pdb;
    #pdb.set_trace()

    return render(request, 'quotation/quotationtimeentriescontent.html', {'docs': docs,
                                                               'issuetrackingsystemnumberofitems': issuetrackingsystemnumberofitems,
                                                               'projectnamerowsources': projectnamerowsources,
                                                               'searchphraseformainresults': searchphraseformainresults,
                                                               'usernamerowsources': usernamerowsources,
                                                               'activitynamerowsources': activitynamerowsources})
@group_required("manager")
@login_required
def quotationerasequoteddocdatainits(request):

    creatorid = request.user.id
    BASE_DIR = settings.BASE_DIR

    quotationdocid = request.POST['quotationdocid']
    quotationdocnumber = request.POST['quotationdocnumber']
    issuetrackingsystemnumberofitems = request.POST['issuetrackingsystemnumberofitems']
    itemdatalistraw = request.POST['itemdatalist']
    itemdatalist = json.loads(itemdatalistraw)

    for x in range(int(issuetrackingsystemnumberofitems)):

        timeentryid = itemdatalist[(8*x+0)]
        timeentryandissueid = itemdatalist[(8*x+1)]
        projectname = itemdatalist[8*x+2]
        username = itemdatalist[8*x+3]
        activityname = itemdatalist[8*x+4]
        hours = itemdatalist[8*x+5]
        comments = itemdatalist[8*x+6]
        spenton = itemdatalist[8*x+7]

        # update redmine  table begin

        cursor21 = connections['redmine'].cursor()
        cursor21.execute("UPDATE custom_values SET "
                        "value = %s "
                        "WHERE custom_field_id = 4 and customized_id = %s ", [None, timeentryid]) # 4 means this  field in Redmine in custom_fields table

        cursor21 = connections['redmine'].cursor()
        cursor21.execute("UPDATE custom_values SET "
                        "value = %s "
                        "WHERE custom_field_id = 6 and customized_id = %s ", [None, timeentryid]) # 6 means this field in Redmine in custom_fields table

        # update redmine table end

    return render(request, 'quotation/quotationissuetrackingsystemredirecturl.html', {'pk': quotationdocid})
