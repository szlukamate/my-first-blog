from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import datetime
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
import xml.etree.ElementTree as ET
import xml.dom.minidom as x12
import base64
# import pdb;
# pdb.set_trace()
@login_required
def customerinvoiceform(request, pk):

    BASE_DIR = settings.BASE_DIR
    creatorid = request.user.id

    xmlfilenameincustomerinvoicexmlfilesdictonary = BASE_DIR + '/customerinvoicexmlfiles/' + str(creatorid) + '/' + pk + '.xml'  # if exists...
    xmlfilenameincustomerinvoicepdfsdictonary = BASE_DIR + '/customerinvoicepdfs/' + pk + '.pdf'  # if exists...
    fs = FileSystemStorage()

    if request.method == "POST":
        selector = request.POST['selector']
        #import pdb;
        #pdb.set_trace()

        if selector == "dispatchthexmlcheck":
            # xml dispatch controlflag (dispatchthexml) check  begin

            if fs.exists(xmlfilenameincustomerinvoicexmlfilesdictonary):
                if fs.exists(xmlfilenameincustomerinvoicepdfsdictonary):
                    dispatchthexml = 0
                    print ('there is already pdf')
                    xmlfilecontent = 'empty: exist xml and pdf too'
                else:
                    file = open(xmlfilenameincustomerinvoicexmlfilesdictonary, 'r')
                    xmlfilecontent = file.read()
                    file.close()

                    dispatchthexml = 1
                    print ('exists xml but pdf...')

            else:
                dispatchthexml = 0
                print ('no xml')
                xmlfilecontent = 'empty: no xml'
            data = []
            data.append(dispatchthexml)
            data.append(xmlfilecontent)
            #data[1] = 44
            print (data)
            json_data = json.dumps(data)

            #    if fs.exists(xmlfilenameincustomerinvoicexmlfilesdictonary):
            #        file = open(xmlfilenameincustomerinvoicexmlfilesdictonary, 'r')
            #        xmlfilecontent = file.read()
            #        file.close()
            #    else:
            #        xmlfilecontent = 'empty'

            return HttpResponse(json_data, content_type="application/json")

            # xml dispatch controlflag (dispatchthexml) check end

        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        docid = request.POST['docid']
        fieldname = request.POST['fieldname']
        tbl = request.POST['tbl']
        #import pdb;
        #pdb.set_trace()

        if tbl == "tblDoc_details":
            cursor22 = connection.cursor()
            cursor22.callproc("spcustomerinvoicedocdetailsfieldsupdate", [fieldname, fieldvalue, rowid])
            results23 = cursor22.fetchall()
            print(results23)
            # import pdb;
            # pdb.set_trace()

            json_data = json.dumps(results23, indent=4, sort_keys=True, default=str)

            return HttpResponse(json_data, content_type="application/json")

        elif tbl == "tblDoc":
            cursor22 = connection.cursor()
            cursor22.callproc("spcustomerinvoicedocfieldsupdate", [fieldname, fieldvalue, docid])
            results23 = cursor22.fetchall()
            print(results23)

            json_data = json.dumps(results23, indent=4, sort_keys=True, default=str)

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
                    "D.denoenabledflag_tbldoc,"
                    "D.dateofcompletiononcustomerinvoice_tbldoc,"
                    "D.deadlineforpaymentoncustomerinvoice_tbldoc,"
                    "D.numberoforderoncustomerinvoice_tbldoc, "
                    "D.dateoforderoncustomerinvoice_tbldoc, "
                    "D.currencyincustomerinvoice_tbldoc, "
                    "D.currencyrateforitemsincustomerinvoice_tbldoc, "
                    "D.remarksincustomerinvoice_tbldoc "

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
                    "supplierdescription_tblProduct_ctblDoc_details, " #25
                    "podocdetailsidforlabel_tbldocdetails, "
                    "vatpercentincustomerinvoice_tbldocdetails "

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

    if fs.exists(xmlfilenameincustomerinvoicepdfsdictonary):
        pdfexists = 1
    else:
        pdfexists = 0

    if fs.exists(xmlfilenameincustomerinvoicexmlfilesdictonary):
        xmlexists = 1
    else:
        xmlexists = 0

    return render(request, 'quotation/customerinvoice.html', {'doc': doc,
                                                           'docdetails': docdetails,
                                                           'base_dir': BASE_DIR,
                                                           'pdfexists': pdfexists,
                                                           'xmlexists': xmlexists,
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
                    "currencyrateinreport_tbldoc, "
                    "dateofcompletiononcustomerinvoice_tbldoc,"
                    "deadlineforpaymentoncustomerinvoice_tbldoc," #25
                    "numberoforderoncustomerinvoice_tbldoc, "
                    "dateoforderoncustomerinvoice_tbldoc, "
                    "currencyincustomerinvoice_tbldoc,"
                    "remarksincustomerinvoice_tbldoc "

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
        "round((unitsalespriceACU_tblDoc_details/currencyrateforitemsincustomerinvoice_tbldoc),2) as unitsalespricetoreport, "
        "round((unitsalespriceACU_tblDoc_details/currencyrateforitemsincustomerinvoice_tbldoc),2)*sum(Qty_tblDoc_details) as netpricetoreport, "
        "1, "  # 20
        "1, "
        #        "round((purchase_price_tblproduct_ctblDoc_details),2) as unitpurchasepricetoreport, " #20
        #        "round((purchase_price_tblproduct_ctblDoc_details),2)*Qty_tblDoc_details as purchasepricetoreport, "
        "1, "
        #        "podocdetailsidforlabel_tbldocdetails,"
        "discreteflag_tblproduct,"
        "serviceflag_tblproduct, "
        "currencyrateforitemsincustomerinvoice_tbldoc, " #25
        "vatpercentincustomerinvoice_tbldocdetails, "
        "round((unitsalespriceACU_tblDoc_details/currencyrateforitemsincustomerinvoice_tbldoc),2)*(vatpercentincustomerinvoice_tbldocdetails/100)*sum(Qty_tblDoc_details) as vatvaluetoreport, "
        "round((unitsalespriceACU_tblDoc_details/currencyrateforitemsincustomerinvoice_tbldoc),2)*sum(Qty_tblDoc_details) + round((unitsalespriceACU_tblDoc_details/currencyrateforitemsincustomerinvoice_tbldoc),2)*(vatpercentincustomerinvoice_tbldocdetails/100)*sum(Qty_tblDoc_details) as grossprice "

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
        "serviceflag_tblproduct, "
        "vatpercentincustomerinvoice_tbldocdetails "

        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
        [docid])
    docdetails = cursor3.fetchall()

    docdetailscount = len(docdetails)

    cursor14 = connection.cursor()
    cursor14.execute("SELECT "
                     "`Docid_tblDoc_details_id`, "
                     "Productid_tblDoc_details_id, "
                     "podocdetailsidforlabel_tbldocdetails, "
                     "Qty_tblDoc_details, "
                     "unit_tbldocdetails, "
                     "Doc_detailsid_tblDoc_details, "
                     "Note_tblDoc_details "

                     "FROM quotation_tbldoc_details "

                     "WHERE Docid_tblDoc_details_id=%s", [docid])
    labelids = cursor14.fetchall()

    #import pdb;
    #pdb.set_trace()

    # labelids to table begin
    # aim: enablelabelkindflag set to 1 at first instance of product that the print form writes the "Unique id" or "batch id" text
    # only once at thebeginning in  line
    #
    cursor22 = connection.cursor()
    cursor22.execute("DROP TEMPORARY TABLE IF EXISTS labelidtemptable;")
    cursor22.execute("CREATE TEMPORARY TABLE IF NOT EXISTS labelidtemptable "
                     "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                     "     docid_tblLabelidtemptable INT(11) NOT NULL, "
                     "     productid_tblLabelidtemptable INT(11) NOT NULL, "
                     "     podocdetailsidforlabel_tblLabelidtemptable INT(11) NOT NULL, "
                     "     qty_tblLabelidtemptable DECIMAL(10,1) NULL,"
                     "     unit_tblLabelidtemptable varchar(20) NULL,"
                     "     enablelabelkindflag_tblLabelidtemptable INT(11) NULL,"
                     "      fromstockflag_tblLabelidtemptable INT(11) NULL,"
                     "      fromstockname_tblLabelidtemptable varchar(200) NULL, "
                     "      fromstocknameprintingenabled_tblLabelidtemptable INT(11) NULL, "
                     "      note_tblLabelidtemptable varchar(200) NULL) "

                     "      ENGINE=INNODB "
                     "    ; ")

    for x in labelids:
        to_docid_tblLabelidtemptable = x[0]
        to_productid_tblLabelidtemptable = x[1]
        to_podocdetailsidforlabel_tblLabelidtemptable = x[2]
        to_qty_tblLabelidtemptable = x[3]
        to_unit_tblLabelidtemptable = x[4]
        to_note_tblLabelidtemptable = x[6]

        # check labelid from stock or not begin
        if to_podocdetailsidforlabel_tblLabelidtemptable != None:

            cursor22.execute("SELECT   "
                             "customerorderdocidforcustomerinvoice_tbldoc "
                             ""
                             "FROM quotation_tbldoc "
                             ""
                             "WHERE Docid_tblDoc = %s ", [to_docid_tblLabelidtemptable])
            customerorderdocidresults = cursor22.fetchall()


            for x in customerorderdocidresults:
                customerorderdocid = x[0]


            cursor22.execute("SELECT   "
                             "D2.stockflag as stockflag, "
                             "D2.stockname as stockname "
                                                 
                             "FROM quotation_tbldoc_details DD "
                             
                             "JOIN (SELECT "
                             "      quotation_tbldoc.Docid_tblDoc, "
                             "      D1.stockflag as stockflag, "
                             "      D1.stockname as stockname "
                             ""
                             "      FROM quotation_tbldoc "

                                     "JOIN (SELECT "
                                     
                                     "       D0.docid_tbldoc, "
                                     "       D.stockflag as stockflag, "
                                     "       D.stockname as stockname "
                                     
                                     "       FROM quotation_tbldoc D0 "
                                     
                                     
                                             "JOIN (SELECT "
                                             "      docid_tbldoc, "
                                                   "Contactid_tblDoc_id, "
                                             "      CONT.stockflag as stockflag, "
                                             "      CONT.stockname as stockname "
                                                    
                                                   "FROM quotation_tbldoc "
                                             ""
                                             "      JOIN (SELECT "
                                             ""
                                             "           Contactid_tblContacts, "
                                             "           Companyid_tblContacts_id,"
                                             "           COMP.stockflag as stockflag,"
                                             "           COMP.stockname as stockname "
                
                                                         "FROM quotation_tblcontacts "
                                             
                                             "           JOIN (SELECT "
                                                             "Companyid_tblCompanies, "
                                             "                stockflag_tblcompanies as stockflag, "
                                                            " companyname_tblcompanies as stockname "                

                                                             "FROM quotation_tblcompanies "
                                             "               ) as COMP "
                                             "           ON quotation_tblcontacts.Companyid_tblContacts_id = COMP.Companyid_tblCompanies "
                                             
                            
                                                        ") as CONT"
                                             "      ON quotation_tbldoc.Contactid_tblDoc_id = CONT.Contactid_tblContacts "
                                                   ") as D "                          
                                             "ON D0.docid_tbldoc = D.docid_tbldoc "
                                    
                                           ") as D1 "
                                     "ON quotation_tbldoc.wherefromdocid_tbldoc = D1.docid_tbldoc "


                             "      ) as D2 "
                             "ON DD.Docid_tblDoc_details_id = D2.Docid_tblDoc "
                             
                             "JOIN quotation_tbldoc "
                             "ON DD.Docid_tblDoc_details_id=quotation_tbldoc.Docid_tblDoc "

                             "WHERE podocdetailsidforlabel_tbldocdetails=%s and Doc_kindid_tblDoc_id=8 and wheretodocid_tbldoc=%s ", [to_podocdetailsidforlabel_tblLabelidtemptable, customerorderdocid])
            stockflagresults = cursor22.fetchall()


            for x in stockflagresults:
                fromstockflag = x[0]
                fromstockname = x[1]


        # check labelid from stock or not end

        cursor22.execute("INSERT INTO labelidtemptable ("
                         "docid_tblLabelidtemptable, "
                         "productid_tblLabelidtemptable, "
                         "podocdetailsidforlabel_tblLabelidtemptable, "
                         "qty_tblLabelidtemptable, "
                         "fromstockflag_tblLabelidtemptable, "
                         "fromstockname_tblLabelidtemptable, "
                         "note_tblLabelidtemptable, "
                         "unit_tblLabelidtemptable) VALUES ('" + str(to_docid_tblLabelidtemptable) + "', "
                                                           "'" + str(to_productid_tblLabelidtemptable) + "', "
                                                           "'" + str(to_podocdetailsidforlabel_tblLabelidtemptable) + "', "
                                                           "'" + str(to_qty_tblLabelidtemptable) + "', "
                                                           "'" + str(fromstockflag) + "', "
                                                           "'" + str(fromstockname) + "', "
                                                           "'" + str(to_note_tblLabelidtemptable) + "', "
                                                           "'" + str(to_unit_tblLabelidtemptable) + "');")

    cursor22.execute("SELECT   "
                     "auxid, "
                     "docid_tblLabelidtemptable, "
                     "productid_tblLabelidtemptable, "
                     "podocdetailsidforlabel_tblLabelidtemptable, "
                     "qty_tblLabelidtemptable, "
                     "unit_tblLabelidtemptable, "
                     "fromstockflag_tblLabelidtemptable, "
                     "fromstockname_tblLabelidtemptable, "
                     "fromstocknameprintingenabled_tblLabelidtemptable, "
                     "note_tblLabelidtemptable "

                     "FROM labelidtemptable ")
    labelidtemptables = cursor22.fetchall()
    # labelids to table end


    # enablelabelkindflag and fromstocknameprintingenabled update begin
    for x in labelidtemptables:
        auxid = x[0]
        productid = x[2]
        fromstockname = x[7]
        note = x[9]

        #enablelabelkindflag set begin
        cursor22.execute("SELECT min(auxid) "
                         "FROM labelidtemptable "
                         "WHERE productid_tblLabelidtemptable=%s and note_tblLabelidtemptable=%s ", [productid, note])
        labelidtemptableresults = cursor22.fetchall()

        for x2 in labelidtemptableresults:
            minauxidforproduct = x2[0]
        cursor22.execute("UPDATE labelidtemptable SET "
                         "enablelabelkindflag_tblLabelidtemptable=1 "
                         "WHERE auxid =%s ", [minauxidforproduct])
        # enablelabelkindflag set end

        #fromstocknameprintingenabled set begin
        cursor22.execute("SELECT min(auxid) "
                         "FROM labelidtemptable "
                         "WHERE productid_tblLabelidtemptable=%s and fromstockname_tblLabelidtemptable=%s ", [productid, fromstockname])
        labelidtemptableresults = cursor22.fetchall()

        for x2 in labelidtemptableresults:
            minauxidforproductandfromstockname = x2[0]
        cursor22.execute("UPDATE labelidtemptable SET "
                         "fromstocknameprintingenabled_tblLabelidtemptable=1 "
                         "WHERE auxid =%s ", [minauxidforproductandfromstockname])
        #fromstocknameprintingenabled set end

        a = 1
        #enablelabelkindflag signs that the labelkind discrete or indiscrete
        # labelidtemptable table:
        # auxid, enablelabelkindflag_tblLabelidtemptable,  productid_tblLabelidtemptable, fromstocknameprintingenabled_tblLabelidtemptable, fromstockname_tblLabelidtemptable, note_tblLabelidtemptable
        # 1 1 9 1 note12 centralstock
        # 2 null 9 null note12 centralstock
        # 3 null 9 1 note12 stock2
        # 4 1 33 1 note12 stock2
        # 5 null 33 null note12 stock2

        # 6 1 9 1 note14 centralstock
        # 7 null 9 null note14 centralstock
        # 8 null 9 1 note14 stock2
        # 9 1 33 1 note14 stock2
        # 10 null 33 null note14 stock2

    cursor22.execute("SELECT   "
                     "auxid, "
                     "docid_tblLabelidtemptable, "
                     "productid_tblLabelidtemptable, "
                     "podocdetailsidforlabel_tblLabelidtemptable, "
                     "qty_tblLabelidtemptable, "
                     "unit_tblLabelidtemptable, "
                     "enablelabelkindflag_tblLabelidtemptable,"
                     "fromstockflag_tblLabelidtemptable,"
                     "fromstockname_tblLabelidtemptable, "
                     "fromstocknameprintingenabled_tblLabelidtemptable,"
                     "note_tblLabelidtemptable " #10

                     "FROM labelidtemptable ")
    labelidtemptableswithenablelabelkindflagset = cursor22.fetchall()

    #import pdb;
    #pdb.set_trace()

    # enablelabelkindflag and fromstocknameprintingenabled update end


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
        customerinvoiceid = request.POST['customerinvoiceid']
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
        [customerinvoiceid])

    doc = cursor0.fetchall()
    json_data = json.dumps(doc)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def customerinvoicemake(request, docid):
