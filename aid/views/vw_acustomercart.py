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


#import pdb;
#pdb.set_trace()
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
@login_required
def acustomercartform(request, pk):
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
#    import pdb;
#    pdb.set_trace()

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
    if len(maxchapternums) == 0:
        maxfirstnum = 0
        maxsecondnum = 0
        maxthirdnum = 0
        maxfourthnum = 0
    else:
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

    return render(request, 'aid/acustomercart.html',
                  {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums': nextchapternums,
                   'creatordata': creatordata,
                   'polinks': polinks,
                   'stockradiobuttonrows': stockradiobuttonrows,
                   'currencycodes': currencycodes})
def acustomercartrefresh(request):
# determine latest available cart begin
    docdetails = None #if there is not item to show in cart (let has an init value)
    anonymoususerid = request.POST['anonymoususerid']
    anonymoususerid = int(anonymoususerid)
    useridnow = request.user.id
    if useridnow != None:
        userkind = 'realuser'
    else:
        userkind = 'anonymoususer'

    if userkind == 'realuser':
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tbladoc "
                        ""
                        "FROM aid_tbladoc "
                        ""
                        "WHERE obsolete_tbladoc=0 and creatorid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                        "order by docid_tbladoc desc",
                        [useridnow])
        results = cursor1.fetchall()
        if len(results) != 0:
            hascart = 'hascart'
            for x in results:
                latestunorderedcartdocid = x[0]
        else:
            hascart = 'hasnotcart'

    if userkind == 'anonymoususer':
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tbladoc "
                        ""
                        "FROM aid_tbladoc "
                        ""
                        "WHERE obsolete_tbladoc=0 and anonymoususerid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                        "order by docid_tbladoc desc",
                        [anonymoususerid])
        results = cursor1.fetchall()
        if len(results) != 0:
            hascart = 'hascart'
            for x in results:
                latestanonymousunorderedcartdocid = x[0]
        else:
            hascart = 'hasnotcart'
#determine latest available cart end

#save the anonymosuser's cart as realuser's cart begin
    if userkind == 'realuser' and hascart == 'hasnotcart': #the user became realuser from anonymoususer (the realuser inherited the anonymoususer's cart after login)
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tbladoc "
                        ""
                        "FROM aid_tbladoc "
                        ""
                        "WHERE obsolete_tbladoc=0 and anonymoususerid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                        "order by docid_tbladoc desc",
                        [anonymoususerid])
        results = cursor1.fetchall()
        if len(results) != 0:
            hascartasthisuserwhenheshewasanonymous = 'hascart'
            for x in results:
                latestanonymousunorderedcartdocid = x[0]
            cursor12 = connection.cursor()
            cursor12.execute(
                "UPDATE aid_tbladoc SET "
                "creatorid_tbladoc=%s "
                "WHERE Docid_tbladoc=%s ", [useridnow, latestanonymousunorderedcartdocid])
            hascart = hascartasthisuserwhenheshewasanonymous
            latestunorderedcartdocid = latestanonymousunorderedcartdocid
        else:
            hascartasthisuserwhenheshewasanonymous = 'hasnotcart'
