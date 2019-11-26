from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from datetime import datetime, timedelta

## import pdb;
# pdb.set_trace()
@login_required
def docs(request):
    cursor1 = connection.cursor()
    cursor1.execute("SELECT docid_tbldoc, Pcd_tblDoc, Town_tblDoc, "
                    "Doc_kindid_tblDoc_id, "
                    "companyname_tblcompanies_ctbldoc, "
                    "firstname_tblcontacts_ctbldoc, "
                    "lastname_tblcontacts_ctbldoc, "
                    "creationtime_tbldoc,"
                    "Doc_kind_name_tblDoc_kind, "
                    "pretag_tbldockind,"
                    "docnumber_tbldoc "
                    "FROM quotation_tbldoc "
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                    "WHERE obsolete_tbldoc = 0 "
                    "order by docid_tbldoc desc ")
    docs = cursor1.fetchall()
    return render(request, 'quotation/docs.html', {'docs': docs})
def group_required(group_name, login_url=None):
    """
    Decorator for views that checks whether a user belongs to a particular
    group, redirecting to the log-in page if necessary.
    """
    def check_group(user):
        # First check if the user belongs to the group
        if user.groups.filter(name=group_name).exists():
            return True
    return user_passes_test(check_group, login_url=login_url)

@group_required("manager")
@login_required
def docsearch(request):
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "companyname_tblcompanies_ctbldoc "
                    "FROM quotation_tbldoc "
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                    "WHERE obsolete_tbldoc = 0 "
                    "GROUP BY companyname_tblcompanies_ctbldoc ")
    companies = cursor1.fetchall()

    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Doc_kind_name_tblDoc_kind "
                    "FROM quotation_tbldoc "
                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "
                    "WHERE obsolete_tbldoc = 0 "
                    "GROUP BY Doc_kind_name_tblDoc_kind ")
    dockindnames = cursor1.fetchall()

    #   fromdate = datetime.today() - timedelta(365)
    #todate = datetime.today()


    return render(request, 'quotation/docsearch.html', {'companies': companies,
                                                        'dockindnames':dockindnames})
@login_required
def docsearchcontent(request):
    docnumber = request.POST['docnumber']
    dockindname = request.POST['dockindname']
    fromdate = request.POST['fromdate']
    todate = request.POST['todate']
    company = request.POST['company']

    if docnumber != '':
        docnumberformainresults = "and D1.docnumber_tbldoc='" + docnumber + "' "
    else:
        docnumberformainresults = ""
        docnumberforrowsources = ""

    if dockindname != '':
        dockindnameformainresults = "and Doc_kind_name_tblDoc_kind='" + dockindname + "' "
        dockindnameforrowsources = "and Doc_kind_name_tblDoc_kind='" + dockindname + "' "
    else:
        dockindnameformainresults = ""
        dockindnameforrowsources = ""

    #datephrase = "and creationtime_tbldoc BETWEEN '" + fromdate + "' and '" + todate + "' "
