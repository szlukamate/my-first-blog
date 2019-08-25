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
@login_required
def customerinvoiceform(request, pk):
    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        docid = request.POST['docid']
        fieldname = request.POST['fieldname']
        tbl = request.POST['tbl']
        if tbl == "tblDoc_details":
            cursor22 = connection.cursor()
            cursor22.callproc("spcustomerinvoicedocdetailsfieldsupdate", [fieldname, fieldvalue, rowid])
            results23 = cursor22.fetchall()
            print(results23)
            # import pdb;
            # pdb.set_trace()

            json_data = json.dumps(results23)

            return HttpResponse(json_data, content_type="application/json")

        elif tbl == "tblDoc":
            cursor22 = connection.cursor()
            cursor22.callproc("spcustomerinvoicedocfieldsupdate", [fieldname, fieldvalue, docid])
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
                    "pretag_tbldockind, "  # 25
                    "D.wherefromdocid_tbldoc, "
                    "D.wheretodocid_tbldoc, "
                    "Dfrom.companyname_tblcompanies_ctbldoc as companywherefromdeno, "
                    "Dto.companyname_tblcompanies_ctbldoc as companywheretodeno, "
                    "D.stocktakingdeno_tbldoc, "  # 30
                    "D.denoenabledflag_tbldoc "

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
                    "round((((unitsalespriceACU_tblDoc_details-(purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details))/(unitsalespriceACU_tblDoc_details))*100),1) as unitsalespricemargin, "  # 20
                    "round((listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as listpriceACU, "
                    "(100-round(((unitsalespriceACU_tblDoc_details/(listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details))*100),1)) as discount, "
                    "unit_tbldocdetails, "
                    "companyname_tblcompanies, "
                    "supplierdescription_tblProduct_ctblDoc_details, "
                    "IF (serviceflag_tblproduct=1, 0, podocdetailsidforlabel_tbldocdetails) "
                    #                        "serviceflag_tblproduct "

                    "FROM quotation_tbldoc_details as DD "

                    "LEFT JOIN quotation_tblproduct as P "
                    "ON DD.Productid_tblDoc_details_id = P.Productid_tblProduct "

                    "JOIN quotation_tblcompanies as C "
                    "ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "

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

    return render(request, 'quotation/customerinvoice.html', {'doc': doc,
                                                           'docdetails': docdetails,
                                                           'companyid': companyid,
                                                           'nextchapternums': nextchapternums,
                                                           'creatordata': creatordata,
                                                           'currencycodes': currencycodes})


