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
from django.core.mail import EmailMessage


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
def acustomerorderform(request, pk):
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
                    "deferredpaymentdaysincustomerorder_tbladoc "

                    "FROM aid_tbladoc as D "

                    "JOIN aid_tbladoc_kind as DK "
                    "ON D.Doc_kindid_tblaDoc_id = DK.Doc_kindid_tblaDoc_kind "

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
    # if there is not such product already not show goto

    cursor3.execute("SELECT  DD.Doc_detailsid_tblaDoc_details, "
                    "DD.Qty_tblaDoc_details, "
                    "DD.Docid_tblaDoc_details_id, "
                    "DD.customerdescription_tblProduct_ctblaDoc_details, "
                    "DD.firstnum_tblaDoc_details, "
                    "DD.fourthnum_tblaDoc_details, "
                    "DD.secondnum_tblaDoc_details, "
                    "DD.thirdnum_tblaDoc_details, "
                    "DD.Note_tblaDoc_details, "
                    "DD.creationtime_tblaDoc_details, "
                    "DD.purchase_price_tblproduct_ctblaDoc_details, " # 10
                    "DD.listprice_tblaDoc_details, "
                    "DD.currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details, "
                    "DD.Productid_tblaDoc_details_id, "
                    "DD.Doc_detailsid_tblaDoc_details, "
                    "COALESCE(Productid_tblaProduct, 0), "
                    "DD.currencyrate_tblcurrency_ctblaDoc_details, "
                    "round((((DD.listprice_tblaDoc_details-DD.purchase_price_tblproduct_ctblaDoc_details)/(DD.listprice_tblaDoc_details))*100),1) as listpricemargin, "
                    "DD.unitsalespriceACU_tblaDoc_details, "
                    "round((DD.purchase_price_tblproduct_ctblaDoc_details * DD.currencyrate_tblcurrency_ctblaDoc_details),2) as purchasepriceACU, "
                    "round((((DD.unitsalespriceACU_tblaDoc_details-(DD.purchase_price_tblproduct_ctblaDoc_details * DD.currencyrate_tblcurrency_ctblaDoc_details))/(DD.unitsalespriceACU_tblaDoc_details))*100),1) as unitsalespricemargin, "
                    "round((DD.listprice_tblaDoc_details * DD.currencyrate_tblcurrency_ctblaDoc_details),2) as listpriceACU, "
                    "(100-round(((DD.unitsalespriceACU_tblaDoc_details/(DD.listprice_tblaDoc_details * DD.currencyrate_tblcurrency_ctblaDoc_details))*100),1)) as discount, "
                    "DD.unit_tbladocdetails, "
                    "companyname_tblacompanies, "
                    "DD.supplierdescription_tblProduct_ctblaDoc_details " # 25

                    "FROM aid_tbladoc_details as DD "

                    "LEFT JOIN (SELECT Productid_tblaProduct FROM aid_tblaproduct WHERE obsolete_tblaproduct = 0) as x "
                    "ON DD.Productid_tblaDoc_details_id = x.Productid_tblaProduct "

                    "LEFT JOIN aid_tblacompanies as C "
                    "ON DD.suppliercompanyid_tbladocdetails = C.companyid_tblacompanies "
                
                    "WHERE DD.docid_tbladoc_details_id=%s "
                    "order by DD.firstnum_tblaDoc_details,DD.secondnum_tblaDoc_details,DD.thirdnum_tblaDoc_details,DD.fourthnum_tblaDoc_details",
                    [pk])
    docdetails = cursor3.fetchall()
    #import pdb;
    #pdb.set_trace()

    cursor14 = connection.cursor()
    cursor14.execute("SELECT DD.Doc_detailsid_tblaDoc_details, "
                    "DD2.podocdetails, "
                    "DD2.podocdetailsqty, "
                    "DD2.podocnumber, "
                    "DD2.popretag, "
                    "DD2.podocid, " #5
                    "DD3.sumpodocdetailsqty "
                     
                    "FROM aid_tbladoc_details as DD "

                   "LEFT JOIN    (SELECT (Doc_detailsid_tblaDoc_details) as podocdetails, "
                    "               podetailslink_tbladocdetails, "
                    "               (Qty_tblaDoc_details) as podocdetailsqty, "
                    "               (docnumber_tbladoc) as podocnumber, "
                    "               (pretag_tbladockind) as popretag, "
                    "               (docid) as podocid "
                    "               FROM aid_tbladoc_details as DDx "

                    "               JOIN (SELECT docnumber_tbladoc, "
                    "                            (COALESCE(Docid_tblaDoc, 0)) as docid, "
                    "                             pretag_tbladockind "
                    "                       FROM aid_tbladoc"
                    "                       JOIN aid_tbladoc_kind "
                    "                       ON aid_tbladoc.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "

                    "                       WHERE obsolete_tbladoc = 0"
                    "                    ) as D"
                    "               ON D.docid=DDx.Docid_tblaDoc_details_id "
                    "            ) as DD2 "
                    "ON DD.Doc_detailsid_tblaDoc_details=DD2.podetailslink_tbladocdetails "

                   "LEFT JOIN    (SELECT podetailslink_tbladocdetails, sum(Qty_tblaDoc_details) as sumpodocdetailsqty "
                    "               FROM aid_tbladoc_details as DDxx "

                    "               JOIN aid_tbladoc as Dxx "
                    "               ON Dxx.Docid_tblaDoc=DDxx.Docid_tblaDoc_details_id "
                    "               WHERE obsolete_tbladoc=0 "
                    "               GROUP BY podetailslink_tbladocdetails) as DD3 "
                    "ON DD.Doc_detailsid_tblaDoc_details=DD3.podetailslink_tbladocdetails "

                     "WHERE DD.docid_tbladoc_details_id=%s",[pk])
    polinks = cursor14.fetchall()

    cursor15 = connection.cursor()
    cursor15.execute("SELECT "
                     "Companyid_tblaCompanies, "
                     "companyname_tblacompanies "

                     "FROM aid_tblacompanies "

                     "WHERE stockflag_tblacompanies=1 ")
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

    return render(request, 'aid/acustomerorder.html',
                  {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums': nextchapternums,
                   'creatordata': creatordata,
                   'polinks': polinks,
                   'stockradiobuttonrows': stockradiobuttonrows,
                   'currencycodes': currencycodes})