#    datephrase = "and DATE(quotation_tbldoc.creationtime_tbldoc) >= '" + fromdate + "' and DATE('D.creationtime_tbldoc') <= '" + todate + "' "
#    datephrase = "and D.creationtime_tbldoc >= '" + fromdate + "' and D.creationtime_tbldoc <= '" + todate + "' "
    #datephrase = "and DATE(creationtime_tbldoc) = '2019-04-19'"
    datephraseformainresults = ''
    datephraseforrowsources = ''
    if company != '':
        companyformainresults = "and companyname_tblcompanies_ctbldoc='" + company + "'"
        companyforrowsources = "and companyname_tblcompanies_ctbldoc='" + company + "'"
    else:
        companyformainresults = ""
        companyforrowsources = ""

    #import pdb;
    #pdb.set_trace()
    searchphraseformainresults = docnumberformainresults + dockindnameformainresults + datephraseformainresults + companyformainresults + " "
    searchphraseforrowsources = dockindnameforrowsources + companyforrowsources + " "

    cursor1 = connection.cursor()
    #import pdb;
    #pdb.set_trace()

    cursor1.execute("SELECT D1.docid_tbldoc, "
                    "D1.pcd_tblcompanies_ctbldoc, "
                    "D1.town_tblcompanies_ctbldoc, "
                    "D1.Doc_kindid_tblDoc_id, "
                    "D1.companyname_tblcompanies_ctbldoc, "
                    "D1.firstname_tblcontacts_ctbldoc, "
                    "D1.lastname_tblcontacts_ctbldoc, "
                    "D1.creationtime_tbldoc, "
                    "Doc_kind_name_tblDoc_kind, "
                    "pretag_tbldockind, "
                    "D1.docnumber_tbldoc, " #10
                    "Doc_kindid_tblDoc_kind, "
                    "D1.subject_tbldoc, "
                    "D1.wherefromdocid_tbldoc, "
                    "D1.wheretodocid_tbldoc, "
                    "Dfrom.fromcompanyname, "
                    "Dto.tocompanyname, "
                    "D1.obsolete_tbldoc, "
                    "Dfrom.frompretag, "
                    "Dfrom.fromdocnumber, "
                    "Dto.topretag, " #20
                    "Dto.todocnumber, "
                    "D1.stocktakingdeno_tbldoc, "
                    "D1.denoenabledflag_tbldoc, "
                    "D1.machinemadedocflag_tbldoc "
                   
                    "FROM quotation_tbldoc as D1 "

                    "JOIN quotation_tbldoc_kind "
                    "ON D1.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                    "LEFT JOIN (SELECT companyname_tblcompanies_ctbldoc as fromcompanyname, "
                    "                   docid_tbldoc as fromdocid, "
                    "                   pretag_tbldockind as frompretag, "
                    "                   docnumber_tbldoc as fromdocnumber "
                    
                    "                   FROM quotation_tbldoc "

                    "                   JOIN quotation_tbldoc_kind "
                    "                   ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                    "           ) as Dfrom "
                    "ON D1.wherefromdocid_tbldoc = Dfrom.fromdocid "

                    "LEFT JOIN (SELECT companyname_tblcompanies_ctbldoc as tocompanyname, "
                    "                   docid_tbldoc as todocid, "
                    "                   pretag_tbldockind as topretag, "
                    "                   docnumber_tbldoc as todocnumber "
                    
                    "                   FROM quotation_tbldoc "

                    "                   JOIN quotation_tbldoc_kind "
                    "                   ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                    "           ) as Dto "
                    "ON D1.wheretodocid_tbldoc = Dto.todocid "

                    "HAVING D1.obsolete_tbldoc = 0 " + searchphraseformainresults + ""
                    "order by D1.docid_tbldoc desc ")
    docs = cursor1.fetchall()
    #import pdb;
    #pdb.set_trace()

    cursor2 = connection.cursor()
    cursor2.execute("SELECT "
                    "companyname_tblcompanies_ctbldoc "

                    "FROM quotation_tbldoc "

                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                    "WHERE quotation_tbldoc.obsolete_tbldoc = 0 " + searchphraseforrowsources + ""
                    "GROUP BY companyname_tblcompanies_ctbldoc ")

    companiesrowsources = cursor2.fetchall()
    cursor1 = connection.cursor()
    cursor1.execute("SELECT "
                    "Doc_kind_name_tblDoc_kind "

                    "FROM quotation_tbldoc "

                    "JOIN quotation_tbldoc_kind "
                    "ON quotation_tbldoc.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                    "WHERE quotation_tbldoc.obsolete_tbldoc = 0 " + searchphraseforrowsources + ""
                    "GROUP BY Doc_kind_name_tblDoc_kind ")

    dockindrowsources = cursor1.fetchall()
    return render(request, 'quotation/docsearchcontent.html', {'docs': docs,
                                                               'companiesrowsources': companiesrowsources,
                                                               'dockindrowsources': dockindrowsources})

