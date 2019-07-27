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

    return render(request, 'quotation/pohandlerframe.html', {})

def pohandlerfieldsupdate(request):
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
def pohandlersearchresults(request):
    receivedstatus = request.POST['receivedstatus']
    print(receivedstatus)

    if receivedstatus == 'false':
        receivedstatusphrase = "and DDdeno.denodocnumber is null "
    else:
        receivedstatusphrase = ""
    searchphrase = receivedstatusphrase


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
                    "DD2.corcompany, "  # 31
    
                    "DD.dateofarrival_tbldocdetails, "
                    "companyname_tblcompanies_ctbldoc as supplier,"
                    "Docid_tblDoc as podocid, "
                    "pretag_tbldockind as popretag, "
                    "docnumber_tbldoc as podocnumber, "
                    
                    "DDdeno.denodocdetails, "
                    "DDdeno.denodocnumber, "    
                    "DDdeno.denopretag, "    
                    "DDdeno.denodocid " #40    
    
                    "FROM quotation_tbldoc_details as DD "
    
                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x ON DD.Productid_tblDoc_details_id = x.Productid_tblProduct "
                    "JOIN quotation_tblcompanies as C ON DD.suppliercompanyid_tbldocdetails = C.companyid_tblcompanies "
    
                    "JOIN quotation_tbldoc "
                    "ON quotation_tbldoc.Docid_tblDoc=DD.Docid_tblDoc_details_id "
    
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
    
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

                   "LEFT JOIN    (SELECT (Doc_detailsid_tblDoc_details) as denodocdetails, "
                    "               denotopodetailslink_tbldocdetails, "
                    "               (docnumber_tbldoc) as denodocnumber, "
                    "               (pretag_tbldockind) as denopretag, "
                    "               (docid) as denodocid "
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
                    "            ) as DDdeno "
                    "ON DD.Doc_detailsid_tblDoc_details=DDdeno.denotopodetailslink_tbldocdetails "
    
                    "WHERE Doc_kindid_tblDoc_id=7 and obsolete_tbldoc = 0 " + searchphrase + " "
                    "order by DD.Docid_tblDoc_details_id, firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details")
    pos = cursor3.fetchall()
    porowsnumber = len(pos)

    return render(request, 'quotation/pohandler.html', {'pos': pos,
                                                        'porowsnumber': porowsnumber})
def pohandlerrowsourceforarrivaldates(request):
    cursor0 = connection.cursor()
    cursor0.execute(
            "SELECT dateofarrival_tbldocdetails, "
            "DDdeno.denodocnumber "
            
            "FROM quotation_tbldoc_details as DD "
    
            "JOIN quotation_tbldoc "
            "ON quotation_tbldoc.Docid_tblDoc=DD.Docid_tblDoc_details_id "

           "LEFT JOIN    (SELECT "
            "               denotopodetailslink_tbldocdetails, "
            "               (docnumber_tbldoc) as denodocnumber "

            "               FROM quotation_tbldoc_details as DD2 "

            "               JOIN (SELECT docnumber_tbldoc, "
            "                            (COALESCE(Docid_tblDoc, 0)) as docid "
    
            "                       FROM quotation_tbldoc"

            "                       WHERE obsolete_tbldoc = 0"
            "                    ) as D"
            "               ON D.docid=DD2.Docid_tblDoc_details_id "
            "            ) as DDdeno "
            "ON DD.Doc_detailsid_tblDoc_details=DDdeno.denotopodetailslink_tbldocdetails "

    
            "WHERE dateofarrival_tbldocdetails is not null and obsolete_tbldoc = 0 and DDdeno.denodocnumber is null "
            "GROUP BY dateofarrival_tbldocdetails, DDdeno.denodocnumber "
            "ORDER BY dateofarrival_tbldocdetails desc")

    arrivaldates = cursor0.fetchall()

    rownmbs=len(arrivaldates)

    return render(request, 'quotation/pohandlerrowsourceforarrivaldates.html', {'arrivaldates': arrivaldates, 'rownmbs': rownmbs})


def pohandlerreception(request): #from pohandlerform
    dateofarrival = request.POST['dateofarrival']
    dateofarrivallistraw = request.POST['dateofarrivallist']
    dateofarrivallist = json.loads(dateofarrivallistraw)

    creatorid = request.user.id