#save the anonymosuser's cart as realuser's cart end

    if userkind == 'realuser' and hascart == 'hascart':
        cursor3 = connection.cursor()
        cursor3.execute("SELECT  "
                        "DD.Doc_detailsid_tblaDoc_details, "
                        "DD.Qty_tblaDoc_details, "
                        "DD.Docid_tblaDoc_details_id, "
                        "DD.customerdescription_tblProduct_ctblaDoc_details, "
                        "DD.firstnum_tblaDoc_details, "
                        "DD.fourthnum_tblaDoc_details, "
                        "DD.secondnum_tblaDoc_details, "
                        "DD.thirdnum_tblaDoc_details, "
                        "DD.Note_tblaDoc_details, "
                        "DD.creationtime_tblaDoc_details, "
                        "DD.purchase_price_tblproduct_ctblaDoc_details, "  # 10
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
                        "DD.supplierdescription_tblProduct_ctblaDoc_details, "  # 25
                        "round(DD.Qty_tblaDoc_details * CAST(unitsalespriceACU_tblaDoc_details AS DECIMAL(10,1)),1) as salesprice, "
                        "maxqtyincart_tblaproduct_ctblaDoc_details "
    
                        "FROM aid_tbladoc_details as DD "
    
                        "LEFT JOIN (SELECT Productid_tblaProduct FROM aid_tblaproduct WHERE obsolete_tblaproduct = 0) as x "
                        "ON DD.Productid_tblaDoc_details_id = x.Productid_tblaProduct "
    
                        "LEFT JOIN aid_tblacompanies as C "
                        "ON DD.suppliercompanyid_tbladocdetails = C.companyid_tblacompanies "
    
                        "WHERE DD.docid_tbladoc_details_id=%s "
                        "order by DD.firstnum_tblaDoc_details,DD.secondnum_tblaDoc_details,DD.thirdnum_tblaDoc_details,DD.fourthnum_tblaDoc_details",
                        [latestunorderedcartdocid])
        docdetails = cursor3.fetchall()
    if userkind == 'anonymoususer' and hascart == 'hascart':
        cursor3 = connection.cursor()
        cursor3.execute("SELECT  "
                        "DD.Doc_detailsid_tblaDoc_details, "
                        "DD.Qty_tblaDoc_details, "
                        "DD.Docid_tblaDoc_details_id, "
                        "DD.customerdescription_tblProduct_ctblaDoc_details, "
                        "DD.firstnum_tblaDoc_details, "
                        "DD.fourthnum_tblaDoc_details, "
                        "DD.secondnum_tblaDoc_details, "
                        "DD.thirdnum_tblaDoc_details, "
                        "DD.Note_tblaDoc_details, "
                        "DD.creationtime_tblaDoc_details, "
                        "DD.purchase_price_tblproduct_ctblaDoc_details, "  # 10
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
                        "DD.supplierdescription_tblProduct_ctblaDoc_details, "  # 25
                        "round(DD.Qty_tblaDoc_details * CAST(unitsalespriceACU_tblaDoc_details AS DECIMAL(10,1)),1) as salesprice, "
                        "maxqtyincart_tblaproduct_ctblaDoc_details "

                        "FROM aid_tbladoc_details as DD "

                        "LEFT JOIN (SELECT Productid_tblaProduct FROM aid_tblaproduct WHERE obsolete_tblaproduct = 0) as x "
                        "ON DD.Productid_tblaDoc_details_id = x.Productid_tblaProduct "

                        "LEFT JOIN aid_tblacompanies as C "
                        "ON DD.suppliercompanyid_tbladocdetails = C.companyid_tblacompanies "

                        "WHERE DD.docid_tbladoc_details_id=%s "
                        "order by DD.firstnum_tblaDoc_details,DD.secondnum_tblaDoc_details,DD.thirdnum_tblaDoc_details,DD.fourthnum_tblaDoc_details",
                        [latestanonymousunorderedcartdocid])
        docdetails = cursor3.fetchall()
    return render(request, 'aid/acustomercarttemplate.html', {'docdetails': docdetails})
def acustomercartadditemtocart(request):
# 1 real user has cart already
# 2 real user has not cart yet
# 3 anonymous user has cart already
# 4 anonymous user has not cart yet
    anonymoususerid = request.POST['anonymoususerid']
    anonymoususerid = int(anonymoususerid)
    useridnow = request.user.id
    if useridnow != None:
        userkind = 'realuser'
    else:
        userkind = 'anonymoususer'

    if userkind == 'realuser':
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tbladoc "
                        ""
                        "FROM aid_tbladoc "
                        ""
                        "WHERE obsolete_tbladoc=0 and creatorid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                        "order by docid_tbladoc desc",
                        [useridnow])
        results = cursor1.fetchall()
        if len(results) != 0:
            hascart = 'hascart'
        else:
            hascart = 'hasnotcart'

    if userkind == 'anonymoususer':
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tbladoc "
                        ""
                        "FROM aid_tbladoc "
                        ""
                        "WHERE obsolete_tbladoc=0 and anonymoususerid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                        "order by docid_tbladoc desc",
                        [anonymoususerid])
        results = cursor1.fetchall()
        if len(results) != 0:
            hascart = 'hascart'
        else:
            hascart = 'hasnotcart'


    def addingitemtocart(userkind,hascart):
        return True