@login_required
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

        cursor7 = connection.cursor()
        cursor7.execute(
            "SELECT currencyisocode_tblcurrency "
            "FROM quotation_tblcurrency "
            "WHERE accountcurrency_tblcurrency = 1")
        results = cursor7.fetchall()
        for instancesingle in results:
            accountcurrencycodeclone = instancesingle[0]


        cursor8 = connection.cursor()
        cursor8.execute("SELECT max(docnumber_tblDoc) FROM quotation_tbldoc "
                        "WHERE Doc_kindid_tblDoc_id = %s", [dockindidfornewdoc])
        results = cursor8.fetchall()
        resultslen = len(results)
        #import pdb;
        #pdb.set_trace()

        if results[0][0] is not None: # only if there is not doc yet (this would be the first instance)
            for x in results:
                docnumber = x[0]
                docnumber += 1
        else:
                docnumber = 80 # arbitrary number

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
                        "paymenttextforquotation_tblpayment_ctbldoc, "
                        "accountcurrencycode_tbldoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [dockindidfornewdoc, contactidfornewdoc, companynameclone, firstnameclone, lastnameclone, prefacecloneforquotation, backpagetextcloneforquotation, docnumber, creatorid,
                        titleclone,
                        mobileclone,
                        emailclone,
                        pcdclone,
                        townclone,
                        addressclone,
                        paymenttextcloneforquotation,
                        accountcurrencycodeclone])

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

    cursor = connection.cursor()
    cursor.execute("SELECT doc_kindid_tbldoc_kind, doc_kind_name_tbldoc_kind FROM quotation_tbldoc_kind")
    dockinds = cursor.fetchall()
    transaction.commit()

    return render(request, 'quotation/docadd.html', {'dockinds': dockinds, 'contacts': contacts})

@login_required
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

    if dockind == 1:  # Quotation
        return redirect('quotationform', pk=pk)
    elif dockind == 2:  # CustomerOrder
        return redirect('customerorderform', pk=pk)
    elif dockind == 3:  # CustomerInvoice
        return redirect('customerinvoiceform', pk=pk)
    elif dockind == 4:  # Job Number
        return redirect('jobnumberform', pk=pk)
    elif dockind == 5:  # Email
        return redirect('emailform', pk=pk)
    elif dockind == 6:  # Accounting Entry
        return redirect('accountentryform', pk=pk)
    elif dockind == 7:  # Supplier Order
        return redirect('purchaseorderform', pk=pk)
    elif dockind == 8:  # Delivery Note
        return redirect('deliverynoteform', pk=pk)

@login_required
def docremove(request, pk):
    cursor1 = connection.cursor()
    cursor1.execute(
        "UPDATE quotation_tbldoc SET "
        "obsolete_tbldoc=1 "
        "WHERE docid_tbldoc =%s ", [pk])

    transaction.commit()

    return redirect('docsearch')
