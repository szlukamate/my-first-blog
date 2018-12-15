from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
# import pdb;
# pdb.set_trace()
def companies(request):

    cursor = connection.cursor()
    cursor.execute("SELECT Companyid_tblCompanies, companyname_tblcompanies FROM quotation_tblcompanies")
    companies = cursor.fetchall()
    transaction.commit()
    return render(request, 'quotation/companies.html', {'companies': companies})

def companynew(request):

    cursor1 = connection.cursor()
    cursor1.execute("INSERT INTO quotation_tblcompanies (companyname_tblcompanies) VALUES ('DefaultCompany')")
    transaction.commit()

    return redirect('companies')

def companyremove(request,pk):
    cursor1 = connection.cursor()
    cursor1.execute(
        "DELETE FROM quotation_tblcompanies WHERE companyid_tblcompanies=%s ", [pk])
    transaction.commit()

    return redirect('companies')

def companyedit(request, pk):



                if request.method == "POST":
                    companyname = request.POST['companyname']
                    cursor2 = connection.cursor()
                    cursor2.execute(
                        "UPDATE quotation_tblcompanies "
                        "SET companyname_tblcompanies = %s "
                        "WHERE companyid_tblcompanies = %s", [companyname, pk])

                    #else:
                cursor0 = connection.cursor()
                cursor0.execute(
                    "SELECT companyid_tblcompanies, companyname_tblcompanies FROM quotation_tblcompanies WHERE companyid_tblcompanies=%s ",
                    [pk])
                particularcompany = cursor0.fetchall()


                cursor1 = connection.cursor()
                cursor1.execute(
                    "SELECT contactid_tblcontacts, firstname_tblcontacts, lastname_tblcontacts FROM quotation_tblcontacts WHERE companyid_tblcontacts_id=%s ",
                    [pk])
                contacts = cursor1.fetchall()
                #    form = quotationroweditForm(instance=quotationrow)

                return render(request, 'quotation/companyedit.html', {'particularcompany': particularcompany, 'contacts': contacts })
