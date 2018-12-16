from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
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

    cursor = connection.cursor()
    cursor.execute("SELECT Productid_tblProduct, Product_price_tblProduct, Product_description_tblProduct, currencyisocode_tblcurrency, currencyid_tblcurrency "
                    "FROM quotation_tblproduct "
                    "JOIN quotation_tblcurrency "
                    "ON quotation_tblproduct.currencyid_tblcurrency_fktblproduct = quotation_tblcurrency.currencyid_tblcurrency ")

    products = cursor.fetchall()
    transaction.commit()

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT currencyid_tblcurrency, currencyisocode_tblcurrency FROM quotation_tblcurrency")
    currencycodes = cursor3.fetchall()
    transaction.commit()

    return render(request, 'quotation/products.html', {'products': products, 'currencycodes': currencycodes })
