from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# import pdb;
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
def adocsearch(request):
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


    return render(request, 'aid/adocsearch.html', {'companies': companies,
                                                        'dockindnames':dockindnames})
@group_required("manager")
@login_required
def adocsearchcontent(request):
    docnumber = request.POST['docnumber']
    dockindname = request.POST['dockindname']
    fromdate = request.POST['fromdate']
    todate = request.POST['todate']
    company = request.POST['company']

    if docnumber != '':
        docnumberformainresults = "and D1.docnumber_tbladoc='" + docnumber + "' "
    else:
        docnumberformainresults = ""
        docnumberforrowsources = ""

    if dockindname != '':
        dockindnameformainresults = "and Doc_kind_name_tblaDoc_kind='" + dockindname + "' "
        dockindnameforrowsources = "and Doc_kind_name_tblaDoc_kind='" + dockindname + "' "
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
        companyformainresults = "and companyname_tblcompanies_ctbladoc='" + company + "'"
        companyforrowsources = "and companyname_tblcompanies_ctbladoc='" + company + "'"
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

    cursor1.execute("SELECT D1.docid_tbladoc, "
                    "D1.pcd_tblcompanies_ctbladoc, "
                    "D1.town_tblcompanies_ctbladoc, "
                    "D1.Doc_kindid_tblaDoc_id, "
                    "D1.companyname_tblcompanies_ctbladoc, "
                    "D1.firstname_tblcontacts_ctbladoc, "
                    "D1.lastname_tblcontacts_ctbladoc, "
                    "D1.creationtime_tbladoc, "
                    "Doc_kind_name_tblaDoc_kind, "
                    "pretag_tbladockind, "
                    "D1.docnumber_tbladoc, " #10
                    "Doc_kindid_tblaDoc_kind, "
                    "D1.subject_tbladoc, "
                    "D1.wherefromdocid_tbladoc, "
                    "D1.wheretodocid_tbladoc, "
                    "Dfrom.fromcompanyname, "
                    "Dto.tocompanyname, "
                    "D1.obsolete_tbladoc, "
                    "Dfrom.frompretag, "
                    "Dfrom.fromdocnumber, "
                    "Dto.topretag, " #20
                    "Dto.todocnumber, "
                    "D1.stocktakingdeno_tbladoc, "
                    "D1.denoenabledflag_tbladoc, "
                    "D1.machinemadedocflag_tbladoc "
                   
                    "FROM aid_tbladoc as D1 "

                    "JOIN aid_tbladoc_kind "
                    "ON D1.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "

                    "LEFT JOIN (SELECT companyname_tblcompanies_ctbladoc as fromcompanyname, "
                    "                   docid_tbladoc as fromdocid, "
                    "                   pretag_tbladockind as frompretag, "
                    "                   docnumber_tbladoc as fromdocnumber "
                    
                    "                   FROM aid_tbladoc "

                    "                   JOIN aid_tbladoc_kind "
                    "                   ON aid_tbladoc.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "

                    "           ) as Dfrom "
                    "ON D1.wherefromdocid_tbladoc = Dfrom.fromdocid "

                    "LEFT JOIN (SELECT companyname_tblcompanies_ctbladoc as tocompanyname, "
                    "                   docid_tbladoc as todocid, "
                    "                   pretag_tbladockind as topretag, "
                    "                   docnumber_tbladoc as todocnumber "
                    
                    "                   FROM aid_tbladoc "

                    "                   JOIN aid_tbladoc_kind "
                    "                   ON aid_tbladoc.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "

                    "           ) as Dto "
                    "ON D1.wheretodocid_tbladoc = Dto.todocid "

                    "HAVING D1.obsolete_tbladoc = 0 " + searchphraseformainresults + ""
                    "order by D1.docid_tbladoc desc ")
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
    return render(request, 'aid/adocsearchcontent.html', {'docs': docs,
                                                               'companiesrowsources': companiesrowsources,
                                                               'dockindrowsources': dockindrowsources})