# if no available cart creating a cart doc begin
    if hascart == 'hasnotcart':
        contactid = None
        prefacetext = ''
        backpagetext = ''
        prefacespectext = ''
        subject = 'x'
        total = 0
        deliverydays = 1
        paymenttext = ''
        currencycodeinreport = 'HUF'
        currencyrateinreport = 1
        accountcurrencycode = 'HUF'
        companynameclone = 'Aid Customer'
        firstnameclone = 'xfirstname'
        lastnameclone = 'xlastname'
        titleclone = 'Mr/Mrs'
        mobileclone = '11'
        emailclone = 'xemail'
        pcdclone = '1111'
        townclone = 'Szeged'
        addressclone = 'xx'

        cursor8 = connection.cursor()
        cursor8.execute("SELECT max(docnumber_tbladoc) FROM aid_tbladoc "
                        "WHERE Doc_kindid_tbladoc_id = 10")
        results = cursor8.fetchall()
        resultslen = len(results)
        for x in results:
            docnumber = x[0]
            docnumber += 1

        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO aid_tbladoc "
                        "( Doc_kindid_tbladoc_id, "
                        "Contactid_tbladoc_id, "
                        "companyname_tblcompanies_ctbladoc, "
                        "firstname_tblcontacts_ctbladoc, "
                        "lastname_tblcontacts_ctbladoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                        "prefacespecforquotation_tbladoc, "
                        "subject_tbladoc, "
                        "docnumber_tbladoc, "
                        "total_tbladoc, " #10
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
                        "accountcurrencycode_tbladoc, "
                        "anonymoususerid_tbladoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [10, contactid, companynameclone, firstnameclone, lastnameclone, prefacetext, backpagetext, prefacespectext,
                        subject,
                        docnumber,
                        total,
                        deliverydays,
                        useridnow,
                        titleclone,
                        mobileclone,
                        emailclone,
                        pcdclone,
                        townclone,
                        addressclone,
                        paymenttext,
                        currencycodeinreport,
                        currencyrateinreport,
                        '12',
                        accountcurrencycode,
                        anonymoususerid])

    if userkind == 'realuser':
        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tbladoc) FROM aid_tbladoc WHERE creatorid_tbladoc=%s", [useridnow])
        results = cursor3.fetchall()
        for x in results:
            latestunorderedcartdocid = x[0]

    if userkind == 'anonymoususer':
        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tbladoc) FROM aid_tbladoc WHERE anonymoususerid_tbladoc=%s", [anonymoususerid])
        results = cursor3.fetchall()
        for x in results:
            latestanonymousunorderedcartdocid = x[0]