@group_required("manager")
@login_required
def acustomerordernewrow(request, pkdocid, pkproductid, pkdocdetailsid, nextfirstnumonhtml, nextsecondnumonhtml,
                    nextthirdnumonhtml, nextfourthnumonhtml):
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT `Productid_tblaProduct`, "
        "`purchase_price_tblaproduct`, `"
        "customerdescription_tblaProduct`, "
        "`margin_tblaproduct`, "
        "`currencyisocode_tblcurrency_ctblaproduct`, "
        "currencyrate_tblacurrency, "
        "unit_tblaproduct, "
        "supplierdescription_tblaProduct, "
        "suppliercompanyid_tblaProduct "
        "FROM `aid_tblaproduct` "
        "LEFT JOIN aid_tblacurrency "
        "ON aid_tblaproduct.currencyisocode_tblcurrency_ctblaproduct=aid_tblacurrency.currencyisocode_tblacurrency "
        "WHERE Productid_tblaProduct= %s", [pkproductid])
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
            "UPDATE aid_tbladoc_details SET "
            "Productid_tblaDoc_details_id= %s, "
            "firstnum_tblaDoc_details=%s, "
            "secondnum_tblaDoc_details=%s, "
            "thirdnum_tblaDoc_details=%s, "
            "fourthnum_tblaDoc_details=%s, "
            "purchase_price_tblproduct_ctblaDoc_details=%s, "
            "customerdescription_tblProduct_ctblaDoc_details=%s, "
            "currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details=%s, "
            "listprice_tblaDoc_details=%s, "
            "currencyrate_tblcurrency_ctblaDoc_details=%s, "
            "unitsalespriceACU_tblaDoc_details=%s, "
            "unit_tbladocdetails=%s, "
            "supplierdescription_tblProduct_ctblaDoc_details=%s, "
            "suppliercompanyid_tblaDocdetails=%s "
            "WHERE doc_detailsid_tbladoc_details =%s ",
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
            "INSERT INTO aid_tbladoc_details "
            "(`Qty_tblaDoc_details`, "
            "`Docid_tblaDoc_details_id`, "
            "`Productid_tblaDoc_details_id`, "
            "`firstnum_tblaDoc_details`, "
            "`fourthnum_tblaDoc_details`, " #5
            "`secondnum_tblaDoc_details`, "
            "`thirdnum_tblaDoc_details`, "
            "`Note_tblaDoc_details`, "
            "`purchase_price_tblproduct_ctblaDoc_details`, "
            "`customerdescription_tblProduct_ctblaDoc_details`, " #10
            "`currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details`, "
            "listprice_tblaDoc_details, "
            "currencyrate_tblcurrency_ctblaDoc_details, "
            "unitsalespriceACU_tblaDoc_details, "
            "unit_tbladocdetails, " #15
            "`supplierdescription_tblProduct_ctblaDoc_details`, "
            "suppliercompanyid_tblaDocdetails) "

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

    return redirect('acustomerorderform', pk=pkdocid)