@login_required
def doclink(request, docid):
    fixstate = request.session.get('fixstate','0')

    #onfix='1'
    if fixstate == '1':
        docid2 = request.session.get('fixtothis', '0')
    else:
        docid2=docid

    def docstolevel(firstfieldpass, secondfieldpass, thirdfieldpass, levelmembernumberpass, appendablelist):
        levelmembernumber = levelmembernumberpass
        firstfield = firstfieldpass
        secondfield = secondfieldpass  # docid
        thirdfield = thirdfieldpass
        fourthfield = 200 * levelmembernumber  # rect x coordinate
        fifthfield = fourthfield + levelmembernumber * 11 + 88  # line x coordinate lower point
        sixthfield = 88 + 197 * thirdfield  # line x coordinate upper point
        seventhfield = docdata(secondfield, 1)  # companyname
        eigthfield = docdata(secondfield, 2)  # firstname
        ninethfield = docdata(secondfield, 3)  # lastname
        tenthfield = docdata(secondfield, 4)  # dockindname
        eleventhfield = docdata(secondfield, 5)  # pretag
        twelvethfield = docdata(secondfield, 6)  # docnumber
        thirteenthfield = docdata(secondfield, 7)  # creationtime
        fourteenthfield = docdata(secondfield, 8)  # subject
        fifteenthfield = fourthfield + 5 # text x coordinate
        sixteenthfield = docdata(secondfield, 10) # na text
        seventeenthfield = docdata(secondfield, 11) # na text

        levelmembernumber = levelmembernumber + 1
        appendvar = (
            firstfield, secondfield, thirdfield, fourthfield, fifthfield, sixthfield, seventhfield, eigthfield,
            ninethfield,
            tenthfield, eleventhfield, twelvethfield, thirteenthfield, fourteenthfield, fifteenthfield, sixteenthfield, seventeenthfield)
        docstolevelwithparentpointerlist = appendablelist
        docstolevelwithparentpointerlist.append(appendvar)

        return docstolevelwithparentpointerlist

    def docdata(dociddata, fieldindex):
        cursor1 = connection.cursor()
        cursor1.execute("SELECT D.docid_tbldoc, "
                        "companyname_tblcompanies_ctbldoc, "
                        "firstname_tblcontacts_ctbldoc, "
                        "lastname_tblcontacts_ctbldoc, "
                        "Doc_kind_name_tblDoc_kind, "
                        "pretag_tbldockind, "
                        "docnumber_tbldoc, "
                        "creationtime_tbldoc, "
                        "subject_tbldoc, "
                        "Doc_kindid_tblDoc_kind, "
#                        "1 " 

                        "numberofcorlines.corlines, "
                        "podocdetailsset.polines "
                        "FROM quotation_tbldoc as D "
                        "JOIN quotation_tbldoc_kind "
                        "ON D.Doc_kindid_tblDoc_id=quotation_tbldoc_kind.doc_kindid_tbldoc_kind "

                        "JOIN (SELECT count(Docid_tblDoc_details_id) as corlines "
                        "       FROM quotation_tbldoc_details"
                        "       WHERE Docid_tblDoc_details_id = %s) as numberofcorlines  "

                        "JOIN (SELECT count(D1.Docid_tblDoc_details_id) as polines "
                        "       FROM quotation_tbldoc_details as D1 "

                        "       JOIN quotation_tbldoc_details as D2 "
                        "       ON D1.Doc_detailsid_tblDoc_details=D2.podetailslink_tbldocdetails "

                        "       JOIN quotation_tbldoc as Doc "
                        "       ON D2.Docid_tblDoc_details_id=Doc.Docid_tblDoc "

                        "       WHERE obsolete_tbldoc=0) as podocdetailsset "

                        "WHERE D.docid_tbldoc = %s", [dociddata, dociddata])

        results = cursor1.fetchall()
        resultslen = len(results)
        if resultslen != 0:
            for x in results:
                result = x[fieldindex]

                if x[9]!=2 and fieldindex == 10:
                    result = ''
                if x[9]!=2 and fieldindex == 11:
                    result = ''

        else:
            result=''
        return result
    #doclevel-1 start
    cursor1 = connection.cursor()

    cursor1.execute("SELECT " # self join if parentdoc is obsolete -> 0 length results2
                    "p.Docid_tblDoc as parent, "
                    "d.Docid_tblDoc as doc "
                    "FROM quotation_tbldoc d "
                    "LEFT JOIN quotation_tbldoc p "
                    "ON d.doclinkparentid_tblDoc = p.docid_tbldoc "
                    "WHERE p.obsolete_tbldoc = 0 and d.Docid_tblDoc = %s", [docid2])
    results2 = cursor1.fetchall()
    results2len = len(results2)
    if results2len != 0:
        for x in results2:
            doclevelminus1id = x[0]
    else:

        doclevelminus1id = 0

    levelmembernumber = 0
    firstfield = doclevelminus1id
    secondfield = doclevelminus1id  # docid
    thirdfield = 0
    doctolevelminus1 = tuple(docstolevel(firstfield, secondfield, thirdfield, levelmembernumber, []))
    doclevelminus1 = ()
    doclevelminus1 = doclevelminus1 + doctolevelminus1

    #docslevel0 start

    levelmembernumber=0
    firstfield = doclevelminus1id
    secondfield = docid2  # docid
    thirdfield = 0
    doctolevel0 = tuple(docstolevel(firstfield, secondfield, thirdfield, levelmembernumber, []))
    doclevel0 = ()
    doclevel0 = doclevel0 + doctolevel0

    #docslevel1 start
    cursor1 = connection.cursor()
    cursor1.execute("SELECT doclinkparentid_tbldoc, docid_tbldoc "
                    "FROM quotation_tbldoc "
                    "WHERE doclinkparentid_tbldoc = %s and obsolete_tbldoc = 0", [docid2])
    docstolevel1 = cursor1.fetchall()

    docslevel1 = ()
    docstolevel1len=len(docstolevel1)
    docslevel1widthforsvg=222 * docstolevel1len
    docstolevel1list = list(docstolevel1)
    for z in range(docstolevel1len): #order number to the tuple for template lines
        levelmembernumber = z
        firstfield = docstolevel1list[z][0]
        secondfield = docstolevel1list[z][1]  # docid
        thirdfield = 0
        docstolevel1 = tuple(docstolevel(firstfield, secondfield, thirdfield, levelmembernumber, []))
        docslevel1 = docslevel1 + docstolevel1

    #docslevel2 start
    docscountlevel1 = len(docslevel1)
    docslevel2 = ()
    docs33tolevel2 = ()
    levelmembernumber=0
    for x in range(docscountlevel1):

        cursor2 = connection.cursor()
        cursor2.execute("SELECT doclinkparentid_tbldoc, docid_tbldoc "
                        "FROM quotation_tbldoc "
                        "WHERE doclinkparentid_tbldoc = %s and obsolete_tbldoc = 0", [docslevel1[x][1]])
        docstolevel2 = cursor2.fetchall()
        docstolevel2len=len(docstolevel2)
        docstolevel2list = list(docstolevel2)
        appendablelist= []
        for z in range(docstolevel2len): #order number to the tuple for template lines
            firstfield = docstolevel2list[z][0]
            secondfield = docstolevel2list[z][1] #docid
            thirdfield = x
            appendablelist=docstolevel(firstfield, secondfield, thirdfield, levelmembernumber, appendablelist)
            levelmembernumber=levelmembernumber+1

        docs33tolevel2 = tuple(appendablelist)
        docslevel2 = docslevel2 + docs33tolevel2

    docslevel2widthforsvg = levelmembernumber * 222

    #docslevel3 start
    docscountlevel2 = len(docslevel2)

    docslevel3 = ()
    levelmembernumber = 0
    docstolevel3withparentpointerlist = []
    for x in range(docscountlevel2):

        cursor2 = connection.cursor()
        cursor2.execute("SELECT doclinkparentid_tbldoc, docid_tbldoc "
                        "FROM quotation_tbldoc "
                        "WHERE doclinkparentid_tbldoc = %s and obsolete_tbldoc = 0", [docslevel2[x][1]])
        docstolevel3 = cursor2.fetchall()
        docstolevel3len = len(docstolevel3)
        docstolevel3list = list(docstolevel3)
        docstolevel3withparentpointerlist = []
        for z in range(docstolevel3len):  # order number to the tuple for template lines
            firstfield = docstolevel3list[z][0]
            secondfield = docstolevel3list[z][1] #docid
            thirdfield = x
            fourthfield = 200 * levelmembernumber  # rect x coordinate
            fifthfield = fourthfield + levelmembernumber * 11 + 88  # line x coordinate lower point
            sixthfield = 88 + 197 * thirdfield # line x coordinate upper point
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
    docslevel3widthforsvg = levelmembernumber * 222

    #import pdb;
    #pdb.set_trace()




    return render(request, 'quotation/doclink.html', {'doclevelminus1': doclevelminus1,
                                                      'doclevel0': doclevel0,
                                                      'docslevel1': docslevel1,
                                                      'docslevel1widthforsvg': docslevel1widthforsvg,
                                                      'docslevel2': docslevel2,
                                                      'docslevel2widthforsvg': docslevel2widthforsvg,
                                                      'docslevel3': docslevel3,
                                                      'docslevel3widthforsvg': docslevel3widthforsvg,
                                                      'fixstate': fixstate})
@login_required
def doclinkfix(request, docid, fixstate):
    request.session['fixstate'] = fixstate  # set turn on/off fix
    request.session['fixtothis'] = docid #set

    return redirect('doclink', docid=docid)