#splitting start
    dateofarrivallistsplitted= []
    for x1 in range(0, len(dateofarrivallist), 4):
        podocdetailsid = dateofarrivallist[x1+0]
        podocid = dateofarrivallist[x1+1]
        cordocid = dateofarrivallist[x1+2]
        dateofarrivaldate = dateofarrivallist[x1+3]

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
                        "round((((unitsalespriceACU_tblDoc_details-(purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details))/(unitsalespriceACU_tblDoc_details))*100),1) as unitsalespricemargin, " #20
                        "round((listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as listpriceACU, "
                        "(100-round(((unitsalespriceACU_tblDoc_details/(listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details))*100),1)) as discount, "
                        "unit_tbldocdetails, "
                        "suppliercompanyid_tbldocdetails, "
                        "podetailslink_tbldocdetails, "
                        "serviceflag_tblproduct, "
                        "discreteflag_tblproduct "
                        
                        "FROM quotation_tbldoc_details "
                        "LEFT JOIN quotation_tblproduct as P "
                        "ON "
                        "quotation_tbldoc_details.Productid_tblDoc_details_id = P.Productid_tblProduct "

                        "WHERE Doc_detailsid_tblDoc_details=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                        [podocdetailsid])
        docdetails = cursor3.fetchall()

        for x in docdetails:
            qty = x[1]
            docid = x[2]
            firstnum = x[4]
            fourthnum = x[5]
            secondnum = x[6]
            thirdnum = x[7]
            note = x[8]
            productid = x[13]
            currencyrate = x[16]
            suppliercompanyid = x[24]
            podetailslink = x[25]

            purchase_priceclone = x[10]
            customerdescriptionclone = x[3]
            currencyisocodeclone = x[12]
            listpricecomputed = x[11]
            currencyrateclone = x[16]
            unitclone = x[23]
            unitsalespriceACU = x[18]
            serviceflag = x[26]
            discreteflag = x[27]
        #import pdb;
        #pdb.set_trace()

        if serviceflag == 1: # if service no split
            appendvar = (podocdetailsid, podocid, cordocid, dateofarrivaldate)
            dateofarrivallistsplitted.append(appendvar) # splitted list name signs that processed the list
        else:
            if discreteflag == 0: # if indiscret (batched non unique) no split
                appendvar = (podocdetailsid, podocid, cordocid, dateofarrivaldate)
                dateofarrivallistsplitted.append(appendvar)
            else:

                cursor4 = connection.cursor()
                for x2 in range(int(qty)):
                    if qty != 1:  # if already splitted dont split again
                        # let's split!

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
                            "podetailslink_tbldocdetails, "
                            "creatorid_tbldocdetails, "
                            "dateofarrival_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

                            [docid,
                             1,
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
                             podetailslink,
                             creatorid,
                             dateofarrivaldate])


                    if qty != 1:  # if was splitted
                        cursor3 = connection.cursor()
                        cursor3.execute("SELECT max(Doc_detailsid_tblDoc_details) FROM quotation_tbldoc_details WHERE creatorid_tbldocdetails=%s", [creatorid])
                        results = cursor3.fetchall()
                        for x in results:
                            maxdocdetailsid = x[0]


                        appendvar = (maxdocdetailsid, podocid, cordocid, dateofarrivaldate)
                        dateofarrivallistsplitted.append(appendvar)
                    else:
                        appendvar = (podocdetailsid, podocid, cordocid, dateofarrivaldate)
                        dateofarrivallistsplitted.append(appendvar)


                    if qty != 1:  # if was splitted
                        # let's delete!
                        cursor2 = connection.cursor()
                        cursor2.execute(
                            "DELETE FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [podocdetailsid])


#splitting end

#dateofarrivallistsplitted to table start
    cursor2 = connection.cursor()
    cursor2.execute("DROP TEMPORARY TABLE IF EXISTS porows;")
    cursor2.execute("CREATE TEMPORARY TABLE IF NOT EXISTS porows "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     podocdetailsid INT(11) NOT NULL, "
                    "     podocid INT(11) NULL, " 
                    "     cordocid INT(11) NULL, "
                    "     productid INT(11) NULL, "
                    "     arrivedqty DECIMAL(10,1) NULL,"
                    "     nop DECIMAL(10,1) NULL,"
                    "     dateofarrivaldate varchar(55) NULL, "
                    "     numberofitemstodeno INT(11) NULL) "
      
                    "      ENGINE=INNODB "
                    "    ; ")

    for x11 in range(len(dateofarrivallistsplitted)):
        podocdetailsid = dateofarrivallistsplitted[x11][0]
        podocid = dateofarrivallistsplitted[x11][1]
        cordocid = dateofarrivallistsplitted[x11][2]
        dateofarrivaldate = dateofarrivallistsplitted[x11][3]

        cursor2.execute("SELECT   "
                        "Productid_tblDoc_details_id,"
                        "Qty_tblDoc_details "

                         "FROM quotation_tbldoc_details "

                         "WHERE Doc_detailsid_tblDoc_details=%s ",
                         [podocdetailsid])
        productidresult = cursor2.fetchall()

        for x2 in productidresult:
            productid = x2[0]
            arrivedqty = x2[1]

        cursor2.execute("INSERT INTO porows (podocdetailsid, "
                        "podocid, "
                        "cordocid, "
                        "productid, "
                        "arrivedqty, "
                        "dateofarrivaldate) VALUES ('" + str(podocdetailsid) + "', "
                                                    "'" + str(podocid) + "', "
                                                    "'" + str(cordocid) + "', "
                                                    "'" + str(productid) + "', "
                                                    "'" + str(arrivedqty) + "', "
                                                    "'" + str(dateofarrivaldate) + "');")

    cursor2.execute("SELECT   "
                        "auxid, "
                        "podocdetailsid, "
                        "podocid, "
                        "cordocid, "
                        "productid, "
                        "arrivedqty, "
                        "dateofarrivaldate "

                        "FROM porows ")
    tables = cursor2.fetchall()
#dateofarrivallistsplitted to table end

    '''
    #docdetails per docid to table start
    for xx in tables:
        auxid = xx[0]
        podocid = xx[2]
        cordocid = xx[3]
        cursor2.execute("SELECT count(auxid) "
                        "FROM porows "
                        "WHERE podocid=%s and cordocid=%s "
                        "GROUP BY podocid, cordocid ",[podocid, cordocid])
        numberofitemstodenoresults = cursor2.fetchall()

        for x2 in numberofitemstodenoresults:
            numberofitemstodeno= x2[0]

        cursor2.execute("UPDATE porows SET " 
                        "numberofitemstodeno= %s "
                        "WHERE auxid =%s ", [numberofitemstodeno, auxid])
    # import pdb;
    # pdb.set_trace()

    #docdetails per docid to table end
    
#porows table:
    #auxid, numberofitemstodeno
    #1 1
    #2 2
    #3 2
    #4 1
    '''
#deliverynote making start
    cursor2.execute("SELECT "
                        "auxid, "
                        "podocdetailsid, "
                        "podocid, "
                        "cordocid, "
                        "productid, "
                        "arrivedqty, "
                        "dateofarrivaldate,"
                        "numberofitemstodeno "

                    "FROM porows ")
    tables2 = cursor2.fetchall()
    docmakercounter = 0
    #import pdb;
    #pdb.set_trace()

    # neededqtytemptable declaration before/outside the following for loop start
    cursor2 = connection.cursor()
    cursor2.execute("DROP TEMPORARY TABLE IF EXISTS neededqtytemptable;")
    cursor2.execute("CREATE TEMPORARY TABLE IF NOT EXISTS neededqtytemptable "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     podocdetailsid INT(11) NOT NULL, "
                    "     cororstockdocidto INT(11) NOT NULL, "
                    "     podocidfrom INT(11) NOT NULL, "
                    "     itemqty DECIMAL(10,1) NULL, "
                    "     numberofitemstodeno INT(11) NULL, "
                    "     subjecttext VARCHAR(255) NULL, "
                    "     denorole VARCHAR(255) NULL, "
                    "     cordocidroot INT(11) NULL) "

                    "      ENGINE=INNODB "
                    "    ; ")
    # neededqtytemptable declaration before/outside the following for loop end


    for x3 in tables2: #porows
        podocdetailsid = x3[1]
        podocid = x3[2]
        cordocid = x3[3]
        productid = x3[4]
        arrivedqty = x3[5]
        numberofitemstodeno = x3[7]

        cursor2.execute("SELECT "
                        "DD2cor.cordocid as cordocid, "
                        "DD1po.Docid_tblDoc_details_id as podocid, "
                        "DD1po.Doc_detailsid_tblDoc_details as docdetailsid, "
                        "DD2cor.corqty as corqty, "
                        "DD1po.Qty_tblDoc_details as poqty, "
                        "COALESCE(DD2cor.fromstockdocid,0) as fromstockdocid, "
                        "COALESCE(DD2cor.denodqty,0) as denodfromstockqty "

                        "FROM quotation_tbldoc_details as DD1po "

                        "LEFT JOIN (SELECT "
                        ""
                        "           Doc_detailsid_tblDoc_details, "
                        "           corqtysum.corqty as corqty, "
                        "           corqtysum.cordocid as cordocid, "
                        "           Denodfromstock.denodqty as denodqty, "
                        "           Denodfromstock.fromstockdocid as fromstockdocid, "
                        "           DD33cor.Productid_tblDoc_details_id as productid "
                        ""
                        "           FROM quotation_tbldoc_details as DD33cor "

                                    # corqtysum        
                                    "LEFT JOIN (SELECT "
            
                                    "           Docid_tblDoc as cordocid, "
                        "                       DD22.corqty as corqty,"
                        "                       DD22.productid as productid "
            
                                    "           FROM quotation_tbldoc as Dcor"

                                    "           LEFT JOIN   (SELECT "
                                    "                       Docid_tblDoc_details_id as docid, "
                                    "                       sum(Qty_tblDoc_details) as corqty, "
                                    "                       Productid_tblDoc_details_id as productid "
            
                                    "                       FROM quotation_tbldoc_details"
            
                                    "                       GROUP BY docid, productid "
                                    "                       ) as DD22 "
                                    "           ON Dcor.Docid_tblDoc = DD22.docid "

            
                                    "          ) as corqtysum "
                                    "ON DD33cor.Docid_tblDoc_details_id = corqtysum.cordocid and DD33cor.Productid_tblDoc_details_id = corqtysum.productid "

                                    # denodfromstocktocor        
                                    "LEFT JOIN (SELECT "
            
                                    "           wheretodocid_tbldoc, "
                                    "           sum(DD2.denodqty) as denodqty, "
                                    "           companyin.docid as fromstockdocid, "
                                    "           DD2.productid as productid "
            
                                    "           FROM quotation_tbldoc as Ddeno"
            
          "                                     JOIN (SELECT"
            "                                           Docid_tblDoc as docid, "
            "                                           lateststocktaking.companyid as companyid, "
            "                                           lateststocktaking.lateststocktaking as lateststocktaking "
            ""
            "                                           FROM quotation_tbldoc as D4 "
    
            "                                           JOIN (SELECT "
            "                                                            lateststocktaking_tblcompanies as lateststocktaking, "
            "                                                            C.Companyid_tblContacts_id as companyid, "
            "                                                            C.Contactid_tblContacts as contactid "
    
            "                                                            FROM quotation_tblcontacts as C "
    
            "                                                            JOIN quotation_tblcompanies as companies "
            "                                                            ON C.Companyid_tblContacts_id = companies.Companyid_tblCompanies "
    
            "                                                      ) as lateststocktaking "
            "                                           ON D4.Contactid_tblDoc_id = lateststocktaking.contactid "
    
            "                                           ) as companyin "
         "                                      ON Ddeno.wherefromdocid_tblDoc = companyin.docid "
            
            
                                    "           LEFT JOIN   (SELECT "
                                    "                       Docid_tblDoc_details_id as docid, "
                                    "                       sum(Qty_tblDoc_details) as denodqty, "
                                    "                       Productid_tblDoc_details_id as productid "
            
                                    "                       FROM quotation_tbldoc_details"
            
                                    "                       GROUP BY docid, productid "
                                    "                       ) as DD2 "
                                    "           ON Ddeno.Docid_tblDoc = DD2.docid "
            
                                    "           WHERE companyin.companyid in (9,10) and Ddeno.creationtime_tbldoc > companyin.lateststocktaking and obsolete_tbldoc=0 "
            
                                    "           GROUP BY wheretodocid_tbldoc, fromstockdocid, productid "
            
                                    "           ) AS Denodfromstock "
                                    "ON DD33cor.Docid_tblDoc_details_id = Denodfromstock.wheretodocid_tbldoc and DD33cor.Productid_tblDoc_details_id = Denodfromstock.productid "
                        ""
                        "           ) as DD2cor "
                        "ON DD1po.podetailslink_tbldocdetails=DD2cor.Doc_detailsid_tblDoc_details and DD1po.Productid_tblDoc_details_id = DD2cor.productid "

                        "WHERE DD1po.Doc_detailsid_tblDoc_details=%s ", [podocdetailsid])

        fromstockresult = cursor2.fetchall()

# sumarrivedqty determination begin
        toinoperatordocdetails = ""
        cursor2.execute("SELECT   "
                        "podocdetailsid "

                        "FROM porows "

                        "WHERE podocid=%s and cordocid=%s and productid=%s ",
                        [podocid, cordocid, productid])
        resultsarrived = cursor2.fetchall()

        for x in resultsarrived:
            podocdetailsidforprocessedarriveds = x[0]

#            if len(results) == 0:
#                cursor2.execute("INSERT INTO processedarrivedtemptable (processedpodocdetailsid) VALUES ('" + str(podocdetailsidforprocessedarriveds) + "');")
            toinoperatordocdetails = toinoperatordocdetails + str(podocdetailsidforprocessedarriveds) + ","

        if toinoperatordocdetails != "":
            toinoperatordocdetails = toinoperatordocdetails[: -1]
            searchphrase = " IN (" + toinoperatordocdetails + ")"
        else:
            searchphrase = "=0 "
        cursor2.execute("SELECT   "
                         "sum(arrivedqty) as sumarrivedqty "

                         "FROM porows "

                        "WHERE podocdetailsid" + searchphrase + " "

                        "GROUP BY cordocid, podocid, productid  ")
        sumarrivedqtyresult = cursor2.fetchall()

        if len(sumarrivedqtyresult) != 0:
            for x2 in sumarrivedqtyresult:
                sumarrivedqty = x2[0]
        else:
            sumarrivedqty = 0
#        import pdb;
#        pdb.set_trace()

        # sumarrivedqty determination end

        cursor2.execute("SELECT "
                        "DD2cor.cordocid as cordocid, "
                        "DD1po.Docid_tblDoc_details_id as podocid, "
                        "DD1po.Doc_detailsid_tblDoc_details, "
                        "DD2cor.corqty as corqty, "
                        "DD1po.Qty_tblDoc_details as poqty, "
                        "COALESCE(DD2cor.backtostockdocid,0), "
                        "COALESCE(DD2cor.Denodbacktostockqty,0) as Denodbacktostockqty "

                        "FROM quotation_tbldoc_details as DD1po "

                        "LEFT JOIN (SELECT "
                        ""
                        "           Doc_detailsid_tblDoc_details, "
                        "           corqtysum.corqty as corqty, "
                        "           corqtysum.cordocid as cordocid, "
                        "           DD33cor.Productid_tblDoc_details_id as productid, "
                        "           Denodbacktostock.Denodbacktostockqty as Denodbacktostockqty, "
                        "           Denodbacktostock.backtostockdocid as backtostockdocid "
                        ""
                        "           FROM quotation_tbldoc_details as DD33cor "

                        # corqtysum        
                        "LEFT JOIN (SELECT "

                        "           Docid_tblDoc as cordocid, "
                        "                       DD22.corqty as corqty,"
                        "                       DD22.productid as productid "

                        "           FROM quotation_tbldoc as Dcor"

                        "           LEFT JOIN   (SELECT "
                        "                       Docid_tblDoc_details_id as docid, "
                        "                       sum(Qty_tblDoc_details) as corqty, "
                        "                       Productid_tblDoc_details_id as productid "

                        "                       FROM quotation_tbldoc_details"

                        "                       GROUP BY docid, productid "
                        "                       ) as DD22 "
                        "           ON Dcor.Docid_tblDoc = DD22.docid "


                        "          ) as corqtysum "
                        "ON DD33cor.Docid_tblDoc_details_id = corqtysum.cordocid and DD33cor.Productid_tblDoc_details_id = corqtysum.productid "


                        # denodbacktostock
                        "LEFT JOIN (SELECT "

                        "           backtostockforcordocid_tbldoc, "
                        "           sum(DD2backtostock.denodqty) as denodbacktostockqty, "
                        "           companybacktostock.docid as backtostockdocid, "
                        "           DD2backtostock.productid as productid "

                        "           FROM quotation_tbldoc as Ddenobacktostock"

                        "                                               JOIN (SELECT"
                        "                                           Docid_tblDoc as docid, "
                        "                                           lateststocktaking.companyid as companyid, "
                        "                                           lateststocktaking.lateststocktaking as lateststocktaking "
                        ""
                        "                                           FROM quotation_tbldoc as D4 "

                        "                                           JOIN (SELECT "
                        "                                                            lateststocktaking_tblcompanies as lateststocktaking, "
                        "                                                            C.Companyid_tblContacts_id as companyid, "
                        "                                                            C.Contactid_tblContacts as contactid "

                        "                                                            FROM quotation_tblcontacts as C "

                        "                                                            JOIN quotation_tblcompanies as companies "
                        "                                                            ON C.Companyid_tblContacts_id = companies.Companyid_tblCompanies "

                        "                                                      ) as lateststocktaking "
                        "                                           ON D4.Contactid_tblDoc_id = lateststocktaking.contactid "

                        "                                   ) as companybacktostock "
                        "                       ON Ddenobacktostock.wheretodocid_tblDoc = companybacktostock.docid "


                        "           LEFT JOIN   (SELECT "
                        "                       Docid_tblDoc_details_id as docid, "
                        "                       sum(Qty_tblDoc_details) as denodqty, "
                        "                       Productid_tblDoc_details_id as productid "

                        "                       FROM quotation_tbldoc_details"

                        "                       GROUP BY docid, productid "
                        "                       ) as DD2backtostock "
                        "           ON Ddenobacktostock.Docid_tblDoc = DD2backtostock.docid "

                        "           WHERE companybacktostock.companyid in (9,10) and Ddenobacktostock.creationtime_tbldoc > companybacktostock.lateststocktaking and obsolete_tbldoc=0 "

                        "           GROUP BY backtostockforcordocid_tbldoc, backtostockdocid, productid "

                        "           ) AS Denodbacktostock "
                        "ON DD33cor.Docid_tblDoc_details_id = Denodbacktostock.backtostockforcordocid_tbldoc and DD33cor.Productid_tblDoc_details_id = Denodbacktostock.productid"

                        "           ) as DD2cor "
                        "ON DD1po.podetailslink_tbldocdetails=DD2cor.Doc_detailsid_tblDoc_details and DD1po.Productid_tblDoc_details_id = DD2cor.productid "

                        "WHERE DD1po.Doc_detailsid_tblDoc_details=%s", [podocdetailsid])

        backtostockresult = cursor2.fetchall()

        # items from stock and back to stock to list start
        fromstocklist = [] #result to list
        for x33 in fromstockresult:
            cordocid = x33[0]
            podocid = x33[1]
            coritemqty = x33[3]
            arriveditemqty = x33[4]
            fromstockstockdocid = x33[5]
            fromstockitemqty = x33[6]
            appendvarfromstocklist = (cordocid, podocid, podocdetailsid, coritemqty, arriveditemqty, fromstockstockdocid, fromstockitemqty)
            fromstocklist.append(appendvarfromstocklist)

        backtostocklist = [] #result to list
        for x332 in backtostockresult:
            cordocid = x332[0]
            podocid = x332[1]
            coritemqty = x332[3]
            arriveditemqty = x332[4]
            backtotockstockdocid = x332[5]
            backtostockitemqty = x332[6]
            appendvarbacktostocklist = (cordocid, podocid, podocdetailsid, coritemqty, arriveditemqty, backtotockstockdocid, backtostockitemqty)
            backtostocklist.append(appendvarbacktostocklist)
        def istherethislabelinneededqtylist ():
            if len(neededqtylist) == 0:
                checktext = 'no'
            else:
                for x11 in range(len(neededqtylist)):
                    podocdetailsidinlabelcheck = neededqtylist[x11][0]
                    if  podocdetailsidinlabelcheck == podocdetailsid:
                        checktext = 'yes'
                        break
                    else:
                        checktext = 'no'

            return checktext

        def underprogressqtyinneededqtytemptable (denoroleparameter, corstockdocidparameter, cordocidrootparameter):
            cursor2.execute("SELECT   "
                            "sum(itemqty) "

                            "FROM neededqtytemptable "
                            "WHERE cororstockdocidto=%s and cordocidroot=%s and denorole=%s "
                            "GROUP BY cororstockdocidto, cordocidroot, denorole ",[corstockdocidparameter, cordocidrootparameter, denoroleparameter])
            results = cursor2.fetchall()

            cursor2.execute("SELECT *   "

                            "FROM neededqtytemptable ")
            results2 = cursor2.fetchall()
            #import pdb;
            #pdb.set_trace()

            if len(results) != 0:
                for x in results:
                    underprogressqty = x[0]
            else:
                underprogressqty = 0


            return underprogressqty

        def discreteorindiscretorservicetheproduct (podocdetailsid):
            cursor3 = connection.cursor()
            cursor3.execute("SELECT  "
                            "Doc_detailsid_tblDoc_details, "
                            "serviceflag_tblproduct, "
                            "discreteflag_tblproduct "

                            "FROM quotation_tbldoc_details "

                            "LEFT JOIN quotation_tblproduct as P "
                            "ON quotation_tbldoc_details.Productid_tblDoc_details_id = P.Productid_tblProduct "

                            "WHERE Doc_detailsid_tblDoc_details=%s "
                            "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                            [podocdetailsid])
            docdetails = cursor3.fetchall()

            for x in docdetails:
                serviceflag = x[1]
                discreteflag = x[2]

            if serviceflag == 1:
                productkind = 'service'
            else:
                if discreteflag == 0:
                    productkind = 'indiscrete'
                else:
                    productkind = 'discrete'

            return productkind

        def sumtodirect (directqty, neededqtylist, cordocidfromstocklist):
            if directqty > 0:
                if discreteorindiscretorservicetheproduct(podocdetailsid) == 'indiscrete':
                    appendvarneededqtylist = (podocdetailsid, cordocid, podocidfromstocklist, directqty, subjectfordeno('directdeno', cordocidfromstocklist), 'todirect', cordocidfromstocklist)
                    neededqtylist.append(appendvarneededqtylist)
                elif discreteorindiscretorservicetheproduct(podocdetailsid) == 'discrete':
                    if istherethislabelinneededqtylist() == 'no':

                        appendvarneededqtylist = (podocdetailsid, cordocid, podocidfromstocklist, 1, subjectfordeno('directdeno', cordocidfromstocklist), 'todirect', cordocidfromstocklist)
                        neededqtylist.append(appendvarneededqtylist)

            return neededqtylist

        def sumtoback (backqty, neededqtylist, fromstockstockdocidinfromstocklist, cordocidfromstocklist):
            if backqty > 0:
                if discreteorindiscretorservicetheproduct(podocdetailsid) == 'indiscrete':
                    appendvarneededqtylist = (podocdetailsid, fromstockstockdocidinfromstocklist, podocidfromstocklist, backqty, subjectfordeno('backtostockdeno', cordocidfromstocklist), 'toback', cordocidfromstocklist)
                    neededqtylist.append(appendvarneededqtylist)
                elif discreteorindiscretorservicetheproduct(podocdetailsid) == 'discrete':
                    if istherethislabelinneededqtylist() == 'no':
                        appendvarneededqtylist = (podocdetailsid, fromstockstockdocidinfromstocklist, podocidfromstocklist, 1, subjectfordeno('backtostockdeno', cordocidfromstocklist), 'toback', cordocidfromstocklist)
                        neededqtylist.append(appendvarneededqtylist)

            return neededqtylist

        def sumtostock (stockitemqty, neededqtylist, surplusstockdocid, cordocidfromstocklist): #sumtostock should be sumtosurplus
            if stockitemqty > 0:
                if discreteorindiscretorservicetheproduct(podocdetailsid) == 'indiscrete':

                    appendvarneededqtylist = (podocdetailsid, surplusstockdocid, podocidfromstocklist, stockitemqty, subjectfordeno('surplustostockdeno', cordocidfromstocklist), 'tosurplus', cordocidfromstocklist)
                    neededqtylist.append(appendvarneededqtylist)
                elif discreteorindiscretorservicetheproduct(podocdetailsid) == 'discrete':
                    if istherethislabelinneededqtylist() == 'no':

                        appendvarneededqtylist = (podocdetailsid, surplusstockdocid, podocidfromstocklist, 1, subjectfordeno('surplustostockdeno', cordocidfromstocklist), 'tosurplus', cordocidfromstocklist)
                        neededqtylist.append(appendvarneededqtylist)

            return neededqtylist


        def subjectfordeno (denokind, cororstockdocid):

            cursor77 = connection.cursor()
            cursor77.execute("SELECT   "
                            "subject_tbldoc, "
                            "pretag_tbldockind, "
                            "docnumber_tbldoc, "
                            "companyname_tblcompanies_ctbldoc "

                            "FROM quotation_tbldoc "

                            "JOIN quotation_tbldoc_kind as DK "
                            "ON quotation_tbldoc.Doc_kindid_tblDoc_id = DK.Doc_kindid_tblDoc_kind "
                            
                            "WHERE docid_tbldoc=%s ",
                            [cororstockdocid])
            subjectresult = cursor77.fetchall()

            for x2 in subjectresult:
                subjectoriginal = x2[0]
                pretag = x2[1]
                docnumber = x2[2]
                companyname = x2[3]

            if denokind == 'directdeno':

                subjecttext = subjectoriginal

                return subjecttext
            elif denokind == 'backtostockdeno':
                subjecttext = 'Back - ' + companyname + ' ' + pretag + str(docnumber)
                return subjecttext


            elif denokind == 'surplustostockdeno':
                subjecttext = 'Surplus - ' + companyname + ' ' + pretag + str(docnumber)

                return subjecttext

#neededitemqtyaggregated start
        neededitemqtyaggregated = 0
        for x333 in range(len(fromstocklist)): # fromstock for a porow
            fromstockitemqtyinfromstocklist = fromstocklist[x333][6]
            neededitemqtyaggregated = neededitemqtyaggregated + fromstockitemqtyinfromstocklist

            fromstockitemqtyinbacktostocklist = 0

            if len(fromstocklist) != 0:

                for x3333 in range(len(backtostocklist)):
                    if len(backtostocklist) != 0:
                        fromstockitemqtyinbacktostocklist = backtostocklist[x3333][6]
                        neededitemqtyaggregated = neededitemqtyaggregated - fromstockitemqtyinbacktostocklist
# neededitemqtyaggregated end

        neededqtylist = []
        sumofbacktostockqty = 0
        for x333 in range(len(fromstocklist)): # fromstock for a porow
            neededitemqty = 0
            cordocidfromstocklist = fromstocklist[x333][0]
            podocidfromstocklist = fromstocklist[x333][1]
            coritemqtyinfromstocklist = fromstocklist[x333][3]
            arriveditemqtyinfromstocklist = fromstocklist[x333][4]
            fromstockstockdocidinfromstocklist = fromstocklist[x333][5]
            fromstockitemqtyinfromstocklist = fromstocklist[x333][6]

            fromstockitemqtyinbacktostocklist = 0

            if fromstockstockdocidinfromstocklist != 0:

                for x3333 in range(len(backtostocklist)):
                    arriveditemqtyinbacktostocklist = backtostocklist[x3333][4]
                    fromstockstockdocidinbacktostocklist = backtostocklist[x3333][5]
                    fromstockitemqtyinbacktostocklist = backtostocklist[x3333][6]

            if sumarrivedqty <= coritemqtyinfromstocklist - neededitemqtyaggregated:
                neededitemtodirectqty = coritemqtyinfromstocklist - underprogressqtyinneededqtytemptable('todirect', cordocidfromstocklist, cordocidfromstocklist)
                neededitemqty = 0
                neededtostockqty = 0
            else:
                neededitemqty = (fromstockitemqtyinfromstocklist - fromstockitemqtyinbacktostocklist) - underprogressqtyinneededqtytemptable('toback',fromstockstockdocidinfromstocklist, cordocidfromstocklist) #neededitemqty should be = neededitemtobackqty
                neededitemtodirectqty = coritemqtyinfromstocklist - fromstockitemqtyinfromstocklist + neededitemqty - underprogressqtyinneededqtytemptable('todirect', cordocidfromstocklist, cordocidfromstocklist)
                neededtostockqty = sumarrivedqty - (neededitemqty + neededitemtodirectqty)- underprogressqtyinneededqtytemptable('tosurplus',1382, cordocidfromstocklist) - underprogressqtyinneededqtytemptable('todirect',cordocidfromstocklist, cordocidfromstocklist) - underprogressqtyinneededqtytemptable('toback',fromstockstockdocidinfromstocklist, cordocidfromstocklist)

            if sumarrivedqty <= coritemqtyinfromstocklist:

                if neededitemqty == 0:
                    sumtodirect(sumarrivedqty, neededqtylist, cordocidfromstocklist)
                else:
                    sumtodirect(neededitemtodirectqty, neededqtylist, cordocidfromstocklist)
                    sumtoback(neededitemqty, neededqtylist, fromstockstockdocidinfromstocklist, cordocidfromstocklist )

            else:
                sumtostock(neededtostockqty, neededqtylist, 1382, cordocidfromstocklist)  # surplusstockdocid)
                sumtoback(neededitemqty, neededqtylist, fromstockstockdocidinfromstocklist,cordocidfromstocklist)
                sumtodirect(neededitemtodirectqty, neededqtylist, cordocidfromstocklist)

        #import pdb;
        #pdb.set_trace()

        # neededqtylist to temptable start
        for x11 in range(len(neededqtylist)):
            podocdetailsid = neededqtylist[x11][0]
            cororstockdocidto = neededqtylist[x11][1]
            podocidfrom = neededqtylist[x11][2]
            itemqty = neededqtylist[x11][3]
            subjecttext = neededqtylist[x11][4]
            denorole = neededqtylist[x11][5]
            cordocidroot = neededqtylist[x11][6]

            cursor2.execute("INSERT INTO neededqtytemptable (podocdetailsid, "
                            "cororstockdocidto, "
                            "podocidfrom, "
                            "subjecttext, "
                            "denorole, "
                            "cordocidroot, "
                            "itemqty) VALUES ('" + str(podocdetailsid) + "', "
                                                              "'" + str(cororstockdocidto) + "', "
                                                              "'" + str(podocidfrom) + "', "
                                                              "'" + str(subjecttext) + "', "
                                                              "'" + str(denorole) + "', "
                                                              "'" + str(cordocidroot) + "', "
                                                              "'" + str(itemqty) + "');")

        cursor2.execute("SELECT   "
                        "auxid, "
                        "podocdetailsid, "
                        "cororstockdocidto, "
                        "podocidfrom, "
                        "subjecttext, "
                        "denorole, "
                        "cordocidroot, "
                        "itemqty "

                        "FROM neededqtytemptable ")
        neededqtytemptable = cursor2.fetchall()
        # neededqtylist to temptable end

        import pdb;
        pdb.set_trace()
        d = 1




# docdetails per docid to neededqtytemptable start
    for xx in neededqtytemptable:
        auxid = xx[0]
        podocidfrom = xx[3]
        cororstockdocidto = xx[2]
        denorole = xx[5]

        cursor2.execute("SELECT count(auxid) "
                        "FROM neededqtytemptable "
                        "WHERE podocidfrom=%s and cororstockdocidto=%s and denorole=%s"
                        "GROUP BY podocidfrom, cororstockdocidto, denorole ", [podocidfrom, cororstockdocidto, denorole])
        numberofitemstodenoresults = cursor2.fetchall()

        for x2 in numberofitemstodenoresults:
            numberofitemstodeno = x2[0]

        cursor2.execute("UPDATE neededqtytemptable SET "
                        "numberofitemstodeno= %s "
                        "WHERE auxid =%s ", [numberofitemstodeno, auxid])

# docdetails per docid to neededqtytemptable end

    cursor2.execute("SELECT   "
                    "auxid, "
                    "podocdetailsid, "
                    "cororstockdocidto, "
                    "podocidfrom, "
                    "itemqty, "
                    "numberofitemstodeno, "
                    "subjecttext "
                    
                    "FROM neededqtytemptable ")
    neededqtytemptable = cursor2.fetchall()

    #import pdb;
    #pdb.set_trace()


    for x31 in neededqtytemptable:
        podocdetailsid = x31[1]
        podocid = x31[3]
        cordocid = x31[2]
        itemqty = x31[4]
        numberofitemstodeno = x31[5]
        subjecttext = x31[6]

        if docmakercounter  == 0: #doc create only once even multiple docdetails
            docmakercounter = numberofitemstodeno

            pk = cordocid
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
                            "wheretodocid_tbldoc,"
                            "denoenabledflag_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            [8, contactid,
                             companynameclone,
                             firstnameclone,
                             lastnameclone,
                             prefacetext,
                             backpagetext,
                             prefacespectext,
                             subjecttext,
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
                             cordocid,
                             accountcurrencycode,
                             podocid,
                             cordocid,
                             1])


            cursor3 = connection.cursor()
            cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
            results = cursor3.fetchall()
            for x in results:
                maxdocid = x[0]

        docmakercounter -= 1 #doc maked flag

        cursor2.execute("SELECT  `Doc_detailsid_tblDoc_details`, "
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

                        "WHERE obsolete_tbldoc=0 and Doc_detailsid_tblDoc_details=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                        [podocdetailsid])
        docdetails = cursor2.fetchall()
        #import pdb;
        #pdb.set_trace()

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
                "supplierdescription_tblProduct_ctblDoc_details, "
                "podocdetailsidforlabel_tbldocdetails) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

                [maxdocid,
                 itemqty,
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
                 supplierdescriptionclone,
                 podocdetailsid])
