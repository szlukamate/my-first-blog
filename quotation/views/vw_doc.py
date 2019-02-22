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
                    "WHERE obsolete_tbldoc = 0 "
                    "order by docid_tbldoc desc ")
    docs = cursor1.fetchall()
    # docs = tblDoc.objects.all()
    return render(request, 'quotation/docs.html', {'docs': docs})


def docadd(request):
    if request.method == "POST":
        dockindidfornewdoc = request.POST['dockindidfornewdoc']
        contactidfornewdoc = request.POST['contactidfornewdoc']

        creatorid=request.user.id
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
            "WHERE contactid_tblcontacts =%s", [contactidfornewdoc])
        companyandcontactdata = cursor1.fetchall()
        for instancesingle in companyandcontactdata:
            companynameclone = instancesingle[1]
            companyid = instancesingle[2] # for the lookup the default values in the tblcompanies (i.e. defaultpreface)
            firstnameclone = instancesingle[3]
            lastnameclone = instancesingle[4]
            titleclone = instancesingle[5]
            mobileclone = instancesingle[6]
            emailclone = instancesingle[7]
            pcdclone = instancesingle[8]
            townclone = instancesingle[9]
            addressclone = instancesingle[10]

        cursor5 = connection.cursor()
        cursor5.execute(
            "SELECT defaultbackpageidforquotation_tblcompanies, "
            "defaultprefaceidforquotation_tblcompanies, "
            "defaultpaymentid_tblcompanies "
            "FROM quotation_tblcompanies "
            "WHERE Companyid_tblCompanies = %s", [companyid])
        defaultsfromtblcompanies = cursor5.fetchall()
        for instancesingle in defaultsfromtblcompanies:
            defaultbackpageidforquotation = instancesingle[0]
            defaultprefaceidforquotation = instancesingle[1]
            defaultpaymentid = instancesingle[2]

        cursor6 = connection.cursor()
        cursor6.execute(
            "SELECT paymenttextforquotation_tblpayment "
            "FROM quotation_tblpayment "
            "WHERE paymentid_tblpayment = %s", [defaultpaymentid])
        paymentset = cursor6.fetchall()
        for instancesingle in paymentset:
            paymenttextcloneforquotation = instancesingle[0]

        cursor6 = connection.cursor()
        cursor6.execute(
            "SELECT backpagetextforquotation_tblbackpageforquotation "
            "FROM quotation_tblbackpageforquotation "
            "WHERE backpageidforquotation_tblbackpageforquotation = %s", [defaultbackpageidforquotation])
        backpageset = cursor6.fetchall()
        for instancesingle in backpageset:
            backpagetextcloneforquotation = instancesingle[0]

        cursor7 = connection.cursor()
        cursor7.execute(
            "SELECT prefacetextforquotation_tblprefaceforquotation "
            "FROM quotation_tblprefaceforquotation "
            "WHERE prefaceidforquotation_tblprefaceforquotation = %s", [defaultprefaceidforquotation])
        prefaceset = cursor7.fetchall()
        for instancesingle in prefaceset:
            prefacecloneforquotation = instancesingle[0]

        cursor8 = connection.cursor()
        cursor8.execute("SELECT max(docnumber_tblDoc) FROM quotation_tbldoc "
                        "WHERE Doc_kindid_tblDoc_id = %s", [dockindidfornewdoc])
        results = cursor8.fetchall()
        for x in results:
            docnumber = x[0]
            docnumber += 1

        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO quotation_tbldoc "
                        "( Doc_kindid_tblDoc_id, "
                        "Contactid_tblDoc_id,"
                        "companyname_tblcompanies_ctbldoc, "
                        "firstname_tblcontacts_ctbldoc, "
                        "lastname_tblcontacts_ctbldoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbldoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbldoc, "
                        "docnumber_tblDoc, "
                        "creatorid_tbldoc, "
                        "title_tblcontacts_ctbldoc, "
                        "mobile_tblcontacts_ctbldoc, "
                        "email_tblcontacts_ctbldoc, "
                        "pcd_tblcompanies_ctbldoc, "
                        "town_tblcompanies_ctbldoc, "
                        "address_tblcompanies_ctbldoc, "
                        "paymenttextforquotation_tblpayment_ctbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [dockindidfornewdoc, contactidfornewdoc, companynameclone, firstnameclone, lastnameclone, prefacecloneforquotation, backpagetextcloneforquotation, docnumber, creatorid,
                        titleclone,
                        mobileclone,
                        emailclone,
                        pcdclone,
                        townclone,
                        addressclone,
                        paymenttextcloneforquotation ])

        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tblDoc) FROM quotation_tbldoc")
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        cursor4 = connection.cursor()
        cursor4.execute(
            "INSERT INTO quotation_tbldoc_details ( Docid_tblDoc_details_id) VALUES (%s)",
            [maxdocid])

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
def docremove(request, pk):
    cursor1 = connection.cursor()
    cursor1.execute(
        "UPDATE quotation_tbldoc SET "
        "obsolete_tbldoc=1 "
        "WHERE docid_tbldoc =%s ", [pk])

    transaction.commit()

    return redirect('docs')