# if no available cart creating a cart doc end

    productid = request.POST['productid']
    qty = request.POST['qty']

    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT `Productid_tblaProduct`, "
        "`purchase_price_tblaproduct`, `"
        "customerdescription_tblaProduct`, "
        "`margin_tblaproduct`, "
        "`currencyisocode_tblcurrency_ctblaproduct`, "
        "currencyrate_tblacurrency, " #5
        "unit_tblaproduct, "
        "supplierdescription_tblaProduct, "
        "suppliercompanyid_tblaProduct, "
        "maxqtyincart_tblaproduct "

        "FROM `aid_tblaproduct` "

        "LEFT JOIN aid_tblacurrency "
        "ON aid_tblaproduct.currencyisocode_tblcurrency_ctblaproduct=aid_tblacurrency.currencyisocode_tblacurrency "

        "WHERE Productid_tblaProduct= %s", [productid])
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
        maxqtyincartclone = instancesingle[9]
        unitsalespriceACU=listpricecomputed * currencyrateclone

        maxfirstnum = 0
        if hascart == 'hascart':
            if userkind == 'realuser':
                cursor5 = connection.cursor()
                cursor5.execute("SELECT `firstnum_tblaDoc_details` "
        
                                "FROM aid_tbladoc_details "
        
                                "WHERE docid_tbladoc_details_id=%s "
                                "order by firstnum_tblaDoc_details desc "
                                "LIMIT 1"
                                , [latestunorderedcartdocid])
                maxchapternums = cursor5.fetchall()
                for x in maxchapternums:
                    maxfirstnum = x[0]
            if userkind == 'anonymoususer':
                cursor5 = connection.cursor()
                cursor5.execute("SELECT `firstnum_tblaDoc_details` "
        
                                "FROM aid_tbladoc_details "
        
                                "WHERE docid_tbladoc_details_id=%s "
                                "order by firstnum_tblaDoc_details desc "
                                "LIMIT 1"
                                , [latestanonymousunorderedcartdocid])
                maxchapternums = cursor5.fetchall()
                for x in maxchapternums:
                    maxfirstnum = x[0]

        nextfirstnumonhtml = maxfirstnum + 1
        nextsecondnumonhtml =0
        nextthirdnumonhtml =0
        nextfourthnumonhtml =0

        if userkind == 'realuser':
            cursor1 = connection.cursor() # new row needed
            cursor1.execute(
                "INSERT INTO aid_tbladoc_details "
                "(`Qty_tblaDoc_details`, "
                "`Docid_tblaDoc_details_id`, "
                "`Productid_tblaDoc_details_id`, "
                "`firstnum_tblaDoc_details`, "
                "`fourthnum_tblaDoc_details`, "
                "`secondnum_tblaDoc_details`, "
                "`thirdnum_tblaDoc_details`, "
                "`Note_tblaDoc_details`, "
                "`purchase_price_tblproduct_ctblaDoc_details`, "
                "`customerdescription_tblProduct_ctblaDoc_details`, "
                "`currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details`, "
                "listprice_tblaDoc_details, "
                "currencyrate_tblcurrency_ctblaDoc_details, "
                "unitsalespriceACU_tblaDoc_details, "
                "unit_tbladocdetails, "
                "`supplierdescription_tblProduct_ctblaDoc_details`, "
                "suppliercompanyid_tblaDocdetails, "
                "maxqtyincart_tblaproduct_ctblaDoc_details ) " 
    
                "VALUES (%s, %s, %s, %s,%s,%s,%s,'Defaultnote', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                [qty,
                 latestunorderedcartdocid,
                 productid,
                 nextfirstnumonhtml,
                 nextfourthnumonhtml,
                 nextsecondnumonhtml,
                 nextthirdnumonhtml,
                 purchase_priceclone,
                 customerdescriptionclone,
                 currencyisocodeclone,
                 listpricecomputed,
                 currencyrateclone,
                 unitsalespriceACU,
                 unitclone,
                 supplierdescriptionclone,
                 suppliercompanyidclone,
                 maxqtyincartclone])
            transaction.commit()
        if userkind == 'anonymoususer':
            cursor1 = connection.cursor()
            cursor1.execute(
                "INSERT INTO aid_tbladoc_details "
                "(`Qty_tblaDoc_details`, "
                "`Docid_tblaDoc_details_id`, "
                "`Productid_tblaDoc_details_id`, "
                "`firstnum_tblaDoc_details`, "
                "`fourthnum_tblaDoc_details`, "
                "`secondnum_tblaDoc_details`, "
                "`thirdnum_tblaDoc_details`, "
                "`Note_tblaDoc_details`, "
                "`purchase_price_tblproduct_ctblaDoc_details`, "
                "`customerdescription_tblProduct_ctblaDoc_details`, "
                "`currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details`, "
                "listprice_tblaDoc_details, "
                "currencyrate_tblcurrency_ctblaDoc_details, "
                "unitsalespriceACU_tblaDoc_details, "
                "unit_tbladocdetails, "
                "`supplierdescription_tblProduct_ctblaDoc_details`, "
                "suppliercompanyid_tblaDocdetails, "
                "maxqtyincart_tblaproduct_ctblaDoc_details ) " 
    
                "VALUES (%s, %s, %s, %s,%s,%s,%s,'Defaultnote', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                [qty,
                 latestanonymousunorderedcartdocid,
                 productid,
                 nextfirstnumonhtml,
                 nextfourthnumonhtml,
                 nextsecondnumonhtml,
                 nextthirdnumonhtml,
                 purchase_priceclone,
                 customerdescriptionclone,
                 currencyisocodeclone,
                 listpricecomputed,
                 currencyrateclone,
                 unitsalespriceACU,
                 unitclone,
                 supplierdescriptionclone,
                 suppliercompanyidclone,
                 maxqtyincartclone])
            transaction.commit()

    gg=1
    json_data = json.dumps(gg)

    return HttpResponse(json_data, content_type="application/json")
def acustomercartincreasingqty(request):
    docdetailsid = request.POST['docdetailsid']

    cursor2 = connection.cursor()
    cursor2.execute(
        "SELECT Qty_tblaDoc_details "

        "FROM aid_tbladoc_details "

        "WHERE Doc_detailsid_tblaDoc_details=%s ", [docdetailsid])
    results = cursor2.fetchall()
    for x in results:
        oldqty = x[0]
    newqty = oldqty + 1

    cursor1 = connection.cursor()
    cursor1.execute(
        "UPDATE aid_tbladoc_details SET "
        "Qty_tblaDoc_details=%s "
        "WHERE Doc_detailsid_tblaDoc_details =%s ", [newqty, docdetailsid])

    return render(request, 'quotation/customerinvoicexmlresponsepdfstackingredirecturl.html', {'pk': 1}) #same redirect when xmlresponse arrives therefore same redirecturl.html