@group_required("manager")
@login_required
def adocadd(request):

    if request.method == "POST":

        dockindidfornewdoc = request.POST['dockindidfornewdoc']
        contactidfornewdoc = request.POST['contactidfornewdoc']
        creatorid=request.user.id

        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT contactid_tblacontacts, "
            "companyname_tblacompanies, "
            "Companyid_tblaCompanies, "
            "Firstname_tblacontacts, "
            "lastname_tblacontacts, "
            "title_tblacontacts, "
            "mobile_tblacontacts, "
            "email_tblacontacts, "
            "pcd_tblacompanies, "
            "town_tblacompanies, "
            "address_tblacompanies "
            
            "FROM aid_tblacontacts "
            
            "JOIN aid_tblacompanies "
            "ON aid_tblacompanies.companyid_tblacompanies = aid_tblacontacts.companyid_tblacontacts_id "
            
            "WHERE contactid_tblacontacts =%s", [contactidfornewdoc])
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
            "SELECT defaultbackpageidforquotation_tblacompanies, "
            "defaultprefaceidforquotation_tblacompanies, "
            "defaultpaymentid_tblacompanies "

            "FROM aid_tblacompanies "

            "WHERE Companyid_tblaCompanies = %s", [companyid])
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
        cursor8.execute("SELECT max(docnumber_tblaDoc) FROM aid_tbladoc "
                        "WHERE Doc_kindid_tblaDoc_id = %s", [dockindidfornewdoc])
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
        cursor2.execute("INSERT INTO aid_tbladoc "
                        "( Doc_kindid_tblaDoc_id, "
                        "Contactid_tblaDoc_id,"
                        "companyname_tblcompanies_ctbladoc, "
                        "firstname_tblcontacts_ctbladoc, "
                        "lastname_tblcontacts_ctbladoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                        "docnumber_tblaDoc, "
                        "creatorid_tbladoc, "
                        "title_tblcontacts_ctbladoc, "
                        "mobile_tblcontacts_ctbladoc, "
                        "email_tblcontacts_ctbladoc, "
                        "pcd_tblcompanies_ctbladoc, "
                        "town_tblcompanies_ctbladoc, "
                        "address_tblcompanies_ctbladoc, "
                        "paymenttextforquotation_tblpayment_ctbladoc, "
                        "accountcurrencycode_tbladoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
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
        cursor3.execute("SELECT max(Docid_tblaDoc) FROM aid_tbladoc")
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        cursor4 = connection.cursor()
        cursor4.execute(
            "INSERT INTO aid_tbladoc_details ( Docid_tblaDoc_details_id) VALUES (%s)",
            [maxdocid])

        return redirect('adocselector', pk=maxdocid)

    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT aid_tblacontacts.contactid_tblacontacts, aid_tblacompanies.companyname_tblacompanies,"
        "aid_tblacontacts.Firstname_tblacontacts, aid_tblacontacts.lastname_tblacontacts "
        "FROM aid_tblacontacts "
        "JOIN aid_tblacompanies "
        "ON aid_tblacompanies.companyid_tblacompanies = aid_tblacontacts.companyid_tblacontacts_id "
        "ORDER BY companyname_tblacompanies")
    contacts = cursor0.fetchall()
    transaction.commit()

    cursor = connection.cursor()
    cursor.execute("SELECT doc_kindid_tbladoc_kind, doc_kind_name_tbladoc_kind FROM aid_tbladoc_kind")
    dockinds = cursor.fetchall()
    transaction.commit()

    return render(request, 'aid/adocadd.html', {'dockinds': dockinds, 'contacts': contacts})
@group_required("manager")
@login_required
def adocselector(request, pk):
    cursor = connection.cursor()
    cursor.execute("SELECT  aid_tbladoc_kind.Doc_kindid_tbladoc_kind "
     
                   "FROM aid_tbladoc "
     
                   "JOIN aid_tbladoc_kind "
                   "ON aid_tbladoc.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "
     
                   "WHERE aid_tbladoc.docid_tbladoc=%s ", [pk])
    results = cursor.fetchall()
    for x in results:
        dockind = x[0]

    if dockind == 1:  # Quotation
        return redirect('quotationform', pk=pk)
    elif dockind == 2:  # CustomerOrder
        return redirect('acustomerorderform', pk=pk)
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
    elif dockind == 9:  # Customer Acknowledgement
        return redirect('acustomeracknowledgementform', pk=pk)
    elif dockind == 10:  # Customer Cart
        return redirect('acustomercartform', pk=pk)