@group_required("manager")
@login_required
def acustomerordernewrowadd(request):
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
        "SELECT Productid_tblaProduct, "
        "purchase_price_tblaproduct, "
        "margin_tblaproduct, "
        "round((100*purchase_price_tblaproduct)/(100-margin_tblaproduct),2) as listprice, "
        "customerdescription_tblaProduct, "
        "currencyisocode_tblcurrency_ctblaproduct, "
        "supplierdescription_tblaProduct "
        "FROM aid_tblaproduct "
        "WHERE obsolete_tblaproduct=0 ")
    products = cursor1.fetchall()
    transaction.commit()
    # return redirect('quotationform', pk=1)

    return render(request, 'aid/acustomerordernewrowadd.html',
                  {'products': products, 'docid': customerorderid, 'nextchapternumset': nextchapternumset,
                   'docdetailsid': docdetailsid})

@group_required("manager")
@login_required
def acustomerorderrowremove(request, pk):
    cursor2 = connection.cursor()
    cursor2.execute(
        "SELECT Docid_tblaDoc_details_id FROM aid_tbladoc_details WHERE Doc_detailsid_tblaDoc_details=%s ", [pk])
    results = cursor2.fetchall()
    for x in results:
        na = x[0]
    transaction.commit()

    cursor1 = connection.cursor()
    cursor1.execute(
        "DELETE FROM aid_tbladoc_details WHERE Doc_detailsid_tblaDoc_details=%s ", [pk])
    transaction.commit()

    return redirect('acustomerorderform', pk=na)

