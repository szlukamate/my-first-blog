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
def stockmain(request):
    cursor22 = connection.cursor()
    cursor22.callproc("spstock", [])
    docdetails = cursor22.fetchall()


    #import pdb;
    #pdb.set_trace()

    rowsnumber = len(docdetails)
    customerordernumber = 1
    return render(request, 'quotation/stock.html', {'docdetails': docdetails,
                                                              'customerordernumber': customerordernumber,
                                                              'rowsnumber': rowsnumber})
@group_required("manager")
@login_required
def stocklabellist(request): # labels on stockform for particular product
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
            "Dingoing.inlabel as labelid, "
            "Dingoing.inqty as inqty, "
            "DDoutgoing.outqty as outqty, "
           "COALESCE(Dingoing.inqty,0)-COALESCE(DDoutgoing.outqty,0) as onstock " 
    
            "FROM quotation_tbldoc_details as DD "
#ingoing
            "JOIN (SELECT "
            "       D.Docid_tblDoc as docid, "
            "       DDingoing.inlabel as inlabel, "
            "       D.obsolete_tbldoc as obsolete, "
            "       sum(DDingoing.inqty) as inqty "
            ""
            "       FROM quotation_tbldoc as D "
            "   "
                    "JOIN (SELECT podocdetailsidforlabel_tbldocdetails as inlabel, "
                    "           Docid_tblDoc_details_id, "
                    "           sum(Qty_tblDoc_details) as inqty "
            
                    "           FROM quotation_tbldoc_details as DD2 "
            
                    "           JOIN quotation_tbldoc as D2"
                    "           ON DD2.Docid_tblDoc_details_id = D2.Docid_tblDoc "
            
                    "           WHERE D2.obsolete_tbldoc=0 "
                    "           GROUP BY inlabel, Docid_tblDoc_details_id "
                    
                    "           ) as DDingoing "
                    "ON D.Docid_tblDoc = DDingoing.Docid_tblDoc_details_id " 

                    
                    "JOIN quotation_tbldoc as D2 " #contactid lookup
                    "ON D.wheretodocid_tblDoc = D2.Docid_tblDoc "

            "       WHERE D2.Contactid_tblDoc_id=9 and D2.obsolete_tbldoc = 0 "             
        "           GROUP BY docid, "
        "                       inlabel, "
        "                       obsolete "
            ""
            
            "     ) as Dingoing "

            "ON DD.Docid_tblDoc_details_id = Dingoing.docid "

#outgoing    
            "LEFT JOIN (SELECT podocdetailsidforlabel_tbldocdetails as outlabel, "
            "           Docid_tblDoc_details_id, "
            "           sum(Qty_tblDoc_details) as outqty "
    
            "           FROM quotation_tbldoc_details as DD2 "
    
            "           JOIN quotation_tbldoc as D2"
            "           ON DD2.Docid_tblDoc_details_id = D2.Docid_tblDoc "

            "           WHERE obsolete_tbldoc=0 and wherefromdocid_tbldoc=788  "
            "           GROUP BY outlabel, Docid_tblDoc_details_id "
            
            "           ) as DDoutgoing "
            "ON DD.podocdetailsidforlabel_tbldocdetails = DDoutgoing.outlabel " #and outqty <> DDoutgoing.outqty "
   
        
            "JOIN quotation_tbldoc as D "
            "ON DD.Docid_tblDoc_details_id = D.Docid_tblDoc "

        
            "WHERE DD.Productid_tblDoc_details_id=%s and D.obsolete_tbldoc=0   " 
            "GROUP BY labelid, inqty, outqty, onstock  "
            "order by labelid desc "
            , [productid])


        resultspre = cursor0.fetchall()
        toresults = []
        results = []
        import pdb;
        pdb.set_trace()

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