# invoice items to temptable begin
    creatorid = request.user.id
    today = datetime.date.today()

    cursor222 = connection.cursor()
    cursor222.execute("DROP TEMPORARY TABLE IF EXISTS denoddocdetailstemptable;")
    cursor222.execute("CREATE TEMPORARY TABLE IF NOT EXISTS denoddocdetailstemptable "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     denoddocdetailsid INT(11) NOT NULL) "
                    "      ENGINE=INNODB "
                    "    ; ")

    # which deno belongs to this order begin
    pk = docid
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "wheretodocid_tbldoc, "
                    "Doc_detailsid_tblDoc_details "

                    "FROM quotation_tbldoc "

                    "JOIN quotation_tbldoc_details "
                    "ON quotation_tbldoc.Docid_tblDoc = quotation_tbldoc_details.Docid_tblDoc_details_id "

                    "WHERE wheretodocid_tbldoc=%s and obsolete_tbldoc = 0 and Doc_kindid_tblDoc_id = 8 "
                    "order by docid_tbldoc desc",
                    [pk])
    denoddocdetails = cursor1.fetchall()
    # which deno belongs to this order end

    #import pdb;
    #pdb.set_trace()

    for x in denoddocdetails:
        denoddocdetailsid = x[1]
        cursor222.execute("INSERT INTO denoddocdetailstemptable "
                        "(denoddocdetailsid) VALUES ('" + str(denoddocdetailsid) + "');")

    cursor222.execute("SELECT *  "
                    "FROM denoddocdetailstemptable ")
    denoddocdetailstemptableresult = cursor222.fetchall()