@login_required
def customerinvoiceprint(request, docid):
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
                    "docnumber_tbldoc, "  # 10
                    "creatorid_tbldoc, "
                    "creationtime_tbldoc, "
                    "title_tblcontacts_ctbldoc, "
                    "mobile_tblcontacts_ctbldoc, "
                    "email_tblcontacts_ctbldoc, "
                    "pcd_tblcompanies_ctbldoc, "
                    "town_tblcompanies_ctbldoc, "
                    "address_tblcompanies_ctbldoc, "
                    "total_tbldoc, "
                    "deliverydays_tbldoc, "  # 20
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
        "SELECT  "
        " 1, "
        #        "`Doc_detailsid_tblDoc_details`, "
        "sum(Qty_tblDoc_details), "
        "`Docid_tblDoc_details_id`, "
        "`customerdescription_tblProduct_ctblDoc_details`, "
        "`firstnum_tblDoc_details`, "
        "`fourthnum_tblDoc_details`, "
        "`secondnum_tblDoc_details`, "
        "`thirdnum_tblDoc_details`, "
        "`Note_tblDoc_details`, "
        "1, "
        #        "`creationtime_tblDoc_details`, "
        "purchase_price_tblproduct_ctblDoc_details, "  # 10
        "listprice_tblDoc_details, "
        "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
        "Productid_tblDoc_details_id, "
        "1, "
        #        "Doc_detailsid_tblDoc_details, "
        "unit_tbldocdetails, "
        "currencyrateinreport_tbldoc, "
        "unitsalespriceACU_tblDoc_details, "
        "1, "
        "1, "
        "1, "  # 20
        "1, "
        #        "round((unitsalespriceACU_tblDoc_details/currencyrateinreport_tbldoc),2) as unitsalespricetoreport, "
        #        "round((unitsalespriceACU_tblDoc_details/currencyrateinreport_tbldoc),2)*Qty_tblDoc_details as salespricetoreport, "
        #        "round((purchase_price_tblproduct_ctblDoc_details),2) as unitpurchasepricetoreport, " #20
        #        "round((purchase_price_tblproduct_ctblDoc_details),2)*Qty_tblDoc_details as purchasepricetoreport, "
        "1, "
        #        "podocdetailsidforlabel_tbldocdetails,"
        "discreteflag_tblproduct,"
        "serviceflag_tblproduct "


        "FROM quotation_tbldoc_details "

        "LEFT JOIN quotation_tbldoc "
        "ON quotation_tbldoc_details.Docid_tblDoc_details_id = quotation_tbldoc.Docid_tblDoc "

        "JOIN quotation_tblproduct "
        "ON quotation_tbldoc_details.Productid_tblDoc_details_id = quotation_tblproduct.Productid_tblProduct "

        "WHERE docid_tbldoc_details_id=%s "

        "GROUP BY "
        #        "`Doc_detailsid_tblDoc_details`, "
        #        "`Qty_tblDoc_details`, "
        "`Docid_tblDoc_details_id`, "
        "`customerdescription_tblProduct_ctblDoc_details`, "
        "`firstnum_tblDoc_details`, "
        "`fourthnum_tblDoc_details`, "
        "`secondnum_tblDoc_details`, "
        "`thirdnum_tblDoc_details`, "
        "`Note_tblDoc_details`, "
        #        "`creationtime_tblDoc_details`, "
        "purchase_price_tblproduct_ctblDoc_details, "  # 10
        "listprice_tblDoc_details, "
        "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, "
        "Productid_tblDoc_details_id, "
        #        "Doc_detailsid_tblDoc_details, "
        "unit_tbldocdetails, "
        "currencyrateinreport_tbldoc, "
        "unitsalespriceACU_tblDoc_details, "
        #        "unitsalespricetoreport, "
        #        "salespricetoreport, "
        #        "unitpurchasepricetoreport, " #20
        #        "purchasepricetoreport, "
        #        "podocdetailsidforlabel_tbldocdetails,"
        "discreteflag_tblproduct,"
        "serviceflag_tblproduct "

        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
        [docid])
    docdetails = cursor3.fetchall()

    cursor14 = connection.cursor()
    cursor14.execute("SELECT "
                     "`Docid_tblDoc_details_id`, "
                     "Productid_tblDoc_details_id, "
                     "podocdetailsidforlabel_tbldocdetails, "
                     "Qty_tblDoc_details, "
                     "unit_tbldocdetails "

                     "FROM quotation_tbldoc_details "

                     "WHERE Docid_tblDoc_details_id=%s", [docid])
    labelids = cursor14.fetchall()

    # labelids to table begin
    # aim: enablelabelkindflag set to 1 at first instance of product that the print form writes the "Unique id" or "batch id" text
    # only once at thebeginning in line
    cursor22 = connection.cursor()
    cursor22.execute("DROP TEMPORARY TABLE IF EXISTS labelidtemptable;")
    cursor22.execute("CREATE TEMPORARY TABLE IF NOT EXISTS labelidtemptable "
                     "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                     "     docid_tblLabelidtemptable INT(11) NOT NULL, "
                     "     productid_tblLabelidtemptable INT(11) NOT NULL, "
                     "     podocdetailsidforlabel_tblLabelidtemptable INT(11) NOT NULL, "
                     "     qty_tblLabelidtemptable DECIMAL(10,1) NULL,"
                     "     unit_tblLabelidtemptable varchar(20) NULL,"
                     "     enablelabelkindflag_tblLabelidtemptable INT(11) NULL) "

                     "      ENGINE=INNODB "
                     "    ; ")

    for x in labelids:
        to_docid_tblLabelidtemptable = x[0]
        to_productid_tblLabelidtemptable = x[1]
        to_podocdetailsidforlabel_tblLabelidtemptable = x[2]
        to_qty_tblLabelidtemptable = x[3]
        to_unit_tblLabelidtemptable = x[4]

        cursor22.execute("INSERT INTO labelidtemptable ("
                         "docid_tblLabelidtemptable, "
                         "productid_tblLabelidtemptable, "
                         "podocdetailsidforlabel_tblLabelidtemptable, "
                         "qty_tblLabelidtemptable, "
                         "unit_tblLabelidtemptable) VALUES ('" + str(to_docid_tblLabelidtemptable) + "', "
                                                                                                     "'" + str(
            to_productid_tblLabelidtemptable) + "', "
                                                "'" + str(to_podocdetailsidforlabel_tblLabelidtemptable) + "', "
                                                                                                           "'" + str(
            to_qty_tblLabelidtemptable) + "', "
                                          "'" + str(to_unit_tblLabelidtemptable) + "');")

    cursor22.execute("SELECT   "
                     "auxid, "
                     "docid_tblLabelidtemptable, "
                     "productid_tblLabelidtemptable, "
                     "podocdetailsidforlabel_tblLabelidtemptable, "
                     "qty_tblLabelidtemptable, "
                     "unit_tblLabelidtemptable "

                     "FROM labelidtemptable ")
    labelidtemptables = cursor22.fetchall()
    # labelids to table end

    # enablelabelkindflag update begin
    for x in labelidtemptables:
        auxid = x[0]
        productid = x[2]

        cursor22.execute("SELECT min(auxid) "
                         "FROM labelidtemptable "
                         "WHERE productid_tblLabelidtemptable=%s", [productid])
        labelidtemptableresults = cursor22.fetchall()

        for x2 in labelidtemptableresults:
            minauxidforproduct = x2[0]

        cursor22.execute("UPDATE labelidtemptable SET "
                         "enablelabelkindflag_tblLabelidtemptable=1 "
                         "WHERE auxid =%s ", [minauxidforproduct])

        a = 1
    # labelidtemptable table:
    # auxid, enablelabelkindflag_tblLabelidtemptable,  productid_tblLabelidtemptable
    # 1 1 9
    # 2 null 9
    # 3 null 9
    # 4 1 33
    # 5 null 33
    cursor22.execute("SELECT   "
                     "auxid, "
                     "docid_tblLabelidtemptable, "
                     "productid_tblLabelidtemptable, "
                     "podocdetailsidforlabel_tblLabelidtemptable, "
                     "qty_tblLabelidtemptable, "
                     "unit_tblLabelidtemptable, "
                     "enablelabelkindflag_tblLabelidtemptable "

                     "FROM labelidtemptable ")
    labelidtemptableswithenablelabelkindflagset = cursor22.fetchall()

    # enablelabelkindflag update end

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

    return render(request, 'quotation/customerinvoiceprint.html', {'doc': doc, 'docdetails': docdetails,
                                                                'docdetailscount': docdetailscount,
                                                                'labelidtemptableswithenablelabelkindflagset': labelidtemptableswithenablelabelkindflagset,
                                                                'creatordata': creatordata})


