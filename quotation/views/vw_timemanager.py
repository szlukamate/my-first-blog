from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from quotation.models import tblDoc, tblDoc_kind, tblDoc_details
from django.contrib.auth.decorators import login_required
from quotation.forms import quotationroweditForm
from collections import namedtuple
from django.db import connection, transaction, connections
from array import *
import simplejson as json
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
import subprocess
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as x12
# import pdb;
# pdb.set_trace()
@login_required
def timemanager(request):
        # filtering options to Addfilter selectbox begin
        # Creates a list containing #h lists, each of #w items, all set to 0
        w, h = 3, 3;
        addfilterselectvaluesandoptions = [[0 for x in range(w)] for y in range(h)]

        addfilterselectvaluesandoptions[0][0] = 'Project Name'
        addfilterselectvaluesandoptions[0][1] = 'projectid'

        addfilterselectvaluesandoptions[1][0] = 'Listprice'
        addfilterselectvaluesandoptions[1][1] = 'listprice'

        addfilterselectvaluesandoptions[2][0] = 'Supplier'
        addfilterselectvaluesandoptions[2][1] = 'supplier'
        # filtering options to Addfilter selectbox end

        # import pdb;
        # pdb.set_trace()

        return render(request, 'quotation/timemanager.html', {'addfilterselectvaluesandoptions': addfilterselectvaluesandoptions})
@login_required
def timemanagersearchcontent(request):
    filteritemlistraw = request.POST['filteritemlist']
    filteritemlist = json.loads(filteritemlistraw)

    filteritemname = ''
    filteritemoperator = ''
    filteritemfirstinput = ''
    filteritemsecondinput = ''

    customerdescriptionphrase = ""
    listpricephrase = ""
    supplierphrase = ""

    for x in range(0,len(filteritemlist),4):

        filteritemname = filteritemlist[(x+0)]
        filteritemoperator = filteritemlist[x+1]
        filteritemfirstinput = filteritemlist[x+2]
        filteritemsecondinput = filteritemlist[x+3]

        if filteritemname == 'customerdescription':
            if filteritemoperator == 'contains':
                customerdescriptionphrase = "and customerdescription_tblProduct  LIKE '%" + filteritemfirstinput + "%' "
            if filteritemoperator == 'doesntcontain':
                customerdescriptionphrase = "and customerdescription_tblProduct NOT LIKE '%" + filteritemfirstinput + "%' "

        if filteritemname == 'listprice':
            if filteritemoperator == 'gteq':
                listpricephrase = "and purchase_price_tblproduct >= " + filteritemfirstinput + " "
            if filteritemoperator == 'lteq':
                listpricephrase = "and purchase_price_tblproduct <= " + filteritemfirstinput + " "

        if filteritemname == 'supplier':
            if filteritemoperator == 'is':
                supplierphrase = "and suppliercompanyid_tblproduct = " + filteritemfirstinput + " "

    searchphraseformainresults = (customerdescriptionphrase + listpricephrase + supplierphrase + " ")
#                                  datephraseformainresults + companyformainresults + usernameformainresults +
#                                  activitynameformainresults + quoteddocnumberformainresults + " ")
    searchphraseforrowsources = searchphraseformainresults
    cursor = connection.cursor()
    cursor.execute("SELECT "
                   "timedoneid_tbltimedone, "
                   "hours_tbltimedone, "
                   "projectid_tbltimedone, "
                   "name_tblprojects_redmine_ctbltimedone, "
        "           userid_tbltimedone, "
        "           username_redmine_ctbltimedone, " #5
                   "issueid_tbltimedone, "
                   "issuesubject_redmine_ctbltimedone, "
                   "comments_tbltimedone, "
                   "spenton_tbltimedone, "
                   "timeentryidinits_tbltimedone " #10

                   "FROM quotation_tbltimedone "

                   "WHERE timedoneid_tbltimedone is not null " + searchphraseformainresults + ""
                    )
    timedonespre = cursor.fetchall()
    timedonesnumberofitems = len(timedonespre)