def acustomercartdecreasingqty(request):
    docdetailsid = request.POST['docdetailsid']

    cursor2 = connection.cursor()
    cursor2.execute(
        "SELECT Qty_tblaDoc_details "

        "FROM aid_tbladoc_details "

        "WHERE Doc_detailsid_tblaDoc_details=%s ", [docdetailsid])
    results = cursor2.fetchall()
    for x in results:
        oldqty = x[0]
    newqty = oldqty - 1

    cursor1 = connection.cursor()
    cursor1.execute(

        "UPDATE aid_tbladoc_details SET "
        "Qty_tblaDoc_details=%s "
        "WHERE Doc_detailsid_tblaDoc_details =%s ", [newqty, docdetailsid])

    return render(request, 'quotation/customerinvoicexmlresponsepdfstackingredirecturl.html', {'pk': 1}) #same redirect when xmlresponse arrives therefore same redirecturl.html
def acustomercartproductremove(request): #item removal from cart with ajax
    docdetailsid = request.POST['docdetailsid']

    cursor1 = connection.cursor()
    cursor1.execute(
        "DELETE FROM aid_tbladoc_details "
        "WHERE Doc_detailsid_tblaDoc_details=%s ", [docdetailsid])


    return render(request, 'quotation/customerinvoicexmlresponsepdfstackingredirecturl.html', {'pk': 1}) #same redirect when xmlresponse arrives therefore same redirecturl.html
@login_required
def acustomercartrowremove(request, pk): #rowremove from customercart doc (from form)
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

    return redirect('acustomercartform', pk=na)
def acustomercartpricetagtocarttop(request):
    totalprice = 0 #default init
    anonymoususerid = request.POST['anonymoususerid']
    anonymoususerid = int(anonymoususerid)
    useridnow = request.user.id
    if useridnow != None:
        userkind = 'realuser'
    else:
        userkind = 'anonymoususer'

    if userkind == 'realuser':
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tbladoc "
                        ""
                        "FROM aid_tbladoc "
                        ""
                        "WHERE obsolete_tbladoc=0 and creatorid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                        "order by docid_tbladoc desc",
                        [useridnow])
        results = cursor1.fetchall()
        if len(results) != 0:
            hascart = 'hascart'
            for x in results:
                latestunorderedcartdocid = x[0]
        else:
            hascart = 'hasnotcart'

    if userkind == 'anonymoususer':
        cursor1 = connection.cursor()
        cursor1.execute("SELECT "
                        "Docid_tbladoc "
                        ""
                        "FROM aid_tbladoc "
                        ""
                        "WHERE obsolete_tbladoc=0 and anonymoususerid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                        "order by docid_tbladoc desc",
                        [anonymoususerid])
        results = cursor1.fetchall()
        if len(results) != 0:
            hascart = 'hascart'
            for x in results:
                latestanonymousunorderedcartdocid = x[0]
        else:
            hascart = 'hasnotcart'

    if userkind == 'realuser' and hascart == 'hascart':
        cursor2 = connection.cursor()
        cursor2.execute(
            "SELECT "
            "sum( Qty_tblaDoc_details * CAST(unitsalespriceACU_tblaDoc_details AS DECIMAL(10,1)) ) "
    
            "FROM aid_tbladoc_details "
    
            "WHERE Docid_tblaDoc_details_id=%s ", [latestunorderedcartdocid])
        results = cursor2.fetchall()
        for x in results:
            totalprice = x[0]
            if totalprice is None:
                totalprice = 0
    if userkind == 'anonymoususer' and hascart == 'hascart':
        cursor2 = connection.cursor()
        cursor2.execute(
            "SELECT "
            "sum( Qty_tblaDoc_details * CAST(unitsalespriceACU_tblaDoc_details AS DECIMAL(10,1)) ) "
    
            "FROM aid_tbladoc_details "
    
            "WHERE Docid_tblaDoc_details_id=%s ", [latestanonymousunorderedcartdocid])
        results = cursor2.fetchall()
        for x in results:
            totalprice = x[0]
            if totalprice is None:
                totalprice = 0

    json_data = json.dumps(totalprice)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def acustomercartsaveasorder(request):
# determine latest available cart begin
    useridnow = request.user.id
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Docid_tbladoc "
                    ""
                    "FROM aid_tbladoc "
                    ""
                    "WHERE obsolete_tbladoc=0 and creatorid_tbladoc=%s and thiscarthasthisorderdocid_tbladoc = 0 and Doc_kindid_tbladoc_id=10 "
                    "order by docid_tbladoc desc",
                    [useridnow])
    latestunorderedcartdocidtuple = cursor1.fetchall()
#    if len(latestunorderedcartdocidtuple) == 0: #not possible
#        latestunorderedcartdocid = -1
#    else:
    for x in latestunorderedcartdocidtuple:
            latestunorderedcartdocid = x[0]