# invoice items to temptable end

# select order doc variables begin
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
                    "address_tblcompanies_ctbldoc,"
                    "Doc_kindid_tblDoc_id, "
                    "pretag_tbldockind, "
                    "deferredpaymentdaysincustomerorder_tbldoc, "
                    "creationtime_tbldoc "

                    "FROM quotation_tbldoc "
                    
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

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
        docnumber = x[6]
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
        pretag = x[23]
        deferredpaymentdaysincustomerorder = x[24]
        dateofordertimestamp = x[25]
# select order doc variables end

    ordernumber = pretag + str(docnumber)
    deadlineforpayment = today + datetime.timedelta(days=deferredpaymentdaysincustomerorder)
    dateoforder = dateofordertimestamp.strftime('%Y-%m-%d')

    #import pdb;
    #pdb.set_trace()

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
                    "wheretodocid_tbldoc, "
                    "dateofcompletiononcustomerinvoice_tbldoc,"
                    "numberoforderoncustomerinvoice_tbldoc, "
                    "deadlineforpaymentoncustomerinvoice_tbldoc, "
                    "dateoforderoncustomerinvoice_tbldoc,"
                    "customerorderdocidforcustomerinvoice_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
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
                     docid,
                     today,
                     ordernumber,
                     deadlineforpayment,
                     dateoforder,
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
            cordocdetailsid = x[0]
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
                "supplierdescription_tblProduct_ctblDoc_details, "
                "cidetailslinkfromcor_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", #cordocdetailsid which is invoiced in this row

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
                 supplierdescriptionclone,
                 cordocdetailsid])

    #import pdb;
    #pdb.set_trace()

    rowsnumber = len(docdetails)
    customerordernumber = docid
    return redirect('customerinvoiceform', pk=maxdocid)

