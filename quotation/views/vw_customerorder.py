from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required, user_passes_test
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
def customerorderform(request, pk):
    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        docid = request.POST['docid']
        fieldname = request.POST['fieldname']
        tbl = request.POST['tbl']
        if tbl == "tblDoc_details":
            cursor22 = connection.cursor()
            cursor22.callproc("spcustomerordertbldocdetailsfieldsupdate", [fieldname, fieldvalue, rowid])
            results23 = cursor22.fetchall()
            print(results23)

            json_data = json.dumps(results23)

            return HttpResponse(json_data, content_type="application/json")

        elif tbl == "tblDoc":
            cursor22 = connection.cursor()
            cursor22.callproc("spcustomerordertbldocfieldsupdate", [fieldname, fieldvalue, docid])
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
                    "deferredpaymentdaysincustomerorder_tbldoc "

                    "FROM quotation_tbldoc as D "

                    "JOIN quotation_tbldoc_kind as DK "
                    "ON D.Doc_kindid_tblDoc_id = DK.Doc_kindid_tblDoc_kind "

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
                    "DD.purchase_price_tblproduct_ctblDoc_details, " # 10
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
                    "DD.supplierdescription_tblProduct_ctblDoc_details " # 25

                    
                    

                    "FROM quotation_tbldoc_details as DD "
                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x ON DD.Productid_tblDoc_details_id = x.Productid_tblProduct "
                    "JOIN quotation_tblcompanies as C "
                    "ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "
               
                
                    "WHERE DD.docid_tbldoc_details_id=%s "
                    "order by DD.firstnum_tblDoc_details,DD.secondnum_tblDoc_details,DD.thirdnum_tblDoc_details,DD.fourthnum_tblDoc_details",
                    [pk])
    docdetails = cursor3.fetchall()

    cursor14 = connection.cursor()
    cursor14.execute("SELECT DD.Doc_detailsid_tblDoc_details, "
                    "DD2.podocdetails, "
                    "DD2.podocdetailsqty, "
                    "DD2.podocnumber, "
                    "DD2.popretag, "
                    "DD2.podocid, " #5
                    "DD3.sumpodocdetailsqty "
                     
                    "FROM quotation_tbldoc_details as DD "

                   "LEFT JOIN    (SELECT (Doc_detailsid_tblDoc_details) as podocdetails, "
                    "               podetailslink_tbldocdetails, "
                    "               (Qty_tblDoc_details) as podocdetailsqty, "
                    "               (docnumber_tbldoc) as podocnumber, "
                    "               (pretag_tbldockind) as popretag, "
                    "               (docid) as podocid "
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
                    "ON DD.Doc_detailsid_tblDoc_details=DD2.podetailslink_tbldocdetails "

                   "LEFT JOIN    (SELECT podetailslink_tbldocdetails, sum(Qty_tblDoc_details) as sumpodocdetailsqty "
                    "               FROM quotation_tbldoc_details as DDxx "

                    "               JOIN quotation_tbldoc as Dxx "
                    "               ON Dxx.Docid_tblDoc=DDxx.Docid_tblDoc_details_id "
                    "               WHERE obsolete_tbldoc=0 "
                    "               GROUP BY podetailslink_tbldocdetails) as DD3 "
                    "ON DD.Doc_detailsid_tblDoc_details=DD3.podetailslink_tbldocdetails "

                     "WHERE DD.docid_tbldoc_details_id=%s",[pk])
    polinks = cursor14.fetchall()

    cursor15 = connection.cursor()
    cursor15.execute("SELECT "
                     "Companyid_tblCompanies, "
                     "companyname_tblcompanies "

                     "FROM quotation_tblcompanies "


                     "WHERE stockflag_tblcompanies=1 ")
    stockradiobuttonrows = cursor15.fetchall()

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

    return render(request, 'quotation/customerorder.html',
                  {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums': nextchapternums,
                   'creatordata': creatordata,
                   'polinks': polinks,
                   'stockradiobuttonrows': stockradiobuttonrows,
                   'currencycodes': currencycodes})
