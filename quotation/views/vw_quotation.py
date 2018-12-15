from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
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
    # import pdb;
    # pdb.set_trace()

    #        doc = get_object_or_404(tblDoc,pk=pk)

    # To determine Companyid to pass it to template to goto
    # companyid_tblcontacts
    for x in doc:
        contactid = x[1]
    cursor4 = connection.cursor()
    cursor4.execute("SELECT companyid_tblcontacts_id "
                    "FROM quotation_tblcontacts "
                    "WHERE Contactid_tblContacts=%s ", [contactid])
    companyid = cursor4.fetchall()

    cursor3 = connection.cursor()
    cursor3.execute("SELECT  * "
                    "FROM quotation_tbldoc_details "
                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [pk])
    docdetails = cursor3.fetchall()

    return render(request, 'quotation/quotation.html', {'doc': doc, 'docdetails': docdetails, 'companyid': companyid})


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


def quotationnewrow(request, pk):
    cursor1 = connection.cursor()
    cursor1.execute(
        "INSERT INTO quotation_tbldoc_details (Docid_tblDoc_details_id, Productid_tblDoc_details_id,Qty_tblDoc_details,firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details,Note_tblDoc_details) VALUES (%s, 1,1, 1,0,0,0,'Defaultnote')",
        [pk])
    transaction.commit()

    return redirect('quotationform', pk=pk)


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