@login_required
def customerinvoicebackpage(request):


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
@login_required
def customerinvoicemake(request, docid):

    creatorid = request.user.id

    cursor222 = connection.cursor()
    cursor222.execute("DROP TEMPORARY TABLE IF EXISTS denoddocdetailstemptable;")
    cursor222.execute("CREATE TEMPORARY TABLE IF NOT EXISTS denoddocdetailstemptable "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     denoddocdetailsid INT(11) NOT NULL) "
                    "      ENGINE=INNODB "
                    "    ; ")

    pk = docid
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "wheretodocid_tbldoc, "
                    "Doc_detailsid_tblDoc_details "

                    "FROM quotation_tbldoc "

                    "JOIN quotation_tbldoc_details "
                    "ON quotation_tbldoc.Docid_tblDoc = quotation_tbldoc_details.Docid_tblDoc_details_id "

                    "WHERE wheretodocid_tbldoc=%s and obsolete_tbldoc = 0 "
                    "order by docid_tbldoc desc",
                    [pk])
    denoddocdetails = cursor1.fetchall()

    for x in denoddocdetails:
        denoddocdetailsid = x[1]
        cursor222.execute("INSERT INTO denoddocdetailstemptable "
                        "(denoddocdetailsid) VALUES ('" + str(denoddocdetailsid) + "');")

    cursor222.execute("SELECT *  "
                    "FROM denoddocdetailstemptable ")
    denoddocdetailstemptableresult = cursor222.fetchall()

    pk = docid
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
                    "WHERE Doc_kindid_tblDoc_id = 3")
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
                    "wheretodocid_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [3, contactid,
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
                     docid,
                     accountcurrencycode,
                     docid])

    cursor3 = connection.cursor()
    cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
    results = cursor3.fetchall()
    for x in results:
        maxdocid = x[0]

    for x3 in denoddocdetailstemptableresult:
        denoddocdetailsid = x3[1]

        cursor3 = connection.cursor()
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
                        "supplierdescription_tblProduct_ctblDoc_details, "
                        "podocdetailsidforlabel_tbldocdetails "

                        "FROM quotation_tbldoc_details "

                        "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                        "ON "
                        "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "

                        "JOIN quotation_tbldoc as D "
                        "ON D.Docid_tblDoc=quotation_tbldoc_details.Docid_tblDoc_details_id "

                        "WHERE Doc_detailsid_tblDoc_details=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details LIMIT 1",
                        [denoddocdetailsid])
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

            purchase_priceclone = x[10]
            customerdescriptionclone = x[3]
            supplierdescriptionclone = x[25]

            currencyisocodeclone = x[12]
            listpricecomputed = x[11]
            currencyrateclone = x[16]
            unitclone = x[23]
            unitsalespriceACU = x[18]
            podocdetailsidforlabel = x[26]

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
                "podocdetailsidforlabel_tbldocdetails, "
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
                 podocdetailsidforlabel,
                 supplierdescriptionclone])


    rowsnumber = len(docdetails)
    customerordernumber = docid
    return redirect('customerinvoiceform', pk=maxdocid)