# timedones to temptable begin
    cursor2 = connection.cursor()
    cursor2.execute("DROP TEMPORARY TABLE IF EXISTS timedonetemptable;")
    cursor2.execute("CREATE TEMPORARY TABLE IF NOT EXISTS timedonetemptable "
                    "    ( auxid INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                    "     hours_tbltimedonetemptable FLOAT NOT NULL, "
                    "     projectid_tbltimedonetemptable INT(11) NULL, "
                    "     userid_tbltimedonetemptable INT(11) NULL, "
                    "     issueid_tbltimedonetemptable INT(11) NULL, "
                    "     comments_tbltimedonetemptable varchar(1024) NULL,"
                    "     spenton_tbltimedonetemptable DATE NULL,"
                    "     timeentryidinits_tbltimedonetemptable INT(11) NULL, "
                    "     issueidredbackgroundflag_tbltimedonetemptable INT(11) NULL) " #if projectid alien for issueid the issueid background needs to be set to red

                    "      ENGINE=INNODB "
                    "    ; ")
    for x11 in timedonespre:
        hours = x11[1]
        if hours == None:
            hours = 0
        #hours = round(hours,2)
        projectid = x11[2]
        userid = x11[4]
        issueid = x11[6]
        comments = x11[8]
        spenton = x11[9]
        timeentryidinits = x11[10]
        if timeentryidinits == None:
            timeentryidinits = 0

        cursor2.execute("INSERT INTO timedonetemptable (hours_tbltimedonetemptable, "
                        "projectid_tbltimedonetemptable, "
                        "userid_tbltimedonetemptable, "
                        "issueid_tbltimedonetemptable, "
                        "comments_tbltimedonetemptable, "
                        "spenton_tbltimedonetemptable, "
                        "timeentryidinits_tbltimedonetemptable) VALUES ('" + str(hours) + "', "
                                                    "'" + str(projectid) + "', "
                                                    "'" + str(userid) + "', "
                                                    "'" + str(issueid) + "', "
                                                    "'" + str(comments) + "', "
                                                    "'" + str(spenton) + "', "
                                                    "'" + str(timeentryidinits) + "');")

    cursor2.execute("SELECT   "
                        "auxid, "
                        "hours_tbltimedonetemptable, "
                        "projectid_tbltimedonetemptable, "
                        "userid_tbltimedonetemptable, "
                    "   issueid_tbltimedonetemptable, "
                    "   comments_tbltimedonetemptable, " #5
                    "   spenton_tbltimedonetemptable, "
                    "   timeentryidinits_tbltimedonetemptable "

                        "FROM timedonetemptable ")
    timedonesunsetflag = cursor2.fetchall()

# timedones to temptable end

# setting issueidredbackgroundflag begin
    for x in timedonesunsetflag:
        issueid
    cursor25 = connections['redmine'].cursor()
    cursor25.execute("SELECT "
                     "I.id, "
                     "subject, "
                     "project_id, "
                     "projects.name "

                     "FROM issues as I "

                     "JOIN projects "
                     "ON I.project_id = projects.id "

                     "WHERE I.id is not null and status = 1 ")

    issuerowsourcessss = cursor25.fetchall()

    # setting issueidredbackgroundflag end
    #import pdb;
    #pdb.set_trace()

    cursor23 = connections['redmine'].cursor()
    cursor23.execute("SELECT "
                     "id, "
                     "name "

                     "FROM projects "

                     "WHERE id is not null and status = 1 " + searchphraseforrowsources + " ")

    projectnamerowsources = cursor23.fetchall()

    cursor24 = connections['redmine'].cursor()
    cursor24.execute("SELECT "
                     "id, "
                     "CONCAT(firstname, ' ', lastname) AS username "

                     "FROM users "

                     "WHERE id is not null " + searchphraseforrowsources + " ")

    usernamerowsources = cursor24.fetchall()
    '''
    cursor25 = connections['redmine'].cursor()
    cursor25.execute("SELECT "
                     "id, "
                     "subject, "
                     "project_id "

                     "FROM issues ")

    issuerowsources = cursor25.fetchall()
    '''
    cursor25 = connections['redmine'].cursor()
    cursor25.execute("SELECT "
                     "I.id, "
                     "subject, "
                     "project_id, "
                     "projects.name "

                     "FROM issues as I "

                     "JOIN projects "
                     "ON I.project_id = projects.id "
                     
                     "WHERE I.id is not null and status = 1 ")

    issuerowsources = cursor25.fetchall()

    #import pdb;
    #pdb.set_trace()