@group_required("manager")
@login_required
def stocktakingpreform(request): # Settings --> Stocktaking
    cursor3 = connection.cursor()
    cursor3.execute(
        # stockflag_tblcompanies signs this company is a stock
        # lateststocktaking_tblcompanies signs tha date of last stocktaking which is showed in stockmain
        # denoenabledflag_tbldoc signs this doc counts in stockmain (is zero at stocktaking delivery note under assembling for several hours until ready)
        # stocktakingdeno_tbldoc signs this is a stocktaking deno (creationtimestamp of this row is for lateststocktaking_tblcompanies field)
        "SELECT "
        "Companyid_tblCompanies, "
        "companyname_tblcompanies, "
        "lateststocktaking_tblcompanies, "
        "latestenabledstocktaking.creationtime, "
        "latestenabledstocktaking.docid, "
        "latestdisabledstocktaking.creationtime, "
        "latestdisabledstocktaking.docid "
        ""
        "FROM quotation_tblcompanies as C "
#latestEnabledstocktaking
        "LEFT JOIN (SELECT "
        "      Companyid_tblContacts_id as companyid, "
        "      max(D.creationtime) as creationtime, "
        "      max(D.docid) as docid "

        "      FROM quotation_tblcontacts "
        
        "      JOIN (SELECT Docid_tblDoc as docid, "
        "            Contactid_tblDoc_id as contactid, "
        "            creationtime_tbldoc as creationtime "
        
        "            FROM quotation_tbldoc "
        ""
        "            WHERE denoenabledflag_tbldoc=1 and stocktakingdeno_tbldoc=1 and obsolete_tbldoc=0 "
        "            ) as D "
        "      ON quotation_tblcontacts.Contactid_tblContacts = D.contactid "
        "      GROUP BY companyid"
        "     ) as latestenabledstocktaking "
        "ON C.Companyid_tblCompanies = latestenabledstocktaking.companyid "
#latestDisabledstocktaking
        "LEFT JOIN (SELECT "
        "      Companyid_tblContacts_id as companyid, "
        "      D.creationtime as creationtime, "
        "      D.docid as docid "

        "      FROM quotation_tblcontacts "
        
        "      JOIN (SELECT Docid_tblDoc as docid, "
        "            Contactid_tblDoc_id as contactid, "
        "            creationtime_tbldoc as creationtime "
        
        "            FROM quotation_tbldoc "
        ""
        "            WHERE denoenabledflag_tbldoc=0 and stocktakingdeno_tbldoc=1 and obsolete_tbldoc=0 "
        "            ) as D "
        "      ON quotation_tblcontacts.Contactid_tblContacts = D.contactid "
        "     ) as latestdisabledstocktaking "
        "ON C.Companyid_tblCompanies = latestdisabledstocktaking.companyid "

        ""
        "WHERE stockflag_tblcompanies=1 ")

    results = cursor3.fetchall()
    # import pdb;
    # pdb.set_trace()

    rowsnumber = len(results)
    customerordernumber = 1
    return render(request, 'quotation/stocktakingpreform.html', {'results': results,
                                                    'customerordernumber': customerordernumber,
                                                    'rowsnumber': rowsnumber})

@group_required("manager")
@login_required
def stocknewdocforstocktaking(request): #create a new deno for stocktaking
    stockid = request.POST['stockid']

    cursor0 = connection.cursor()
    cursor0.execute("SELECT "
                    "Contactid_tblContacts "

                    "FROM quotation_tblcontacts "
                    "WHERE Companyid_tblContacts_id=%s ",
                    [stockid])
    results = cursor0.fetchall()
    for x in results:
        contactid = x[0]


    creatorid=request.user.id

    prefacetext = ""
    backpagetext = ""
    prefacespectext = ""
    subject = "Stocktaking"
    total = "Off"
    deliverydays = 0
    paymenttext = ""
    currencycodeinreport = "HUF"
    currencyrateinreport = 1
    accountcurrencycode = "HUF"

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
        companyid = instancesingle[2]  # for the lookup the default values in the tblcompanies (i.e. defaultpreface)
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
                        "WHERE Doc_kindid_tblDoc_id = 8")
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
                        "accountcurrencycode_tbldoc, "
                        "denoenabledflag_tbldoc, "
                        "stocktakingdeno_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [8, contactid, companynameclone, firstnameclone, lastnameclone, prefacetext, backpagetext,
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
                         0,
                         accountcurrencycode,
                         0,
                         1])

        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc WHERE creatorid_tbldoc=%s", [creatorid])
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        cursor0 = connection.cursor() #wheretodocid=docid
        cursor0.execute("UPDATE quotation_tbldoc "
                        "SET wheretodocid_tbldoc = %s "
                        "WHERE Docid_tblDoc = %s ",
                        [maxdocid, maxdocid])

        cursor4 = connection.cursor()
        cursor4.execute(
            "INSERT INTO quotation_tbldoc_details ( Docid_tblDoc_details_id) VALUES (%s)",
            [maxdocid])

    return render(request, 'quotation/stocktakingpreformredirecturl.html', {})
@group_required("manager")
@login_required
def stockcopyfromtimestampforstocktaking(request): #enabling a stocktaking
    stockid = request.POST['stockid']
    latestdisabledstocktakingdenotimestamp = request.POST['latestdisabledstocktakingdenotimestamp']
    latestdisabledstocktakingdenodocid = request.POST['latestdisabledstocktakingdenodocid']

    cursor0 = connection.cursor()
    cursor0.execute("UPDATE quotation_tblcompanies "
                    "SET lateststocktaking_tblcompanies = %s "
                    "WHERE Companyid_tblCompanies = %s ",
                    [latestdisabledstocktakingdenotimestamp, stockid])

    cursor1 = connection.cursor()
    cursor1.execute("UPDATE quotation_tbldoc "
                    "SET denoenabledflag_tbldoc = 1 "
                    "WHERE Docid_tblDoc = %s ",
                    [latestdisabledstocktakingdenodocid])


    return render(request, 'quotation/stocktakingpreformredirecturl.html', {})