@login_required
def customerinvoicemakexxx(request):
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

    for x11 in range(0,len(productidlist),2):
        productid = productidlist[x11+0]
        productqty = productidlist[x11+1]

        cursor2.execute("INSERT INTO denofromstock "
                        "(productid, productqty) VALUES ('" + str(productid) + "', "
                                            "'" + str(productqty) + "');")


    cursor2.execute("SELECT *  "
                    "FROM denofromstock ")
    tables = cursor2.fetchall()
    #import pdb;
    #pdb.set_trace()

    pk = customerordernumber
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
                     customerordernumber,
                     accountcurrencycode,
                     788,
                     customerordernumber])

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

    for x3 in tables:
        productid = x3[1]
        productqty = x3[2]

        cursor3 = connection.cursor()
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

                        "JOIN quotation_tbldoc as D "
                        "ON D.Docid_tblDoc=quotation_tbldoc_details.Docid_tblDoc_details_id "

                        "WHERE Docid_tblDoc_details_id=%s and Productid_tblDoc_details_id=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details LIMIT 1",
                        [customerordernumber, productid])
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
                 productqty,
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
        #import pdb;
        #pdb.set_trace()

    return render(request, 'quotation/pohandlerreceptionredirecturl.html', {})
def customerinvoicerowremove(request, pk):
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

    return redirect('customerinvoiceform', pk=na)
