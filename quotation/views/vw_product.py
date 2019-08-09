from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
import simplejson as json
from django.http import HttpResponse
# import pdb;
# pdb.set_trace()
@login_required
def products(request, pkproductid):
    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        fieldname = request.POST['fieldname']
        #import pdb;
        #pdb.set_trace()
        cursor2 = connection.cursor()
        sqlquery = "UPDATE quotation_tblproduct SET " + fieldname + "= '"  + fieldvalue + "' WHERE productid_tblproduct =" + rowid
        cursor2.execute(sqlquery)

        cursor3 = connection.cursor()
        cursor3.execute("SELECT " + fieldname + " "
                       "FROM quotation_tblproduct "
                        "WHERE productid_tblproduct= %s ", [rowid])
        results = cursor3.fetchall()

        json_data = json.dumps(results)

        return HttpResponse(json_data, content_type="application/json")
    # pkproductid == 0 if the request not asks a particular product
    if int(pkproductid) == 0:
        cursor = connection.cursor()
        cursor.execute("SELECT Productid_tblProduct, "
                       "purchase_price_tblproduct, "
                       "customerdescription_tblProduct, "
                       "currencyisocode_tblcurrency_ctblproduct, "
                       "margin_tblproduct, "
                       "round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as listprice, "
                       "unit_tblproduct, "
                       "suppliercompanyid_tblproduct, "
                       "companyname_tblcompanies, "
                       "supplierdescription_tblProduct, "
                       "discreteflag_tblproduct, " #10
                       "serviceflag_tblproduct "

                       "FROM quotation_tblproduct "
                       "JOIN quotation_tblcompanies "
                       "ON companyid_tblcompanies = suppliercompanyid_tblproduct "
                       "WHERE obsolete_tblproduct=0 "
                       "order by productid_tblproduct"

                       )
        products = cursor.fetchall()
        transaction.commit()


    else:
        cursor = connection.cursor()
        cursor.execute("SELECT Productid_tblProduct, "
                       "purchase_price_tblproduct, "
                       "customerdescription_tblProduct, "
                       "currencyisocode_tblcurrency_ctblproduct, "
                       "margin_tblproduct, "
                       "round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as listprice, "
                       "unit_tblproduct, "
                       "suppliercompanyid_tblproduct, "
                       "companyname_tblcompanies, "
                       "supplierdescription_tblProduct "
                       "FROM quotation_tblproduct "
                       "JOIN quotation_tblcompanies "
                       "ON companyid_tblcompanies = suppliercompanyid_tblproduct "
                       "WHERE productid_tblproduct= %s and obsolete_tblproduct=0 "
                       "order by productid_tblproduct", [pkproductid])

        products = cursor.fetchall()
        transaction.commit()

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT currencyid_tblcurrency, currencyisocode_tblcurrency FROM quotation_tblcurrency")
    currencycodes = cursor3.fetchall()
    transaction.commit()

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT companyid_tblcompanies, companyname_tblcompanies FROM quotation_tblcompanies")
    supplierlist = cursor3.fetchall()
    transaction.commit()


    return render(request, 'quotation/products.html', {'products': products,
                                                       'currencycodes': currencycodes,
                                                       'supplierlist': supplierlist})
@login_required
def productupdatecurrencyisocode(request):
    if request.method == 'POST':
        productidinjs = request.POST['productidinjs']
        currencyidinjs = request.POST['currencyidinjs']

    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT currencyisocode_tblcurrency "
        "FROM quotation_tblproduct "
        "JOIN quotation_tblcurrency "
        "ON currencyid_tblcurrency = currencyid_tblcurrency_fktblproduct "
        "WHERE currencyid_tblcurrency= %s ", [currencyidinjs])
    currencyisocoderecords = cursor0.fetchall()
    for instancesingle in currencyisocoderecords:
        currencyisocodeforrow= instancesingle[0]

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tblproduct SET "
                    "currencyisocode_tblcurrency_ctblproduct= %s "
                    "WHERE productid_tblproduct =%s ", [currencyisocodeforrow, productidinjs])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT currencyisocode_tblcurrency_ctblproduct "
        "FROM quotation_tblproduct "
        "WHERE productid_tblproduct= %s ", [productidinjs])
    results = cursor3.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")

@login_required
def productlistpricefieldupdate(request):
    if request.method == 'POST':
        postselector = request.POST['postselector']
        productidinproductjs = request.POST['productidinproductjs']

        if postselector=='listpriceupdaterequestwithpassingmarginrequired':

            marginrequired = request.POST['marginrequired']

            cursor2 = connection.cursor()
            cursor2.execute("UPDATE quotation_tblproduct SET "
                            "margin_tblproduct= %s "
                            "WHERE productid_tblproduct =%s ", [marginrequired, productidinproductjs])

        elif postselector=='listpriceupdaterequestonly':
            pass
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT purchase_price_tblproduct, margin_tblproduct, round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as listprice "
        "FROM quotation_tblproduct "
        "WHERE productid_tblproduct= %s ", [productidinproductjs])
    results = cursor0.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def productnew(request):
    serviceflag = request.POST['serviceflag']
    discreteflag = request.POST['discreteflag']

    cursor1 = connection.cursor()
    cursor1.execute("INSERT INTO quotation_tblproduct "
                    "(customerdescription_tblproduct, "
                    "serviceflag_tblproduct, "
                    "discreteflag_tblproduct, "
                    "suppliercompanyid_tblproduct) VALUES ('DefaultDescription', '" + serviceflag + "', '" + discreteflag + "', '1')")
    transaction.commit()

    return render(request, 'quotation/productnewredirecturl.html', {})
@login_required
def productremove(request,pkproductid):
    cursor1 = connection.cursor()
    cursor1.execute(
                        "UPDATE quotation_tblproduct SET "
                        "obsolete_tblproduct=1 "
                        "WHERE productid_tblproduct =%s ", [pkproductid])

    transaction.commit()

    return redirect('products', pkproductid=0)
@login_required
def productupdatesupplier(request):
    if request.method == 'POST':
        productidinjs = request.POST['productidinjs']
        supplieridinjs = request.POST['supplieridinjs']

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tblproduct SET "
                    "suppliercompanyid_tblproduct= %s "
                    "WHERE productid_tblproduct =%s ", [supplieridinjs, productidinjs])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT companyname_tblcompanies "
        "FROM quotation_tblcompanies "
        "WHERE companyid_tblcompanies= %s ", [supplieridinjs])
    results = cursor3.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