# determine latest available cart end

    #import pdb;
    #pdb.set_trace()

    useridnow = request.user.id
    aidstartdate = request.POST['aidstartdate']
    aidstarttime = request.POST['aidstarttime']

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Docid_tbladoc, "
                    "Contactid_tbladoc_id, "
                    "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                    "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                    "prefacespecforquotation_tbladoc, "
                    "subject_tbladoc, "
                    "docnumber_tbladoc, "
                    "total_tbladoc, "
                    "deliverydays_tbladoc, "
                    "paymenttextforquotation_tblpayment_ctbladoc, "
                    "currencycodeinreport_tbladoc, " #10
                    "currencyrateinreport_tbladoc, " 
                    "accountcurrencycode_tbladoc, "
                    "companyname_tblcompanies_ctbladoc, "
                    "firstname_tblcontacts_ctbladoc, "
                    "lastname_tblcontacts_ctbladoc, "
                    "title_tblcontacts_ctbladoc, "
                    "mobile_tblcontacts_ctbladoc, "
                    "email_tblcontacts_ctbladoc, "
                    "pcd_tblcompanies_ctbladoc, "
                    "town_tblcompanies_ctbladoc, " #20
                    "address_tblcompanies_ctbladoc "
                    ""
                    "FROM aid_tbladoc "
                    ""
                    "WHERE docid_tbladoc=%s "
                    "order by docid_tbladoc desc",
                    [latestunorderedcartdocid])
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
    '''
    if len(doc) == 0:
        contactid = 1
        prefacetext = ''
        backpagetext = ''
        prefacespectext = ''
        subject = 'xx'
        total = 0
        deliverydays = 1
        paymenttext = ''
        currencycodeinreport = 'HUF'
        currencyrateinreport = 1
        accountcurrencycode = 'HUF'
        companynameclone = 'c'
        firstnameclone = 'q'
        lastnameclone = 'q'
        titleclone = 'Mr/Mrs'
        mobileclone = '11'
        emailclone = 'x@v.vf'
        pcdclone = '1111'
        townclone = 'Szeged'
        addressclone = 'w'
        djangouseridclone = 1
    '''
    cursor8 = connection.cursor()
    cursor8.execute("SELECT max(docnumber_tbladoc) FROM aid_tbladoc "
                    "WHERE Doc_kindid_tbladoc_id = 2")
    results = cursor8.fetchall()
    resultslen = len(results)
    for x in results:
        docnumber = x[0]
        docnumber += 1

    cursor2 = connection.cursor()
    cursor2.execute("INSERT INTO aid_tbladoc "
                    "( Doc_kindid_tbladoc_id, "
                    "Contactid_tbladoc_id, "
                    "companyname_tblcompanies_ctbladoc, "
                    "firstname_tblcontacts_ctbladoc, "
                    "lastname_tblcontacts_ctbladoc, "
                    "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                    "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                    "prefacespecforquotation_tbladoc, "
                    "subject_tbladoc, "
                    "docnumber_tbladoc, "
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
                    "accountcurrencycode_tbladoc, "
                    "aidstartdate_tbladoc, "
                    "aidstarttime_tbladoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [2, contactid, companynameclone, firstnameclone, lastnameclone, prefacetext, backpagetext, prefacespectext,
                    subject,
                    docnumber,
                    total,
                    deliverydays,
                    useridnow,
                    titleclone,
                    mobileclone,
                    emailclone,
                    pcdclone,
                    townclone,
                    addressclone,
                    paymenttext,
                    currencycodeinreport,
                    currencyrateinreport,
                    '113',
                    accountcurrencycode,
                    aidstartdate,
                    aidstarttime])

    cursor3 = connection.cursor()
    cursor3.execute("SELECT max(Docid_tbladoc) FROM aid_tbladoc WHERE creatorid_tbladoc=%s", [useridnow])
    results = cursor3.fetchall()
    for x in results:
        maxdocid = x[0]

    cursor3 = connection.cursor()
    cursor3.execute("UPDATE aid_tbladoc "
                    "SET thiscarthasthisorderdocid_tbladoc=%s "
                    "WHERE Docid_tbladoc=%s", [maxdocid, latestunorderedcartdocid])
    resultsx = cursor3.fetchall()

    cursor3.execute("SELECT `Doc_detailsid_tbladoc_details`, "
                    "`Qty_tbladoc_details`, "
                    "`Docid_tbladoc_details_id`, "
                    "`customerdescription_tblProduct_ctbladoc_details`, "
                    "`firstnum_tbladoc_details`, "
                    "`fourthnum_tbladoc_details`, "
                    "`secondnum_tbladoc_details`, "
                    "`thirdnum_tbladoc_details`, "
                    "`Note_tbladoc_details`, "
                    "`creationtime_tbladoc_details`, "
                    "purchase_price_tblproduct_ctbladoc_details, " #10
                    "listprice_tbladoc_details, "
                    "currencyisocode_tblcurrency_ctblproduct_ctbladoc_details, "
                    "Productid_tbladoc_details_id, "
                    "Doc_detailsid_tbladoc_details, "
                    "COALESCE(Productid_tblaproduct, 0), "
                    "currencyrate_tblcurrency_ctbladoc_details, "
                    "round((((listprice_tbladoc_details-purchase_price_tblproduct_ctbladoc_details)/(listprice_tbladoc_details))*100),1) as listpricemargin, "
                    "unitsalespriceACU_tbladoc_details, "
                    "round((purchase_price_tblproduct_ctbladoc_details * currencyrate_tblcurrency_ctbladoc_details),2) as purchasepriceACU, "
                    "round((((unitsalespriceACU_tbladoc_details-(purchase_price_tblproduct_ctbladoc_details * currencyrate_tblcurrency_ctbladoc_details))/(unitsalespriceACU_tbladoc_details))*100),1) as unitsalespricemargin, "
                    "round((listprice_tbladoc_details * currencyrate_tblcurrency_ctbladoc_details),2) as listpriceACU, "
                    "(100-round(((unitsalespriceACU_tbladoc_details/(listprice_tbladoc_details * currencyrate_tblcurrency_ctbladoc_details))*100),1)) as discount, "
                    "unit_tbladocdetails, "
                    "suppliercompanyid_tbladocdetails, "
                    "supplierdescription_tblProduct_ctbladoc_details " #25

                    "FROM aid_tbladoc_details "

                    "LEFT JOIN (SELECT Productid_tblaproduct FROM aid_tblaproduct WHERE obsolete_tblaproduct = 0) as x "
                    "ON "
                    "aid_tbladoc_details.Productid_tbladoc_details_id = x.Productid_tblaproduct "

                    "WHERE docid_tbladoc_details_id=%s "
                    "order by firstnum_tbladoc_details,secondnum_tbladoc_details,thirdnum_tbladoc_details,fourthnum_tbladoc_details",
                    [latestunorderedcartdocid])
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
            "( Docid_tbladoc_details_id, "
            "`Qty_tbladoc_details`, "
            "`customerdescription_tblProduct_ctbladoc_details`, "
            "firstnum_tbladoc_details, "
            "`fourthnum_tbladoc_details`, "
            "`secondnum_tbladoc_details`, "
            "`thirdnum_tbladoc_details`, "
            "`Note_tbladoc_details`, "
            "purchase_price_tblproduct_ctbladoc_details, "
            "listprice_tbladoc_details, "
            "currencyisocode_tblcurrency_ctblproduct_ctbladoc_details, "
            "Productid_tbladoc_details_id, "
            "currencyrate_tblcurrency_ctbladoc_details, "
            "unitsalespriceACU_tbladoc_details, "
            "unit_tbladocdetails, "
            "suppliercompanyid_tbladocdetails, "
            "supplierdescription_tblProduct_ctbladoc_details, "
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
             useridnow])

    cursor3 = connection.cursor()
    cursor3.execute("SELECT "
                    "Doc_kindid_tblaDoc_id, "
                    "docnumber_tblaDoc, "
                    "pretag_tbladockind "

                    "FROM aid_tbladoc "

                    "JOIN aid_tbladoc_kind as DK "
                    "ON Doc_kindid_tblaDoc_id = DK.Doc_kindid_tblaDoc_kind "

                    "WHERE docid_tbladoc=%s ", [maxdocid])
    customerordernumbers = cursor3.fetchall()
    for x in customerordernumbers:
        customerordernumberdocnumber = x[1]
        customerordernumberpretag = x[2]
    customerordernumber = str(customerordernumberpretag) + str(customerordernumberdocnumber)

    cursor2 = connection.cursor()
    cursor2.execute(
        "SELECT "
        "sum( CAST(Qty_tbladoc_details AS DECIMAL(10,0)) * CAST(unitsalespriceACU_tblaDoc_details AS DECIMAL(10,1)) ) "

        "FROM aid_tbladoc_details "

        "WHERE Docid_tblaDoc_details_id=%s ", [maxdocid])
    results = cursor2.fetchall()
    for x in results:
        totalprice = x[0]
    if totalprice is None:
        totalprice = 0

    cursor13 = connection.cursor()
    cursor13.execute("SELECT "
                    "`Doc_detailsid_tbladoc_details`, "
                    "CAST(Qty_tbladoc_details AS DECIMAL(10,0)), "
                    "`Docid_tbladoc_details_id`, "
                    "`customerdescription_tblProduct_ctbladoc_details`, "
                    "`firstnum_tbladoc_details`, "
                    "`fourthnum_tbladoc_details`, "
                    "`secondnum_tbladoc_details`, "
                    "`thirdnum_tbladoc_details`, "
                    "`Note_tbladoc_details`, "
                    "`creationtime_tbladoc_details`, "
                    "purchase_price_tblproduct_ctbladoc_details, " #10
                    "listprice_tbladoc_details, "
                    "currencyisocode_tblcurrency_ctblproduct_ctbladoc_details, "
                    "Productid_tbladoc_details_id, "
                    "Doc_detailsid_tbladoc_details, "
                    "currencyrate_tblcurrency_ctbladoc_details, " #15
                    "round((((listprice_tbladoc_details-purchase_price_tblproduct_ctbladoc_details)/(listprice_tbladoc_details))*100),1) as listpricemargin, "
                    "unitsalespriceACU_tbladoc_details, "
                    "round((purchase_price_tblproduct_ctbladoc_details * currencyrate_tblcurrency_ctbladoc_details),2) as purchasepriceACU, "
                    "round((((unitsalespriceACU_tbladoc_details-(purchase_price_tblproduct_ctbladoc_details * currencyrate_tblcurrency_ctbladoc_details))/(unitsalespriceACU_tbladoc_details))*100),1) as unitsalespricemargin, "
                    "round((listprice_tbladoc_details * currencyrate_tblcurrency_ctbladoc_details),2) as listpriceACU, "
                    "(100-round(((unitsalespriceACU_tbladoc_details/(listprice_tbladoc_details * currencyrate_tblcurrency_ctbladoc_details))*100),1)) as discount, "
                    "unit_tbladocdetails, "
                    "suppliercompanyid_tbladocdetails, "
                    "supplierdescription_tblProduct_ctbladoc_details, "
                    "CAST(Qty_tbladoc_details AS DECIMAL(10,0)) * CAST(unitsalespriceACU_tblaDoc_details AS DECIMAL(10,1)) as rowprice " #25

                    "FROM aid_tbladoc_details "

                    "WHERE docid_tbladoc_details_id=%s "
                    "order by firstnum_tbladoc_details,secondnum_tbladoc_details,thirdnum_tbladoc_details,fourthnum_tbladoc_details",
                    [maxdocid])
    cordocdetails = cursor13.fetchall()


    html_message = render_to_string('aid/acustomeracknowledgementemail.html', {'context': 'values',
                                                                               'customerordernumber': customerordernumber,
                                                                               'aidstartdate': aidstartdate,
                                                                               'aidstarttime': aidstarttime,
                                                                               'cordocdetails': cordocdetails,
                                                                               'totalprice': totalprice})

    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT "
        "id, "
        "username, "
        "email "

        "FROM auth_user "

        "WHERE id=%s ",
        [useridnow])
    usernowrowfromtable = cursor0.fetchall()
    # import pdb;
    # pdb.set_trace()

    for instancesingle in usernowrowfromtable:
        useremailnow = instancesingle[2]

    email = EmailMessage(
        'Aid Order Acknowledgement', html_message, 'szluka.mate@gmail.com', [useremailnow])  # , cc=[cc])
    email.content_subtype = "html"
    email.send()
    #import pdb;
    #pdb.set_trace()

    return render(request, 'aid/acustomerconfirmationredirecturl.html', {'docid': maxdocid})
def acustomercartaddinganonymoususerid(request):
    neededanewanonymoususeridflag = 0
    useridnow = request.user.id
    anonymoususerid = request.POST['anonymoususerid']
    if anonymoususerid == '':
        anonymoususerid = 0
    else:
        anonymoususerid = int(anonymoususerid)
    if anonymoususerid == 0 and useridnow == None:
        neededanewanonymoususeridflag = 1
    if neededanewanonymoususeridflag == 1:
        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO aid_tblaanonymoususers "
                        "(auxfieldforinsert_tblaanonymoususers) VALUES (%s)",
                        [1])
        cursor8 = connection.cursor()
        cursor8.execute("SELECT max(anonymoususerid_tblanonymoususers) FROM aid_tblaanonymoususers")
        results = cursor8.fetchall()
        for x in results:
            newanonymoususerid = x[0]
    if neededanewanonymoususeridflag == 0:
        newanonymoususerid = anonymoususerid
    json_data = json.dumps(newanonymoususerid)

    return HttpResponse(json_data, content_type="application/json")