@group_required("manager")
@login_required
def customerordernewrow(request, pkdocid, pkproductid, pkdocdetailsid, nextfirstnumonhtml, nextsecondnumonhtml,
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

    return redirect('customerorderform', pk=pkdocid)

@group_required("manager")
@login_required
def customerordernewrowadd(request):
    if request.method == "POST":
        docdetailsid = request.POST['docdetailsid']
        customerorderid = request.POST['customerorderid']
        nextfirstnumonhtml = request.POST['nextfirstnumonhtml']
        nextsecondnumonhtml = request.POST['nextsecondnumonhtml']
        nextthirdnumonhtml = request.POST['nextthirdnumonhtml']
        nextfourthnumonhtml = request.POST['nextfourthnumonhtml']

        nextchapternumset = array('i', [int(nextfirstnumonhtml), int(nextsecondnumonhtml), int(nextthirdnumonhtml),
                                        int(nextfourthnumonhtml)])

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
    # return redirect('quotationform', pk=1)

    return render(request, 'quotation/customerordernewrowadd.html',
                  {'products': products, 'docid': customerorderid, 'nextchapternumset': nextchapternumset,
                   'docdetailsid': docdetailsid})

@group_required("manager")
@login_required
def customerorderrowremove(request, pk):
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

    return redirect('customerorderform', pk=na)

@group_required("manager")
@login_required
def searchcustomerordercontacts(request):
    customerorderbackpage

    if request.method == 'POST':
        search_text = request.POST['search_text']
        docidincustomerorderjs = request.POST['docidincustomerorderjs']
    else:
        search_text = ""
    search_textmodified = "%" + search_text + "%"
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

    rownmbs = len(results)

    return render(request, 'quotation/ajax_search_customerorder_contacts.html',
                  {'results': results, 'rownmbs': rownmbs, 'docidincustomerorderjs': docidincustomerorderjs})

@group_required("manager")
@login_required
def customerorderupdatecontact(request, pkdocid, pkcontactid):
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
                                                pkdocid, ])

    return redirect('customerorderform', pk=pkdocid)

@group_required("manager")
@login_required
def customerorderprint(request, docid):
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Docid_tblDoc, "
                    "Contactid_tblDoc_id, "
                    "Doc_kindid_tblDoc_id, "
                    "companyname_tblcompanies_ctbldoc, "
                    "firstname_tblcontacts_ctbldoc, "
                    "lastname_tblcontacts_ctbldoc, "
                    "prefacetextforcustomerorder_tblprefaceforcustomerorder_ctbldoc, "
                    "backpagetextforcustomerorder_tblbackpageforcustomerorder_ctbldoc, "
                    "prefacespecforcustomerorder_tbldoc, "
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
                    "paymenttextforcustomerorder_tblpayment_ctbldoc, "
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

    return render(request, 'quotation/customerorderprint.html', {'doc': doc, 'docdetails': docdetails,
                                                             'docdetailscount': docdetailscount,
                                                             'creatordata': creatordata})

@group_required("manager")
@login_required
def customerorderuniversalselections(request):
    fieldvalue = request.POST['fieldvalue']
    customerorderdocid = request.POST['customerorderdocid']
    fieldname = request.POST['fieldname']

    cursor2 = connection.cursor()

    cursor2.execute("UPDATE quotation_tbldoc SET "
                    "" + fieldname + "= %s "
                                     "WHERE Docid_tblDoc =%s ", [fieldvalue, customerorderdocid])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT " + fieldname + " "
                                "FROM quotation_tbldoc "
                                "WHERE Docid_tblDoc =%s ", [customerorderdocid])
    results = cursor3.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")

@group_required("manager")
@login_required
def customerorderbackpage(request):
    if request.method == 'POST':
        customerorderid = request.POST['customerorderid']
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT "
        "Docid_tblDoc, "
        "backpagetextforcustomerorder_tblbackpageforcustomerorder_ctbldoc, "
        "docnumber_tbldoc, "
        "creatorid_tbldoc, "
        "deliverydays_tbldoc "
        "FROM quotation_tbldoc "
        "WHERE docid_tbldoc=%s ",
        [customerorderid])

    doc = cursor0.fetchall()
    json_data = json.dumps(doc)

    return HttpResponse(json_data, content_type="application/json")