#
    return render(request, 'quotation/timemanagercontent.html', {'timedones': timedonespre,
                                                       'projectnamerowsources': projectnamerowsources,
                                                       'usernamerowsources': usernamerowsources,
                                                       'issuerowsources': issuerowsources,
                                                       'timedonesnumberofitems': timedonesnumberofitems})
@login_required
def timemanagerupdateprojectselect(request):
    if request.method == 'POST':
        timedoneidinjs = request.POST['timedoneidinjs']
        projectidinjs = request.POST['projectidinjs']
        projectnameinjs = request.POST['projectnameinjs']

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tbltimedone SET "
                    "projectid_tbltimedone= %s, name_tblprojects_redmine_ctbltimedone = %s "
                    "WHERE timedoneid_tbltimedone =%s ", [projectidinjs, projectnameinjs, timedoneidinjs])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT "
        "           projectid_tbltimedone, "
    "               name_tblprojects_redmine_ctbltimedone "
        
        "FROM quotation_tbltimedone "
        
        "WHERE timedoneid_tbltimedone= %s ", [timedoneidinjs])
    results = cursor3.fetchall()
    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def timemanagerupdateuserselect(request):
    if request.method == 'POST':
        timedoneidinjs = request.POST['timedoneidinjs']
        useridinjs = request.POST['useridinjs']
        usernameinjs = request.POST['usernameinjs']

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tbltimedone SET "
                    "userid_tbltimedone= %s, username_redmine_ctbltimedone = %s "
                    "WHERE timedoneid_tbltimedone =%s ", [useridinjs, usernameinjs, timedoneidinjs])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT "
        "           userid_tbltimedone, "
        "           username_redmine_ctbltimedone "
        
        "FROM quotation_tbltimedone "
        
        "WHERE timedoneid_tbltimedone= %s ", [timedoneidinjs])
    results = cursor3.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def timemanagerupdateissueselect(request):
    if request.method == 'POST':
        timedoneidinjs = request.POST['timedoneidinjs']
        issueidinjs = request.POST['issueidinjs']
        issuesubjectinjs = request.POST['issuesubjectinjs']

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tbltimedone SET "
                    "issueid_tbltimedone= %s, issuesubject_redmine_ctbltimedone = %s "
                    "WHERE timedoneid_tbltimedone =%s ", [issueidinjs, issuesubjectinjs, timedoneidinjs])

    cursor3 = connection.cursor()
    cursor3.execute(
        "SELECT "
        "           issueid_tbltimedone, "
        "           issuesubject_redmine_ctbltimedone "
        
        "FROM quotation_tbltimedone "
        
        "WHERE timedoneid_tbltimedone= %s ", [timedoneidinjs])
    results = cursor3.fetchall()

    json_data = json.dumps(results)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def timemanagerfieldupdate(request):
    if request.method == "POST":
        fieldvalue = request.POST['fieldvalue']
        rowid = request.POST['rowid']
        fieldname = request.POST['fieldname']
        #import pdb;
        #pdb.set_trace()

        cursor22 = connection.cursor()
        cursor22.callproc("sptimemanagerfieldsupdate", [fieldname, fieldvalue, rowid])
        results23 = cursor22.fetchall()
        print(results23)
        '''
        cursor2 = connection.cursor()
        sqlquery = "UPDATE quotation_tbltimedone SET " + fieldname + "= '"  + fieldvalue + "' WHERE timedoneid_tbltimedone =" + rowid
        cursor2.execute(sqlquery)

        cursor3 = connection.cursor()
        cursor3.execute("SELECT " + fieldname + " "
                       "FROM quotation_tbltimedone "
                        "WHERE timedoneid_tbltimedone= %s ", [rowid])
        results = cursor3.fetchall()
        '''
        json_data = json.dumps(results23)

        return HttpResponse(json_data, content_type="application/json")
