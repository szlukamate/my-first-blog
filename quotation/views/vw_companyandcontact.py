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


        cursor0 = connection.cursor()
        cursor0.execute(
            "SELECT companyid_tblcompanies, "
            "companyname_tblcompanies, "
            "defaultprefaceidforquotation_tblcompanies, "
            "defaultbackpageidforquotation_tblcompanies, "
            "pcd_tblcompanies, "
            "town_tblcompanies, "
            "address_tblcompanies "
            "FROM quotation_tblcompanies "
            "WHERE companyid_tblcompanies=%s ",
            [pk])
        particularcompany = cursor0.fetchall()
        for instancesingle in particularcompany:
            selecteddefaultprefaceidforquotation = instancesingle[2]
            selecteddefaultbackpageidforquotation = instancesingle[3]

        # default staff
        # tblprefaceforquotation staff
        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT "
            "prefaceidforquotation_tblprefaceforquotation, "
            "prefacenameforquotation_tblprefaceforquotation "
            "FROM quotation_tblprefaceforquotation "
            "WHERE prefaceidforquotation_tblprefaceforquotation=%s ",
            [selecteddefaultprefaceidforquotation])
        selecteddefaultprefaceforquotationset = cursor3.fetchall()
        for instancesingle in selecteddefaultprefaceforquotationset:
            selecteddefaultprefacenameforquotation = instancesingle[1]

        cursor2 = connection.cursor()
        cursor2.execute(
            "SELECT "
            "prefaceidforquotation_tblprefaceforquotation, "
            "prefacenameforquotation_tblprefaceforquotation "
            "FROM quotation_tblprefaceforquotation")
        defaultprefacechoicesforquotation = cursor2.fetchall()

        #tblbackpageforquotation staff
        cursor3 = connection.cursor()
        cursor3.execute(
            "SELECT "
            "backpageidforquotation_tblbackpageforquotation, "
            "backpagenameforquotation_tblbackpageforquotation "
            "FROM quotation_tblbackpageforquotation "
            "WHERE backpageidforquotation_tblbackpageforquotation=%s ",
            [selecteddefaultbackpageidforquotation])
        selecteddefaultbackpageforquotationset = cursor3.fetchall()
        for instancesingle in selecteddefaultbackpageforquotationset:
            selecteddefaultbackpagenameforquotation = instancesingle[1]

        cursor2 = connection.cursor()
        cursor2.execute(
            "SELECT "
            "backpageidforquotation_tblbackpageforquotation, "
            "backpagenameforquotation_tblbackpageforquotation "
            "FROM quotation_tblbackpageforquotation")
        defaultbackpagechoicesforquotation = cursor2.fetchall()
        # default staff end

        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT contactid_tblcontacts, "
            "firstname_tblcontacts, "
            "lastname_tblcontacts, "
            "title_tblcontacts, "
            "mobile_tblcontacts, "
            "email_tblcontacts "
            "FROM quotation_tblcontacts "
            "WHERE companyid_tblcontacts_id=%s ",
            [pk])
        contacts = cursor1.fetchall()

        return render(request, 'quotation/companyedit.html', {'particularcompany': particularcompany,
                                                              'contacts': contacts,
                                                              'defaultprefacechoicesforquotation': defaultprefacechoicesforquotation,
                                                              'selecteddefaultprefacenameforquotation': selecteddefaultprefacenameforquotation,
                                                              'defaultbackpagechoicesforquotation': defaultbackpagechoicesforquotation,
                                                              'selecteddefaultbackpagenameforquotation': selecteddefaultbackpagenameforquotation})
def companyuniversalselections (request):

    fieldvalue = request.POST['fieldvalue']
    companyid = request.POST['companyid']
    fieldnamefromname = request.POST['fieldnamefromname'] # i.e. prefecetextforquotation_tblprefaceforquotation
    fieldnamefromid = request.POST['fieldnamefromid'] # i.e. prefeceidforquotation_tblprefaceidforquotation
    tablenamefrom = request.POST['tablenamefrom'] #i.e. tblprefaceforquotation or tblbackpageforquotation
    fieldnameto = request.POST['fieldnameto'] # i.e. defaultprefaceidforquotation_tblcompanies


    cursor2 = connection.cursor()
    #import pdb;
    #pdb.set_trace()

    cursor2.execute("UPDATE quotation_tblcompanies SET "
                    "" + fieldnameto + "= %s "
                    "WHERE companyid_tblcompanies =%s ", [fieldvalue, companyid])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT " + fieldnameto + " "
        "FROM quotation_tblcompanies "
        "WHERE companyid_tblcompanies= %s ", [companyid])
    results0 = cursor3.fetchall()
    for instancesingle in results0:
        fieldvaluefromsqlverified= instancesingle[0]

    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT " + fieldnamefromname + " "
        "FROM " + tablenamefrom + " "
        "WHERE " + fieldnamefromid + "= %s ", [fieldvaluefromsqlverified])
    results = cursor0.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