@login_required
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
@login_required
def customerinvoicedispatch(request):
    customerinvoiceid = request.POST['customerinvoiceid']
    dateofinvoicevalue = request.POST['dateofinvoicevalue']
    dateofcompletionvalue = request.POST['dateofcompletionvalue']
    deadlineforpaymentvalue = request.POST['deadlineforpaymentvalue']
    methodofpaymentvalue = request.POST['methodofpaymentvalue']
    currencyvalue = request.POST['currencyvalue']
    remarkstextarea = request.POST['remarkstextarea']
    numberofordervalue = request.POST['numberofordervalue']
    companynameandcontactname = request.POST['companynameandcontactname']
    pcd = request.POST['pcd']
    town = request.POST['town']
    address = request.POST['address']
    itemnumber = request.POST['itemnumber']
    itemdatalistraw = request.POST['itemdatalist']
    itemdatalist = json.loads(itemdatalistraw)

    creatorid = request.user.id
    BASE_DIR = settings.BASE_DIR

    #import pdb;
    #pdb.set_trace()

    root = ET.Element("xmlszamla")
    root.set('xmlns','http://www.szamlazz.hu/xmlszamla')
    root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:schemaLocation','http://www.szamlazz.hu/xmlszamla xmlszamla.xsd')

    beallitasok = ET.SubElement(root, "beallitasok")

    ET.SubElement(beallitasok, "felhasznalo").text = "szluka.mate@gmail.com"
    ET.SubElement(beallitasok, "jelszo").text = "bklmgiok"
    ET.SubElement(beallitasok, "szamlaagentkulcs").text = "8y3knm3ht4znt5ns8m3ht4zcdywfrm3ht4zycnwgxm"
    ET.SubElement(beallitasok, "eszamla").text = "true"
    ET.SubElement(beallitasok, "szamlaLetoltes").text = "true"
    ET.SubElement(beallitasok, "valaszVerzio").text = "2"

    fejlec = ET.SubElement(root, "fejlec")

    ET.SubElement(fejlec, "keltDatum").text = "" + dateofinvoicevalue + ""
    ET.SubElement(fejlec, "teljesitesDatum").text = "" + dateofcompletionvalue + ""
    ET.SubElement(fejlec, "fizetesiHataridoDatum").text = "" + deadlineforpaymentvalue + ""
    ET.SubElement(fejlec, "fizmod").text = "" + methodofpaymentvalue + ""
    ET.SubElement(fejlec, "penznem").text = "" + currencyvalue + ""
    ET.SubElement(fejlec, "szamlaNyelve").text = "en"
    ET.SubElement(fejlec, "megjegyzes").text = "" + remarkstextarea + ""
    ET.SubElement(fejlec, "arfolyamBank").text = "MNB"
    ET.SubElement(fejlec, "arfolyam").text = "0.0"
    ET.SubElement(fejlec, "rendelesSzam").text = "" + numberofordervalue + ""
    ET.SubElement(fejlec, "dijbekeroSzamlaszam").text = "dbszsz"
    ET.SubElement(fejlec, "elolegszamla").text = "false"
    ET.SubElement(fejlec, "vegszamla").text = "false"
    ET.SubElement(fejlec, "helyesbitoszamla").text = "false"
    ET.SubElement(fejlec, "helyesbitettSzamlaszam").text = "hbszsz"
    ET.SubElement(fejlec, "dijbekero").text = "false"
    ET.SubElement(fejlec, "szamlaszamElotag").text = "GIPS"

    elado = ET.SubElement(root, "elado")

    ET.SubElement(elado, "bank").text = "BB"
    ET.SubElement(elado, "bankszamlaszam").text = "11111111-22222222-33333333"
    ET.SubElement(elado, "emailReplyto").text = "szluka.mate@gmail.com"
    ET.SubElement(elado, "emailTargy").text = "Incoming Invoice"
    ET.SubElement(elado, "emailSzoveg").text = "FYKI"

    vevo = ET.SubElement(root, "vevo")

    ET.SubElement(vevo, "nev").text = "" + companynameandcontactname + ""
    ET.SubElement(vevo, "irsz").text = "" + pcd + ""
    ET.SubElement(vevo, "telepules").text = "" + town + ""
    ET.SubElement(vevo, "cim").text = "" + address + ""
    ET.SubElement(vevo, "email").text = "szluka.mate@gmail.com"
    ET.SubElement(vevo, "sendEmail").text = "false"
    ET.SubElement(vevo, "adoszam").text = "12345678-1-42"
    ET.SubElement(vevo, "postazasiNev").text = "" + companynameandcontactname + ""
    ET.SubElement(vevo, "postazasiIrsz").text = "" + pcd + ""
    ET.SubElement(vevo, "postazasiTelepules").text = "" + town + ""
    ET.SubElement(vevo, "postazasiCim").text = "" + address + ""
    ET.SubElement(vevo, "telefonszam").text = "+3611111111"
    ET.SubElement(vevo, "megjegyzes").text = "1"

    tetelek = ET.SubElement(root, "tetelek")
    for x in range(int(itemnumber)):
        tetel = ET.SubElement(tetelek, "tetel")

        description = itemdatalist[(10*x+0)]
        unit = itemdatalist[10*x+1]
        unitsalesprice = itemdatalist[10*x+2]
        vatpercent = itemdatalist[10*x+3]
        netprice = itemdatalist[10*x+4]
        vatvalue = itemdatalist[10*x+5]
        grossprice = itemdatalist[10*x+6]
        qty = itemdatalist[10*x+7]
        note = itemdatalist[10*x+8]
        label = itemdatalist[10*x+9]


        #import pdb;
        #pdb.set_trace()

        ET.SubElement(tetel, "megnevezes").text = "" + description + ""
        ET.SubElement(tetel, "mennyiseg").text = "" + qty + ""
        ET.SubElement(tetel, "mennyisegiEgyseg").text = "" + unit + ""
        ET.SubElement(tetel, "nettoEgysegar").text = "" + unitsalesprice + ""
        ET.SubElement(tetel, "afakulcs").text ="" + vatpercent + ""
        ET.SubElement(tetel, "nettoErtek").text = "" + netprice + ""
        ET.SubElement(tetel, "afaErtek").text = "" + vatvalue + ""
        ET.SubElement(tetel, "bruttoErtek").text = "" + grossprice + ""
        ET.SubElement(tetel, "megjegyzes").text = "" + note + "\n" + label + ""


    tree = ET.ElementTree(root)
    # delete/make folder with creatorid
    subprocess.call('if [ ! -d "' + BASE_DIR + '/customerinvoicexmlfiles/' + str(creatorid) + '" ]; then mkdir ' + BASE_DIR + '/customerinvoicexmlfiles/' + str(creatorid) + '  ;else rm -rf ' + BASE_DIR + '/customerinvoicexmlfiles/' + str(creatorid) + ' && mkdir ' + BASE_DIR + '/customerinvoicexmlfiles/' + str(creatorid) + ';  fi', shell=True)

    xmlfilename = BASE_DIR + '/customerinvoicexmlfiles/' + str(creatorid) + '/' + customerinvoiceid + '.xml'
    tree.write(xmlfilename, xml_declaration=True, encoding='utf-8')