@group_required("manager")
@login_required
def acustomerordersaveasacknowledgement(request, pk):
    creatorid = request.user.id

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Docid_tblaDoc, "
                    "Contactid_tblaDoc_id, "
                    "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                    "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                    "prefacespecforquotation_tbladoc, "
                    "subject_tbladoc, "
                    "docnumber_tbladoc, "
                    "total_tbladoc, "
                    "deliverydays_tbladoc, "
                    "paymenttextforquotation_tblpayment_ctbladoc, "
                    "currencycodeinreport_tbladoc, "
                    "currencyrateinreport_tbladoc, "
                    "accountcurrencycode_tbladoc, "
                    "companyname_tblcompanies_ctbladoc, "
                    "firstname_tblcontacts_ctbladoc, "
                    "lastname_tblcontacts_ctbladoc, "
                    "title_tblcontacts_ctbladoc, "
                    "mobile_tblcontacts_ctbladoc, "
                    "email_tblcontacts_ctbladoc, "
                    "pcd_tblcompanies_ctbladoc, "
                    "town_tblcompanies_ctbladoc, "
                    "address_tblcompanies_ctbladoc "

                    "FROM aid_tbladoc "

                    "WHERE docid_tbladoc=%s "
                    "order by docid_tbladoc desc",
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
        cursor8.execute("SELECT max(docnumber_tblaDoc) FROM aid_tbladoc "
                        "WHERE Doc_kindid_tblaDoc_id = 9")
        results = cursor8.fetchall()
        resultslen = len(results)
        for x in results:
            docnumber = x[0]
            docnumber += 1

        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO aid_tbladoc "
                        "( Doc_kindid_tblaDoc_id, "
                        "Contactid_tblaDoc_id, "
                        "companyname_tblcompanies_ctbladoc, "
                        "firstname_tblcontacts_ctbladoc, "
                        "lastname_tblcontacts_ctbladoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                        "prefacespecforquotation_tbladoc, "
                        "subject_tbladoc, "
                        "docnumber_tblaDoc, "
                        "total_tbladoc, "
                        "deliverydays_tbladoc, "
                        "creatorid_tbladoc, "
                        "title_tblcontacts_ctbladoc, "
                        "mobile_tblcontacts_ctbladoc, "
                        "email_tblcontacts_ctbladoc, "
                        "pcd_tblcompanies_ctbladoc, "
                        "town_tblcompanies_ctbladoc, "
                        "address_tblcompanies_ctbladoc, "
                        "paymenttextforquotation_tblpayment_ctbladoc, "
                        "currencycodeinreport_tbladoc, "
                        "currencyrateinreport_tbladoc, "
                        "doclinkparentid_tbladoc, "
                        "accountcurrencycode_tbladoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [9, contactid, companynameclone, firstnameclone, lastnameclone, prefacetext, backpagetext, prefacespectext,
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
        cursor3.execute("SELECT max(Docid_tblaDoc) FROM aid_tbladoc WHERE creatorid_tbladoc=%s", [creatorid])
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

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
                    "purchase_price_tblproduct_ctblaDoc_details, " #10
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
                    "suppliercompanyid_tbladocdetails, "
                    "supplierdescription_tblProduct_ctblaDoc_details " #25

                    "FROM aid_tbladoc_details "

                    "LEFT JOIN (SELECT Productid_tblaProduct FROM aid_tblaproduct WHERE obsolete_tblaproduct = 0) as x "
                    "ON "
                    "aid_tbladoc_details.Productid_tblaDoc_details_id = x.Productid_tblaProduct "

                    "WHERE docid_tbladoc_details_id=%s "
                    "order by firstnum_tblaDoc_details,secondnum_tblaDoc_details,thirdnum_tblaDoc_details,fourthnum_tblaDoc_details",
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
            "INSERT INTO aid_tbladoc_details "
            "( Docid_tblaDoc_details_id, "
            "`Qty_tblaDoc_details`, "
            "`customerdescription_tblProduct_ctblaDoc_details`, "
            "firstnum_tblaDoc_details, "
            "`fourthnum_tblaDoc_details`, "
            "`secondnum_tblaDoc_details`, "
            "`thirdnum_tblaDoc_details`, "
            "`Note_tblaDoc_details`, "
            "purchase_price_tblproduct_ctblaDoc_details, "
            "listprice_tblaDoc_details, "
            "currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details, "
            "Productid_tblaDoc_details_id, "
            "currencyrate_tblcurrency_ctblaDoc_details, "
            "unitsalespriceACU_tblaDoc_details, "
            "unit_tbladocdetails, "
            "suppliercompanyid_tbladocdetails, "
            "supplierdescription_tblProduct_ctblaDoc_details, "
            "creatorid_tbladocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

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


    return redirect('adocselector', pk=maxdocid)
@group_required("manager")
@login_required
def acustomerorderemailtry(request, docid):
    foo = 11
#    html_message = render_to_string('aid/mail_template.html', {'context': 'values', 'foo': foo})
    email = EmailMessage(
        'nax46', 'q', 'szluka.mate@gmail.com', ['szluka.matetest4@gmail.com'])#, cc=[cc])
#    email.content_subtype = "html"
    email.send()
    return redirect('adocselector', pk=docid)
