from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
import json
from django.http import HttpResponse
# import pdb;
# pdb.set_trace()
def products(request):
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

    cursor = connection.cursor()
    cursor.execute("SELECT Productid_tblProduct, purchase_price_tblproduct, Product_description_tblProduct, "
                   "currencyisocode_tblcurrency_ctblproduct, margin_tblproduct, round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as salesprice "
                    "FROM quotation_tblproduct ")

    products = cursor.fetchall()
    transaction.commit()

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT currencyid_tblcurrency, currencyisocode_tblcurrency FROM quotation_tblcurrency")
    currencycodes = cursor3.fetchall()
    transaction.commit()

    return render(request, 'quotation/products.html', {'products': products, 'currencycodes': currencycodes })

def productupdatecurrencyisocode(request,pkproductid, pkcurrencyid):
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT currencyisocode_tblcurrency "
        "FROM quotation_tblproduct "
        "JOIN quotation_tblcurrency "
        "ON currencyid_tblcurrency = currencyid_tblcurrency_fktblproduct "
        "WHERE currencyid_tblcurrency= %s ", [pkcurrencyid])
    currencyisocoderecords = cursor0.fetchall()
    for instancesingle in currencyisocoderecords:
        currencyisocodeforrow= instancesingle[0]

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tblproduct SET "
                    "currencyisocode_tblcurrency_ctblproduct= %s "
                    "WHERE productid_tblproduct =%s ", [currencyisocodeforrow, pkproductid])

    return redirect('products')


def productsalespricefieldupdate(request):
    if request.method == 'POST':
        marginrequired = request.POST['marginrequired']
        productidinproductjs = request.POST['productidinproductjs']

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tblproduct SET "
                    "margin_tblproduct= %s "
                    "WHERE productid_tblproduct =%s ", [marginrequired, productidinproductjs])

    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT purchase_price_tblproduct, margin_tblproduct, round((100*purchase_price_tblproduct)/(100-margin_tblproduct),2) as salesprice "
        "FROM quotation_tblproduct "
        "WHERE productid_tblproduct= %s ", [productidinproductjs])
    results = cursor0.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
