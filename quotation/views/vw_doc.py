from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
# import pdb;
# pdb.set_trace()

def docs(request):
    cursor1 = connection.cursor()
    cursor1.execute("SELECT docid_tbldoc, Pcd_tblDoc, Town_tblDoc, Doc_kindid_tblDoc_id, companyname_tblcompanies_ctbldoc, firstname_tblcontacts_ctbldoc, lastname_tblcontacts_ctbldoc, creationtime_tbldoc "
                    "FROM quotation_tbldoc "
                    "order by docid_tbldoc desc")
    docs = cursor1.fetchall()
    # docs = tblDoc.objects.all()
    return render(request, 'quotation/docs.html', {'docs': docs})


def docadd(request):
    if request.method == "POST":
        dockindidfornewdoc = request.POST['dockindidfornewdoc']
        contactidfornewdoc = request.POST['contactidfornewdoc']
        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO quotation_tbldoc ( Doc_kindid_tblDoc_id, Contactid_tblDoc_id) VALUES (%s,%s)",
                        [dockindidfornewdoc, contactidfornewdoc])

        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc")
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        return redirect('docselector', pk=maxdocid)
    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT quotation_tblcontacts.contactid_tblcontacts, quotation_tblcompanies.companyname_tblcompanies,"
        "quotation_tblcontacts.Firstname_tblcontacts, quotation_tblcontacts.lastname_tblcontacts "
        "FROM quotation_tblcontacts "
        "JOIN quotation_tblcompanies "
        "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
        "ORDER BY companyname_tblcompanies")
    contacts = cursor0.fetchall()
    transaction.commit()
    # import pdb;
    # pdb.set_trace()
    cursor = connection.cursor()
    cursor.execute("SELECT doc_kindid_tbldoc_kind, doc_kind_name_tbldoc_kind FROM quotation_tbldoc_kind")
    dockinds = cursor.fetchall()
    transaction.commit()
    return render(request, 'quotation/docadd.html', {'dockinds': dockinds, 'contacts': contacts})


def docselector(request, pk):
    cursor = connection.cursor()
    cursor.execute("SELECT  quotation_tbldoc_kind.Doc_kindid_tbldoc_kind "
                   "FROM quotation_tbldoc "
                   "JOIN quotation_tbldoc_kind "
                   "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                   "WHERE quotation_tbldoc.docid_tbldoc=%s ", [pk])
    results = cursor.fetchall()
    for x in results:
        dockind = x[0]
    transaction.commit()
    if dockind == 1:  # Quotation
        return redirect('quotationform', pk=pk)
    elif dockind == 2:  # Order
        return redirect('orderform', pk=pk)