@group_required("manager")
@login_required
def adocremove(request, pk):
    cursor1 = connection.cursor()
    cursor1.execute(
        "UPDATE aid_tbladoc SET "
        "obsolete_tbladoc=1 "
        "WHERE docid_tbladoc =%s ", [pk])

    transaction.commit()

    return redirect('adocsearch')
@group_required("manager")
@login_required
def adocorderadd(request):
    if request.method == "POST":
        qty2 = request.POST['qty2']
        creatorid = request.user.id
#        import pdb;
#        pdb.set_trace()


        cursor1 = connection.cursor()
        cursor1.execute(
            "SELECT contactid_tblacontacts, "
            "companyname_tblacompanies, "
            "Companyid_tblaCompanies, "
            "Firstname_tblacontacts, "
            "lastname_tblacontacts, "
            "title_tblacontacts, "
            "mobile_tblacontacts, "
            "email_tblacontacts, "
            "pcd_tblacompanies, "
            "town_tblacompanies, "
            "address_tblacompanies "

            "FROM aid_tblacontacts "

            "JOIN aid_tblacompanies "
            "ON aid_tblacompanies.companyid_tblacompanies = aid_tblacontacts.companyid_tblacontacts_id "

            "WHERE contactid_tblacontacts =%s", [13])
        companyandcontactdata = cursor1.fetchall()

        for instancesingle in companyandcontactdata:
            companynameclone = instancesingle[1]

            companyid = instancesingle[2]  # for the lookup the default values in the tblcompanies (i.e. defaultpreface)
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
        cursor8.execute("SELECT max(docnumber_tblaDoc) FROM aid_tbladoc "
                        "WHERE Doc_kindid_tblaDoc_id = %s", ['2'])
        results = cursor8.fetchall()
        resultslen = len(results)
        # import pdb;
        # pdb.set_trace()

        if results[0][0] is not None:  # only if there is not doc yet (this would be the first instance)
            for x in results:
                docnumber = x[0]
                docnumber += 1
        else:
            docnumber = 80  # arbitrary number

        cursor2 = connection.cursor()
        cursor2.execute("INSERT INTO aid_tbladoc "
                        "( Doc_kindid_tblaDoc_id, "
                        "Contactid_tblaDoc_id,"
                        "companyname_tblcompanies_ctbladoc, "
                        "firstname_tblcontacts_ctbladoc, "
                        "lastname_tblcontacts_ctbladoc, "
                        "prefacetextforquotation_tblprefaceforquotation_ctbladoc, "
                        "backpagetextforquotation_tblbackpageforquotation_ctbladoc, "
                        "docnumber_tblaDoc, "
                        "creatorid_tbladoc, "
                        "title_tblcontacts_ctbladoc, "
                        "mobile_tblcontacts_ctbladoc, "
                        "email_tblcontacts_ctbladoc, "
                        "pcd_tblcompanies_ctbladoc, "
                        "town_tblcompanies_ctbladoc, "
                        "address_tblcompanies_ctbladoc, "
                        "paymenttextforquotation_tblpayment_ctbladoc, "
                        "accountcurrencycode_tbladoc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        ['2', '1', companynameclone, firstnameclone, lastnameclone,
                         prefacecloneforquotation, backpagetextcloneforquotation, docnumber, creatorid,
                         titleclone,
                         mobileclone,
                         emailclone,
                         pcdclone,
                         townclone,
                         addressclone,
                         paymenttextcloneforquotation,
                         accountcurrencycodeclone])

        cursor3 = connection.cursor()
        cursor3.execute("SELECT max(Docid_tblaDoc) "
                        ""
                        "FROM aid_tbladoc")
        results = cursor3.fetchall()
        for x in results:
            maxdocid = x[0]

        cursor3 = connection.cursor()
        cursor3.execute("SELECT "
                        "Doc_kindid_tblaDoc_id, "
                        "docnumber_tblaDoc, "
                        "pretag_tbladockind "

                        "FROM aid_tbladoc "

                        "JOIN aid_tbladoc_kind as DK "
                        "ON Doc_kindid_tblaDoc_id = DK.Doc_kindid_tblaDoc_kind "

                        "WHERE docid_tbladoc=%s ", [maxdocid])
        customerordernumbers = cursor3.fetchall()
        for x in customerordernumbers:
            customerordernumberdocnumber = x[1]
            customerordernumberpretag = x[2]
        customerordernumber = str(customerordernumberpretag) + str(customerordernumberdocnumber)