def doclink(request, docid):
    def docdata(dociddata, fieldindex):
        cursor1 = connection.cursor()
        cursor1.execute("SELECT docid_tbldoc, "
                        "companyname_tblcompanies_ctbldoc, "
                        "firstname_tblcontacts_ctbldoc, "
                        "lastname_tblcontacts_ctbldoc, "
                        "Doc_kind_name_tblDoc_kind, "
                        "pretag_tbldockind, "
                        "docnumber_tbldoc, "
                        "creationtime_tbldoc, "
                        "subject_tbldoc "
                        "FROM quotation_tbldoc "
                        "JOIN quotation_tbldoc_kind "
                        "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                        "WHERE docid_tbldoc = %s ", [dociddata])
        results = cursor1.fetchall()
        for x in results:
            result = x[fieldindex]
        return result
    #doclevel-1 start
    cursor1 = connection.cursor()
    cursor1.execute("SELECT doclinkparentid_tbldoc, docid_tbldoc "
                    "FROM quotation_tbldoc "
                    "WHERE docid_tbldoc = %s ", [docid])
    results = cursor1.fetchall()
    for x in results:
        doclevelminus1 = x[0]
#docslevel0 start
    doclevel0=docid
#docslevel1 start
    cursor1 = connection.cursor()
    cursor1.execute("SELECT doclinkparentid_tbldoc, docid_tbldoc "
                    "FROM quotation_tbldoc "
                    "WHERE doclinkparentid_tbldoc = %s ", [doclevel0])
    docstolevel1 = cursor1.fetchall()


    docslevel1 = ()
    docstolevel1withparentpointerlist = []

    docstolevel1len=len(docstolevel1)
    docslevel1widthforsvg=111 * docstolevel1len
    docstolevel1list = list(docstolevel1)
    docstolevel1withparentpointerlist = []
    for z in range(docstolevel1len): #order number to the tuple for template lines
        firstfield = docstolevel1list[z][0]
        secondfield = docstolevel1list[z][1]
        fourthfield = 90*z #rect x coordinate
        fifthfield = fourthfield + z*11 + 37 #line x coordinate roof of rect
        appendvar= (firstfield, secondfield, x, fourthfield, fifthfield)
        docstolevel1withparentpointerlist.append(appendvar)
    docstolevel1 = tuple(docstolevel1withparentpointerlist)

    docslevel1 = docslevel1 + docstolevel1




#docslevel2 start
    docscountlevel1 = len(docslevel1)


    docslevel2 = ()
    levelmembernumber=0
    docstolevel2withparentpointerlist = []
    for x in range(docscountlevel1):

        cursor2 = connection.cursor()
        cursor2.execute("SELECT doclinkparentid_tbldoc, docid_tbldoc "
                        "FROM quotation_tbldoc "
                        "WHERE doclinkparentid_tbldoc = %s ", [docslevel1[x][1]])
        docstolevel2 = cursor2.fetchall()
        docstolevel2len=len(docstolevel2)
        docstolevel2list = list(docstolevel2)
        docstolevel2withparentpointerlist = []
        for z in range(docstolevel2len): #order number to the tuple for template lines
            firstfield = docstolevel2list[z][0]
            secondfield = docstolevel2list[z][1]
            thirdfield = x
            fourthfield = 90 * levelmembernumber   # rect x coordinate
            fifthfield = fourthfield + levelmembernumber * 5 + 37  # line x coordinate roor of rect
            sixthfield = 37 + 90 * thirdfield
            levelmembernumber = levelmembernumber + 1
            appendvar = (firstfield, secondfield, thirdfield, fourthfield, fifthfield, sixthfield)
            docstolevel2withparentpointerlist.append(appendvar)
        docstolevel2 = tuple(docstolevel2withparentpointerlist)

        docslevel2 = docslevel2 + docstolevel2
        docslevel2widthforsvg = 111 * levelmembernumber
    #docslevel3 start
    docscountlevel2 = len(docslevel2)

    docslevel3 = ()
    levelmembernumber = 0
    docstolevel3withparentpointerlist = []
    for x in range(docscountlevel2):

        cursor2 = connection.cursor()
        cursor2.execute("SELECT doclinkparentid_tbldoc, docid_tbldoc "
                        "FROM quotation_tbldoc "
                        "WHERE doclinkparentid_tbldoc = %s ", [docslevel2[x][1]])
        docstolevel3 = cursor2.fetchall()
        docstolevel3len = len(docstolevel3)
        docstolevel3list = list(docstolevel3)
        docstolevel3withparentpointerlist = []
        for z in range(docstolevel3len):  # order number to the tuple for template lines
            firstfield = docstolevel3list[z][0]
            secondfield = docstolevel3list[z][1]
            thirdfield = x
            fourthfield = 200 * levelmembernumber  # rect x coordinate
            fifthfield = fourthfield + levelmembernumber * 5 + 100  # line x coordinate roor of rect
            sixthfield = 37 + 90 * thirdfield
            seventhfield = docdata(secondfield,1) #companyname
            eigthfield = docdata(secondfield, 2) #firstname
            ninethfield = docdata(secondfield, 3) #lastname
            tenthfield = docdata(secondfield, 4) #dockindname
            eleventhfield = docdata(secondfield, 5) #pretag
            twelvethfield = docdata(secondfield, 6) #docnumber
            thirteenthfield = docdata(secondfield, 7) #creationtime
            fourteenfield = docdata(secondfield, 8) #subject
            levelmembernumber = levelmembernumber + 1
            appendvar = (firstfield, secondfield, thirdfield, fourthfield, fifthfield, sixthfield, seventhfield, eigthfield, ninethfield, tenthfield, eleventhfield, twelvethfield, thirteenthfield, fourteenfield)
            docstolevel3withparentpointerlist.append(appendvar)
        docstolevel3 = tuple(docstolevel3withparentpointerlist)

        docslevel3 = docslevel3 + docstolevel3
        docslevel3widthforsvg = 222 * levelmembernumber

    #import pdb;
    #pdb.set_trace()




    return render(request, 'quotation/doclink.html', {'doclevelminus1': doclevelminus1,
                                                      'doclevel0': doclevel0,
                                                      'docslevel1': docslevel1,
                                                      'docslevel1widthforsvg': docslevel1widthforsvg,
                                                      'docslevel2': docslevel2,
                                                      'docslevel2widthforsvg': docslevel2widthforsvg,
                                                      'docslevel3': docslevel3,
                                                      'docslevel3widthforsvg': docslevel3widthforsvg})