@login_required
def timemanageruploadtoits(request):
    creatorid = request.user.id
    BASE_DIR = settings.BASE_DIR

    timedonesnumberofitems = request.POST['timedonesnumberofitems']
    itemdatalistraw = request.POST['itemdatalist']
    itemdatalist = json.loads(itemdatalistraw)

    for x in range(int(timedonesnumberofitems)):

        timedoneid = itemdatalist[(7*x+0)]
        projectid = itemdatalist[(7*x+1)]
        userid = itemdatalist[(7*x+2)]
        issueid = itemdatalist[7*x+3]
        hours = itemdatalist[7*x+4]
        comments = itemdatalist[7*x+5]
        spenton = itemdatalist[7*x+6]

        firstnum = x + 1
        fourthnum = 0
        secondnum = 0
        #import pdb;
        #pdb.set_trace()

    cursor21 = connections['redmine'].cursor()
    cursor21.execute(
        "INSERT INTO time_entries "
        "( project_id, "
        "user_id, "
        "issue_id, "
        "hours, "
        "comments, "
        "activity_id, " #5
        "spent_on, "
        "tyear, "
        "tmonth, "
        "tweek, "
        "created_on, " #10
        "updated_on, "
        "creatoridfromquotationmaker) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

        [projectid,
         userid,
         issueid,
         hours,
         comments,
#         activityid,
         8,
         spenton,
#         tyear,
         2010,
#         tmonth,
         10,
#         tweek,
         10,
#         createdon,
         '2020-12-12-',
#         updatedon])
         '2020-12-12-',
         creatorid])
    cursor3 = connections['redmine'].cursor()
    cursor3.execute(
        "SELECT "
        "max(id) "

        "FROM time_entries "

        "WHERE creatoridfromquotationmaker = %s",
        [creatorid])
    results = cursor3.fetchall()
    for x in results:
        timeentryid = x[0]
    # import pdb;
    # pdb.set_trace()
    cursor21.execute("INSERT INTO custom_values " #insert the timeentryid custom field
                     "(value, "
                     "custom_field_id, "
                     "customized_type, "
                     "customized_id) VALUES (%s,%s,%s,%s)",

                     [timeentryid,
                      8,
                      'TimeEntry',
                      timeentryid])

    cursor21.execute("INSERT INTO custom_values " #insert the quoteddocdetailsid custom field
                     "(value, "
                     "custom_field_id, "
                     "customized_type, "
                     "customized_id) VALUES (%s,%s,%s,%s)",

                     [None,
                      4,
                      'TimeEntry',
                      timeentryid])

    cursor21.execute("INSERT INTO custom_values " #insert the quoteddocnumber custom field
                     "(value, "
                     "custom_field_id, "
                     "customized_type, "
                     "customized_id) VALUES (%s,%s,%s,%s)",

                     [None,
                      6,
                      'TimeEntry',
                      timeentryid])

    cursor2 = connection.cursor()
    cursor2.execute("UPDATE quotation_tbltimedone SET " #update timeentryid which get from Issue Tracking System - not null means: the timedone item is uploaded to ITS
                     "timeentryidinits_tbltimedone = %s "
                     "WHERE timedoneid_tbltimedone = %s ",
                     [timeentryid, timedoneid ])

    results23 = 0
    json_data = json.dumps(results23)

    return HttpResponse(json_data, content_type="application/json")
@login_required
def timedoneitemnew(request):

    cursor1 = connection.cursor()
    cursor1.execute("INSERT INTO quotation_tbltimedone "
                    "(spenton_tbltimedone) VALUES ('2020-01-01')")

    return redirect('timemanager')
@login_required
def timedoneitemremove(request,pktimedoneid):

    cursor1 = connection.cursor()
    cursor1.execute(
        "DELETE FROM quotation_tbltimedone WHERE timedoneid_tbltimedone=%s ", [pktimedoneid])

    return redirect('timemanager')


@login_required
def timemanagerupdateissueselectafterchangeprojectselect(request): # <-- see name
    timedoneidinjs = request.POST['timedoneidinjs']
    projectidinjs = request.POST['projectidinjs']

    cursor3 = connections['redmine'].cursor()
    cursor3.execute("SELECT "
                     "id, "
                     "subject, "
                     "project_id "

                     "FROM issues "

                     "WHERE project_id = %s ", [projectidinjs])

    selectoptions = cursor3.fetchall()

    return render(request, 'quotation/timemanagerissueselecthtmlafterupdateprojectselect.html',
                  {'timedoneid': timedoneidinjs,
                  'selectoptions': selectoptions})
