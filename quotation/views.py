from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from .forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
# import pdb;
# pdb.set_trace()

def welcome(request):
        return render(request, 'quotation/welcome.html', {})

def docs(request):
<<<<<<< HEAD
        cursor1 = connection.cursor()
        cursor1.execute("SELECT docid_tbldoc, Pcd_tblDoc, Town_tblDoc, Doc_kindid_tblDoc_id "
                        "FROM quotation_tbldoc "
                        "order by docid_tbldoc desc")
        docs = cursor1.fetchall()
        #docs = tblDoc.objects.all()
        return render(request, 'quotation/docs.html', {'docs': docs})

def companies(request):

=======
        docs = tblDoc.objects.all()
        return render(request, 'quotation/docs.html', {'docs': docs})

def companies(request):

>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
    cursor = connection.cursor()
    cursor.execute("SELECT Companyid_tblCompanies, companyname_tblcompanies FROM quotation_tblcompanies")
    companies = cursor.fetchall()
    transaction.commit()
    return render(request, 'quotation/companies.html', {'companies': companies})

def docadd(request):
    if request.method == "POST":
        dockindidfornewdoc = request.POST['dockindidfornewdoc']
        contactidfornewdoc = request.POST['contactidfornewdoc']
        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO quotation_tbldoc ( Doc_kindid_tblDoc_id, Contactid_tblDoc_id) VALUES (%s,%s)", [dockindidfornewdoc, contactidfornewdoc])

        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc")
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        return redirect('docselector', pk=maxdocid)
    cursor0 = connection.cursor()
    cursor0.execute("SELECT quotation_tblcontacts.contactid_tblcontacts, quotation_tblcompanies.companyname_tblcompanies,"
                    "quotation_tblcontacts.Firstname_tblcontacts, quotation_tblcontacts.lastname_tblcontacts "
                    "FROM quotation_tblcontacts "
                    "JOIN quotation_tblcompanies "
                    "ON quotation_tblcompanies.companyid_tblcompanies = quotation_tblcontacts.companyid_tblcontacts_id "
                    "ORDER BY companyname_tblcompanies")
    contacts = cursor0.fetchall()
    transaction.commit()
    #import pdb;
    #pdb.set_trace()
    cursor = connection.cursor()
    cursor.execute("SELECT doc_kindid_tbldoc_kind, doc_kind_name_tbldoc_kind FROM quotation_tbldoc_kind")
    dockinds = cursor.fetchall()
    transaction.commit()
    return render(request, 'quotation/docadd.html', {'dockinds': dockinds, 'contacts': contacts})

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
        if dockind==1: #Quotation
            return redirect('quotationform', pk=pk)
        elif dockind==2: #Order
            return redirect('orderform', pk=pk)

def quotationform(request,pk):
        if request.method == "POST":
                fieldvalue = request.POST['fieldvalue']
                rowid = request.POST['rowid']
                fieldname = request.POST['fieldname']

                cursor2 = connection.cursor()
                sqlquery="UPDATE quotation_tbldoc_details SET " + fieldname + "= '" + fieldvalue + "' WHERE Doc_detailsid_tblDoc_details =" + rowid
                #import pdb;
                #pdb.set_trace()
                cursor2.execute(sqlquery)
<<<<<<< HEAD

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
        #import pdb;
        #pdb.set_trace()

        #        doc = get_object_or_404(tblDoc,pk=pk)

        # To determine Companyid to pass it to template to goto
        #companyid_tblcontacts
        for x in doc:
            contactid=x[1]
        cursor4 = connection.cursor()
        cursor4.execute("SELECT companyid_tblcontacts_id "
                        "FROM quotation_tblcontacts "
                        "WHERE Contactid_tblContacts=%s ",[contactid])
        companyid = cursor4.fetchall()

        cursor3 = connection.cursor()
        cursor3.execute("SELECT  * "
                       "FROM quotation_tbldoc_details "
                       "WHERE docid_tbldoc_details_id=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details", [pk])
        docdetails = cursor3.fetchall()


        return render(request, 'quotation/quotation.html', {'doc':doc, 'docdetails':docdetails, 'companyid':companyid})
=======
        doc = get_object_or_404(tblDoc,pk=pk)
        cursor3 = connection.cursor()
        cursor3.execute("SELECT  * "
                       "FROM quotation_tbldoc_details "
                       "WHERE docid_tbldoc_details_id=%s "
                        "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details", [pk])
        docdetails = cursor3.fetchall()


        return render(request, 'quotation/quotation.html', {'doc':doc, 'docdetails':docdetails})
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
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
        cursor1.execute("INSERT INTO quotation_tbldoc_details (Docid_tblDoc_details_id, Productid_tblDoc_details_id,Qty_tblDoc_details,firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details,Note_tblDoc_details) VALUES (%s, 1,1, 1,0,0,0,'Defaultnote')",[pk])
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


def orderform(request,pk):
    if request.method == "POST":
        firstnum_tblDoc_details = request.POST['firstnum_tblDoc_details']
        Doc_detailsid_tblDoc_details = request.POST['Doc_detailsid_tblDoc_details']
        cursor2 = connection.cursor()
        cursor2.execute(
            "UPDATE quotation_tbldoc_details "
            "SET firstnum_tblDoc_details = %s "
            "WHERE  Doc_detailsid_tblDoc_details = %s", [firstnum_tblDoc_details, Doc_detailsid_tblDoc_details])
        # import pdb;
        # pdb.set_trace()

    doc = get_object_or_404(tblDoc, pk=pk)
    cursor3 = connection.cursor()
    cursor3.execute("SELECT  * "
                    "FROM quotation_tbldoc_details "
                    "WHERE docid_tbldoc_details_id=%s "
                    "order by firstnum_tblDoc_details,secondnum_tblDoc_details,thirdnum_tblDoc_details,fourthnum_tblDoc_details",
                    [pk])

    docdetails = cursor3.fetchall()

    return render(request, 'quotation/order.html', {'doc': doc, 'docdetails': docdetails})
def searchquotationcontacts(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
<<<<<<< HEAD
        docidinquotationjs = request.POST['docidinquotationjs']
=======
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
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

<<<<<<< HEAD
    return render(request, 'quotation/ajax_search_quotation_contacts.html', {'results': results, 'rownmbs': rownmbs, 'docidinquotationjs': docidinquotationjs})
=======
    return render(request, 'quotation/ajax_search_quotation_contacts.html', {'results': results, 'rownmbs': rownmbs})
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
def products(request):
    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        fieldname = request.POST['fieldname']

        cursor2 = connection.cursor()
        sqlquery = "UPDATE quotation_tblproduct SET " + fieldname + "= '"  + fieldvalue + "' WHERE productid_tblproduct =" + rowid
        cursor2.execute(sqlquery)

    cursor = connection.cursor()
    cursor.execute("SELECT Productid_tblProduct, Product_price_tblProduct, Product_description_tblProduct FROM quotation_tblproduct")
    products = cursor.fetchall()
    transaction.commit()
<<<<<<< HEAD
    return render(request, 'quotation/products.html', {'products': products})
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
=======
    return render(request, 'quotation/products.html', {'products': products})
>>>>>>> aab59635ca3ec79857281d64a90704dcd3b4576f
