from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from array import *
# import pdb;
# pdb.set_trace()
def quotationform(request, pk):
    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        fieldname = request.POST['fieldname']

        cursor2 = connection.cursor()
        sqlquery = "UPDATE quotation_tbldoc_details SET " + fieldname + "= '" + fieldvalue + "' WHERE Doc_detailsid_tblDoc_details =" + rowid
        # import pdb;
        # pdb.set_trace()
        cursor2.execute(sqlquery)

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Docid_tblDoc, "
                    "Contactid_tblDoc_id, "
                    "Doc_kindid_tblDoc_id, "
                    "companyname_tblcompanies_ctbldoc, "
                    "firstname_tblcontacts_ctbldoc, "
                    "lastname_tblcontacts_ctbldoc "
                    "FROM quotation_tbldoc "
                    "WHERE docid_tbldoc=%s "
                    "order by docid_tbldoc desc",
                    [pk])
    doc = cursor1.fetchall()
    for x in doc:
        contactid = x[1]
    cursor4 = connection.cursor()
    cursor4.execute("SELECT companyid_tblcontacts_id "
                    "FROM quotation_tblcontacts "
                    "WHERE Contactid_tblContacts=%s ", [contactid])
    companyid = cursor4.fetchall()

    cursor3 = connection.cursor()
    cursor3.execute("SELECT  `Doc_detailsid_tblDoc_details`, `Qty_tblDoc_details`, `Docid_tblDoc_details_id`, `Product_description_tblProduct_ctblDoc_details`, `firstnum_tblDoc_details`, "
                    "`fourthnum_tblDoc_details`, `secondnum_tblDoc_details`, `thirdnum_tblDoc_details`, `Note_tblDoc_details`, `creationtime_tblDoc_details`, "
                    "purchase_price_tblproduct_ctblDoc_details, salesprice_tblDoc_details, currencyisocode_tblcurrency_ctblproduct_ctblDoc_details, Productid_tblDoc_details_id, "
                    "Doc_detailsid_tblDoc_details, COALESCE(Productid_tblProduct, 0) "
                    "FROM quotation_tbldoc_details "
                    "LEFT JOIN (SELECT Productid_tblProduct FROM quotation_tblproduct WHERE obsolete_tblproduct = 0) as x "
                    "ON "
                    "quotation_tbldoc_details.Productid_tblDoc_details_id = x.Productid_tblProduct "
                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [pk])
    docdetails = cursor3.fetchall()

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

    return render(request, 'quotation/quotation.html', {'doc': doc, 'docdetails': docdetails, 'companyid': companyid, 'nextchapternums' : nextchapternums})


'''
def quotationrowedit(request, pk):
        quotationrow = get_object_or_404(tblDoc_details, pk=pk)
        if request.method == "POST":
            form = quotationroweditForm(request.POST, instance=quotationrow)
            if form.is_valid():
                quotationrow.save()

                cursor = connection.cursor()

                cursor.execute("SELECT Docid_tblDoc_details_id FROM quotation_tbldoc_details WHERE Doc_detailsid_tblDoc_details=%s ", [pk])
                results = cursor.fetchall()

                for x in results:
                    na=x[0]

                transaction.commit()

                return redirect('quotationform', pk=na)

        else:
            form = quotationroweditForm(instance=quotationrow)
        return render(request, 'quotation/quotationrowedit.html', {'form': form})
'''