#product variables filling begin
        cursor0 = connection.cursor()
        cursor0.execute(
            "SELECT `Productid_tblaProduct`, "
            "`purchase_price_tblaproduct`, `"
            "customerdescription_tblaProduct`, "
            "`margin_tblaproduct`, "
            "`currencyisocode_tblcurrency_ctblaproduct`, "
            "currencyrate_tblacurrency, "
            "unit_tblaproduct, "
            "supplierdescription_tblaProduct, "
            "suppliercompanyid_tblaProduct "
            "FROM `aid_tblaproduct` "
            "LEFT JOIN aid_tblacurrency "
            "ON aid_tblaproduct.currencyisocode_tblcurrency_ctblaproduct=aid_tblacurrency.currencyisocode_tblacurrency "
            "WHERE Productid_tblaProduct= %s", ['2'])
        results = cursor0.fetchall()
        for instancesingle in results:
            purchase_priceclone = instancesingle[1]
            customerdescriptionclone = instancesingle[2]
            currencyisocodeclone = instancesingle[4]
            marginfromproducttable = instancesingle[3]
            listpricecomputed = round((100 * purchase_priceclone) / (100 - marginfromproducttable), 2)
            currencyrateclone = instancesingle[5]
            unitclone = instancesingle[6]
            supplierdescriptionclone = instancesingle[7]
            suppliercompanyidclone = instancesingle[8]

            unitsalespriceACU = listpricecomputed * currencyrateclone
        # import pdb;
        # pdb.set_trace()
# product variables filling end
# product row to docdetails begin
        cursor1 = connection.cursor()  # new row needed
        cursor1.execute(
            "INSERT INTO aid_tbladoc_details "
            "(`Qty_tblaDoc_details`, "
            "`Docid_tblaDoc_details_id`, "
            "`Productid_tblaDoc_details_id`, "
            "`firstnum_tblaDoc_details`, "
            "`fourthnum_tblaDoc_details`, "
            "`secondnum_tblaDoc_details`, "
            "`thirdnum_tblaDoc_details`, "
            "`Note_tblaDoc_details`, "
            "`purchase_price_tblproduct_ctblaDoc_details`, "
            "`customerdescription_tblProduct_ctblaDoc_details`, "
            "`currencyisocode_tblcurrency_ctblproduct_ctblaDoc_details`, "
            "listprice_tblaDoc_details, "
            "currencyrate_tblcurrency_ctblaDoc_details, "
            "unitsalespriceACU_tblaDoc_details, "
            "unit_tbladocdetails, "
            "`supplierdescription_tblProduct_ctblaDoc_details`, "
            "suppliercompanyid_tblaDocdetails) "
        
            "VALUES (%s, %s, %s, %s,%s,%s,%s,'Defaultnote', %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [qty2,
             maxdocid,
             '2',
             '1',
             '1',
             '1',
             '1',
             purchase_priceclone,
             customerdescriptionclone,
             currencyisocodeclone,
             listpricecomputed,
             currencyrateclone,
             unitsalespriceACU,
             unitclone,
             supplierdescriptionclone,
             suppliercompanyidclone])
# product row to docdetails end
        # email acknowledgement begin
        foo = 11
        html_message = render_to_string('aid/acustomeracknowledgementemail.html', {'context': 'values', 'customerordernumber': customerordernumber})
        email = EmailMessage(
            'Aid Order Acknowledgement', html_message, 'from@me.com', ['szluka.mate@gmail.com'])  # , cc=[cc])
        email.content_subtype = "html"
        email.send()

        # email acknowledgement end

        return redirect('adocselector', pk=maxdocid)

    cursor0 = connection.cursor()
    cursor0.execute(
        "SELECT aid_tblacontacts.contactid_tblacontacts, aid_tblacompanies.companyname_tblacompanies,"
        "aid_tblacontacts.Firstname_tblacontacts, aid_tblacontacts.lastname_tblacontacts "
        "FROM aid_tblacontacts "
        "JOIN aid_tblacompanies "
        "ON aid_tblacompanies.companyid_tblacompanies = aid_tblacontacts.companyid_tblacontacts_id "
        "ORDER BY companyname_tblacompanies")
    contacts = cursor0.fetchall()
    transaction.commit()

    cursor = connection.cursor()
    cursor.execute("SELECT doc_kindid_tbldoc_kind, doc_kind_name_tbldoc_kind FROM quotation_tbldoc_kind")
    dockinds = cursor.fetchall()
    transaction.commit()

    return render(request, 'aid/adocadd.html', {'dockinds': dockinds, 'contacts': contacts})