#deliverynote making end

    return render(request, 'quotation/pohandlerreceptionredirecturl.html',{})
def pohandlersplit(request):
        newqty = request.POST['newqty']
        rowid = request.POST['rowid']

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
                        "round((((unitsalespriceACU_tblDoc_details-(purchase_price_tblproduct_ctblDoc_details * currencyrate_tblcurrency_ctblDoc_details))/(unitsalespriceACU_tblDoc_details))*100),1) as unitsalespricemargin, " #20
                        "round((listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details),2) as listpriceACU, "
                        "(100-round(((unitsalespriceACU_tblDoc_details/(listprice_tblDoc_details * currencyrate_tblcurrency_ctblDoc_details))*100),1)) as discount, "
                        "unit_tbldocdetails, "
                        "suppliercompanyid_tbldocdetails, "
                        "podetailslink_tbldocdetails, "
                        "supplierdescription_tblProduct_ctblDoc_details "

                        "FROM quotation_tbldoc_details "
                        "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                        "ON "
                        "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "
                        "WHERE Doc_detailsid_tblDoc_details=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                        [rowid])
        docdetails = cursor3.fetchall()
        #import pdb;
        #pdb.set_trace()

        for x in docdetails:
            modifiedqty = x[1]-int(newqty)
            docid = x[2]
            firstnum = x[4]
            fourthnum = x[5]
            secondnum = x[6]
            thirdnum = x[7]
            note = x[8]
            productid = x[13]
            currencyrate = x[16]
            suppliercompanyid = x[24]
            podetailslink = x[25]

            purchase_priceclone = x[10]
            customerdescriptionclone = x[3]
            currencyisocodeclone = x[12]
            listpricecomputed = x[11]
            currencyrateclone = x[16]
            unitclone = x[23]
            unitsalespriceACU = x[18]
            supplierdescriptionclone = x[26]

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
            "podetailslink_tbldocdetails, "
            "supplierdescription_tblProduct_ctblDoc_details) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

            [docid,
             newqty,
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
             podetailslink,
             supplierdescriptionclone])

        cursor2 = connection.cursor()
        cursor2.execute(
            "UPDATE quotation_tbldoc_details SET "
            "Qty_tblDoc_details= %s "
            "WHERE doc_detailsid_tbldoc_details =%s ", [modifiedqty, rowid])

        return render(request, 'quotation/pohandlersplitredirecturl.html', {})