def quotationnewrow(request, pkdocid, pkproductid, pkdocdetailsid, nextfirstnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml, nextfourthnumonhtml ):
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT `Productid_tblProduct`, `purchase_price_tblproduct`, `Product_description_tblProduct`, "
        "`margin_tblproduct`,`currencyisocode_tblcurrency_ctblproduct` "
        "FROM `quotation_tblproduct` WHERE Productid_tblProduct= %s", [pkproductid])

    results = cursor0.fetchall()
    for instancesingle in results:
        purchase_priceclone = instancesingle[1]
        productdescriptionclone = instancesingle[2]
        currencyisocodeclone = instancesingle[4]

        marginfromproducttable=instancesingle[3]
        salespricecomputed=round((100*purchase_priceclone)/(100-marginfromproducttable),2)
    #import pdb;
    #pdb.set_trace()
    #pkdocdetailsid=3

    if int(pkdocdetailsid) != 0:
        cursor2 = connection.cursor()
        cursor2.execute(
            "UPDATE quotation_tbldoc_details SET "
            "Productid_tblDoc_details_id= %s, "
            "firstnum_tblDoc_details=%s, "
            "secondnum_tblDoc_details=%s, "
            "thirdnum_tblDoc_details=%s, "
            "fourthnum_tblDoc_details=%s, "
            "purchase_price_tblproduct_ctblDoc_details=%s, "
            "Product_description_tblProduct_ctblDoc_details=%s, "
            "currencyisocode_tblcurrency_ctblproduct_ctblDoc_details=%s, "
            "salesprice_tblDoc_details=%s "
            "WHERE doc_detailsid_tbldoc_details =%s ", [pkproductid, nextfirstnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml, nextfourthnumonhtml, purchase_priceclone,  productdescriptionclone, currencyisocodeclone, salespricecomputed, pkdocdetailsid])

    else:
        cursor1 = connection.cursor()
        cursor1.execute(
            "INSERT INTO quotation_tbldoc_details "
            "(`Qty_tblDoc_details`, `Docid_tblDoc_details_id`, `Productid_tblDoc_details_id`, `firstnum_tblDoc_details`, `fourthnum_tblDoc_details`, "
            "`secondnum_tblDoc_details`, `thirdnum_tblDoc_details`, `Note_tblDoc_details`, `purchase_price_tblproduct_ctblDoc_details`, "
            "`Product_description_tblProduct_ctblDoc_details`, `currencyisocode_tblcurrency_ctblproduct_ctblDoc_details`, salesprice_tblDoc_details) "
            "VALUES (1, %s, %s, %s,%s,%s,%s,'Defaultnote', %s, %s, %s, %s)",
            [pkdocid, pkproductid, nextfirstnumonhtml, nextfourthnumonhtml, nextsecondnumonhtml, nextthirdnumonhtml, purchase_priceclone, productdescriptionclone, currencyisocodeclone, salespricecomputed])
        transaction.commit()

    return redirect('quotationform', pk=pkdocid)

def quotationnewrowadd(request):
    if request.method == "POST":
        docdetailsid = request.POST['docdetailsid']
        quotationid = request.POST['quotationid']
        nextfirstnumonhtml= request.POST['nextfirstnumonhtml']
        nextsecondnumonhtml = request.POST['nextsecondnumonhtml']
        nextthirdnumonhtml = request.POST['nextthirdnumonhtml']
        nextfourthnumonhtml = request.POST['nextfourthnumonhtml']
        #import pdb;
        #pdb.set_trace()

        nextchapternumset = array('i', [int(nextfirstnumonhtml), int(nextsecondnumonhtml), int(nextthirdnumonhtml), int(nextfourthnumonhtml)])

    cursor1 = connection.cursor()
    cursor1.execute(
        "SELECT Productid_tblProduct, purchase_price_tblproduct, margin_tblproduct, round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as salesprice, "
        "Product_description_tblProduct, currencyisocode_tblcurrency_ctblproduct "
        "FROM quotation_tblproduct "
        "WHERE obsolete_tblproduct=0 ")
    products = cursor1.fetchall()
    transaction.commit()
    #return redirect('quotationform', pk=1)

    return render(request, 'quotation/quotationnewrowadd.html',{'products': products, 'docid': quotationid, 'nextchapternumset': nextchapternumset, 'docdetailsid' : docdetailsid })

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
        "quotation_tblcontacts.Firstname_tblcontacts, quotation_tblcontacts.lastname_tblcontacts "
        "FROM quotation_tblcontacts "
        "JOIN quotation_tblcompanies "
        "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
        "WHERE quotation_tblcompanies.companyname_tblcompanies like %s "
        "ORDER BY companyname_tblcompanies", [search_textmodified])

    results = cursor0.fetchall()
    transaction.commit()

    rownmbs=len(results)

    return render(request, 'quotation/ajax_search_quotation_contacts.html', {'results': results, 'rownmbs': rownmbs, 'docidinquotationjs': docidinquotationjs})
def quotationupdatecontact(request,pkdocid, pkcontactid):
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT quotation_tblcontacts.contactid_tblcontacts, quotation_tblcompanies.companyname_tblcompanies,"
        "quotation_tblcontacts.Firstname_tblcontacts, quotation_tblcontacts.lastname_tblcontacts "
        "FROM quotation_tblcontacts "
        "JOIN quotation_tblcompanies "
        "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
        "WHERE quotation_tblcontacts.contactid_tblcontacts= %s ", [pkcontactid])

    contactandcompanydata = cursor0.fetchall()
    for instancesingle in contactandcompanydata:
        companynameclone = instancesingle[1]
        firstnameclone = instancesingle[2]
        lastnameclone = instancesingle[3]

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tbldoc SET "
                    "Contactid_tblDoc_id= %s, "
                    "companyname_tblcompanies_ctbldoc=%s, "
                    "firstname_tblcontacts_ctbldoc=%s, "
                    "lastname_tblcontacts_ctbldoc=%s "
                    "WHERE Docid_tblDoc =%s ", [pkcontactid, companynameclone, firstnameclone, lastnameclone, pkdocid])

    return redirect('quotationform', pk=pkdocid)