# making prettyxml begin

    file = open(xmlfilename, 'r')
    xml_string = file.read()
    file.close()

    parsed_xml = x12.parseString(xml_string)
    pretty_xml_as_string = parsed_xml.toprettyxml()

    file = open(xmlfilename, 'w')
    file.write(pretty_xml_as_string)
    file.close()

# making prettyxml begin

    #import pdb;
    #pdb.set_trace()



    return render(request, 'quotation/customerinvoicedispatchredirecturl.html', {'pk': customerinvoiceid})
@login_required
def customerinvoicexmlresponsepdfstacking(request):
    customerinvoicedocid = request.POST['customerinvoicedocid']
    pdfstringbase64 = request.POST['pdfstringbase64']
    pdfstring = base64.b64decode(pdfstringbase64)
    #import pdb;
    #pdb.set_trace()


    BASE_DIR = settings.BASE_DIR

    xmlstringtopdffilename = BASE_DIR + '/customerinvoicepdfs/' + customerinvoicedocid + '.pdf'
    file = open(xmlstringtopdffilename, 'wb')
    file.write(pdfstring)
    file.close()

    return render(request, 'quotation/customerinvoicexmlresponsepdfstackingredirecturl.html', {'pk': customerinvoicedocid})
@login_required
def customerinvoiceviewpdf(request, pk):
    BASE_DIR = settings.BASE_DIR

    fs = FileSystemStorage()
    storedfilename = BASE_DIR + '/customerinvoicepdfs/' + str(pk) + '.pdf'
    if fs.exists(storedfilename):
        with fs.open(storedfilename) as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="output.pdf"'
            return response
    else:
        return HttpResponseNotFound("The requested pdf was not found in our server.")
@login_required
def customerinvoiceshowpdfbutton(request):
    BASE_DIR = settings.BASE_DIR

    customerinvoicedocid = request.POST['customerinvoicedocid']
    return render(request, 'quotation/customerinvoicexmlresponsepdfstackingredirecturl.html', {'pk': customerinvoicedocid}) #same redirect when xmlresponse arrives therefore same redirecturl.html