@group_required("manager")
@login_required
def adocmyorderssearch(request):
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


    return render(request, 'aid/adocmyorderssearch.html', {'companies': companies,
                                                        'dockindnames':dockindnames})


@group_required("manager")
@login_required
def adocmyorderssearchcontent(request):
    creatorid = request.user.id

    fromdate = request.POST['fromdate']
    todate = request.POST['todate']
    datephraseformainresults = ''
    datephraseforrowsources = ''

    searchphraseformainresults = datephraseformainresults + " "
    searchphraseforrowsources = " "

    cursor1 = connection.cursor()

    cursor1.execute("SELECT D1.docid_tbladoc, "
                    "D1.pcd_tblcompanies_ctbladoc, "
                    "D1.town_tblcompanies_ctbladoc, "
                    "D1.Doc_kindid_tblaDoc_id, "
                    "D1.companyname_tblcompanies_ctbladoc, "
                    "D1.firstname_tblcontacts_ctbladoc, "
                    "D1.lastname_tblcontacts_ctbladoc, "
                    "D1.creationtime_tbladoc, "
                    "Doc_kind_name_tblaDoc_kind, "
                    "pretag_tbladockind, "
                    "D1.docnumber_tbladoc, "  # 10
                    "Doc_kindid_tblaDoc_kind, "
                    "D1.subject_tbladoc, "
                    "D1.wherefromdocid_tbladoc, "
                    "D1.wheretodocid_tbladoc, "
                    "Dfrom.fromcompanyname, "
                    "Dto.tocompanyname, "
                    "D1.obsolete_tbladoc, "
                    "Dfrom.frompretag, "
                    "Dfrom.fromdocnumber, "
                    "Dto.topretag, "  # 20
                    "Dto.todocnumber, "
                    "D1.stocktakingdeno_tbladoc, "
                    "D1.denoenabledflag_tbladoc, "
                    "D1.machinemadedocflag_tbladoc, "
                    "D1.Contactid_tbladoc_id, "
                    "D1.creatorid_tbladoc "

                    "FROM aid_tbladoc as D1 "

                    "JOIN aid_tbladoc_kind "
                    "ON D1.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "

                    "LEFT JOIN (SELECT companyname_tblcompanies_ctbladoc as fromcompanyname, "
                    "                   docid_tbladoc as fromdocid, "
                    "                   pretag_tbladockind as frompretag, "
                    "                   docnumber_tbladoc as fromdocnumber "

                    "                   FROM aid_tbladoc "

                    "                   JOIN aid_tbladoc_kind "
                    "                   ON aid_tbladoc.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "

                    "           ) as Dfrom "
                    "ON D1.wherefromdocid_tbladoc = Dfrom.fromdocid "

                    "LEFT JOIN (SELECT companyname_tblcompanies_ctbladoc as tocompanyname, "
                    "                   docid_tbladoc as todocid, "
                    "                   pretag_tbladockind as topretag, "
                    "                   docnumber_tbladoc as todocnumber "

                    "                   FROM aid_tbladoc "

                    "                   JOIN aid_tbladoc_kind "
                    "                   ON aid_tbladoc.Doc_kindid_tblaDoc_id=aid_tbladoc_kind.doc_kindid_tbladoc_kind "

                    "           ) as Dto "
                    "ON D1.wheretodocid_tbladoc = Dto.todocid "

                    "HAVING D1.obsolete_tbladoc = 0 " + searchphraseformainresults + " and D1.creatorid_tbladoc = " + str(creatorid) + " and D1.Doc_kindid_tblaDoc_id=2 "
                                                                                     "order by D1.docid_tbladoc desc ")
    docs = cursor1.fetchall()

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
    return render(request, 'aid/adocmyorderssearchcontent.html', {'docs': docs,
                                                          'companiesrowsources': companiesrowsources,
                                                          'dockindrowsources': dockindrowsources})
