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
def filtertemplatehtmlonproductform(request):
        invokedfrom = request.POST['invokedfrom']

        if invokedfrom == 'filteritemselectchanged': # when we want change a filteritems on html (clicking the selectbox on filteritem)
                filteritemselectedvalue = request.POST['filteritemselectedvalue']
                filteritemname = request.POST['filteritemname']
                filteritemrowid = request.POST['filteritemrowid']

                if filteritemname == 'customerdescription':
                        if filteritemselectedvalue == 'contains':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'doesntcontain':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'none':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'any':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'listprice':
                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'gteq':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'lteq':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'between':

                                return render(request, 'quotation/filteritemtemplatebetweeninputbox.html', {'filteritemrowid': filteritemrowid})

                        if filteritemselectedvalue == 'none':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'any':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'supplier':

                    cursor3 = connection.cursor()
                    cursor3.execute(
                        "SELECT companyid_tblcompanies, companyname_tblcompanies FROM quotation_tblcompanies")
                    supplierlist = cursor3.fetchall()

                    if filteritemselectedvalue == 'is':

                            return render(request, 'quotation/filteritemtemplateselect.html', {'filteritemfirstinputboxselectoptions': supplierlist,
                                                                                               'filteritemrowid': filteritemrowid})

                    if filteritemselectedvalue == 'isnot':

                            return render(request, 'quotation/filteritemtemplateselect.html', {'filteritemfirstinputboxselectoptions': supplierlist,
                                                                                               'filteritemrowid': filteritemrowid})

                    if filteritemselectedvalue == 'none':

                            return render(request, 'quotation/filteritemtemplateempty.html', {})

                    if filteritemselectedvalue == 'any':

                            return render(request, 'quotation/filteritemtemplateempty.html', {})

        if invokedfrom == 'addfilterselectchanged': # when we want to search first click the #Add Filter selectbox and add some filteritems to html
                filteritemrowid = request.POST['filteritemmaxrowid']
                selectedvalue = request.POST['selectedvalue']
                selectedoption = request.POST['selectedoption'] # name which appears for user


                if selectedvalue == 'customerdescription': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'customerdescription' #attribute for elements

                    filteritemselectoptions[0][0] = 'contains'
                    filteritemselectoptions[0][1] = 'contains'

                    filteritemselectoptions[1][0] = 'doesntcontain'
                    filteritemselectoptions[1][1] = "doesn't contain"

                    filteritemselectoptions[2][0] = 'none'
                    filteritemselectoptions[2][1] = 'none'

                    filteritemselectoptions[3][0] = 'any'
                    filteritemselectoptions[3][1] = 'any'

                if selectedvalue == 'listprice':

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 6;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'listprice' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                    filteritemselectoptions[1][0] = 'gteq'
                    filteritemselectoptions[1][1] = '>='

                    filteritemselectoptions[2][0] = 'lteq'
                    filteritemselectoptions[2][1] = '<='

                    filteritemselectoptions[3][0] = 'between'
                    filteritemselectoptions[3][1] = 'between'

                    filteritemselectoptions[4][0] = 'none'
                    filteritemselectoptions[4][1] = 'none'

                    filteritemselectoptions[5][0] = 'any'
                    filteritemselectoptions[5][1] = 'any'

                if selectedvalue == 'supplier': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'supplier' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                    filteritemselectoptions[1][0] = 'isnot'
                    filteritemselectoptions[1][1] = "is not"

                    filteritemselectoptions[2][0] = 'none'
                    filteritemselectoptions[2][1] = 'none'

                    filteritemselectoptions[3][0] = 'any'
                    filteritemselectoptions[3][1] = 'any'

        return render(request, 'quotation/filtertemplatehtml.html',{'selectedoption': selectedoption,
                                                                    'filteritemrowid': filteritemrowid,
                                                                    'filteritemname': filteritemname,
                                                                    'filteritemselectoptions': filteritemselectoptions})
def filtertemplatehtmlonquotationtimeentryform(request):
        invokedfrom = request.POST['invokedfrom']
        searchphraseformainresults = request.POST['searchphraseformainresults']
        #import pdb;
        #pdb.set_trace()

        if invokedfrom == 'filteritemselectchanged': # when we want change a filteritems on html (clicking the selectbox on filteritem)
                filteritemselectedvalue = request.POST['filteritemselectedvalue']
                filteritemname = request.POST['filteritemname']
                filteritemrowid = request.POST['filteritemrowid']

                if filteritemname == 'projectstatus':
                        if filteritemselectedvalue == 'open':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'closed':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'quoteddocdetailsid':
                        if filteritemselectedvalue == 'hasnotvalue':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'hasvalue':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'quoteddocnumber':
                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                if filteritemname == 'activityname':
                    cursor4 = connections['redmine'].cursor()
                    cursor4 = connection.cursor()
                    cursor4.execute(
                        "SELECT id, name FROM enumerations WHERE type = 'TimeEntryActivity'")
                    activities = cursor4.fetchall()

                    if filteritemselectedvalue == 'is':

                            return render(request, 'quotation/filteritemtemplateselect.html', {'filteritemfirstinputboxselectoptions': activities,
                                                                                               'filteritemrowid': filteritemrowid})

                    if filteritemselectedvalue == 'isnot':

                            return render(request, 'quotation/filteritemtemplateselect.html', {'filteritemfirstinputboxselectoptions': activities,
                                                                                               'filteritemrowid': filteritemrowid})

                    if filteritemselectedvalue == 'none':

                            return render(request, 'quotation/filteritemtemplateempty.html', {})

                    if filteritemselectedvalue == 'any':

                            return render(request, 'quotation/filteritemtemplateempty.html', {})

                if filteritemname == 'datespenton':
                        if filteritemselectedvalue == 'between':

                                return render(request, 'quotation/filteritemtemplatebetweeninputbox.html', {'filteritemrowid': filteritemrowid, 'filteritemname': filteritemname})

                if filteritemname == 'timeentryid':
                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid, 'filteritemname': filteritemname})

                if filteritemname == 'projectid':
                    if searchphraseformainresults == 'a': # timeentrysearchtemplate does not contain  searchphraseformainresults
                        searchphraseformainresults = 'and projects.name is not null'
                    cursor23 = connections['redmine'].cursor()
                    cursor23.execute("SELECT "
                                     "projects.id, "
                                     "projects.name "

                                     "FROM time_entries as T "

                                     "LEFT JOIN custom_values as quoteddocdetailsidtable "
                                     "ON T.id = quoteddocdetailsidtable.customized_id and quoteddocdetailsidtable.custom_field_id = 4 "

                                     "LEFT JOIN custom_values as quoteddocnumbertable "
                                     "ON T.id = quoteddocnumbertable.customized_id and quoteddocnumbertable.custom_field_id = 6 "

                                     "JOIN projects "
                                     "ON T.project_id = projects.id "

                                     "JOIN enumerations "
                                     "ON T.activity_id = enumerations.id "

                                     "JOIN users "
                                     "ON T.user_id = users.id "

                                     "WHERE T.id is not null " + searchphraseformainresults + " "

                                     "GROUP BY projects.id, "
                                     "         projects.name ")
                    projectnamerowsources = cursor23.fetchall()

                    if filteritemselectedvalue == 'is':

                        return render(request, 'quotation/filteritemtemplateselect.html',
                                      {'filteritemfirstinputboxselectoptions': projectnamerowsources,
                                       'filteritemrowid': filteritemrowid})

                if filteritemname == 'userid':
                    if searchphraseformainresults == 'a': # timeentrysearchtemplate does not contain  searchphraseformainresults
                        searchphraseformainresults = 'and users.firstname is not null'
                    cursor23 = connections['redmine'].cursor()
                    cursor23.execute("SELECT "
                                     "users.id, "
                                     "CONCAT(users.firstname, ' ', users.lastname) AS username "

                                     "FROM time_entries as T "

                                     "LEFT JOIN custom_values as quoteddocdetailsidtable "
                                     "ON T.id = quoteddocdetailsidtable.customized_id and quoteddocdetailsidtable.custom_field_id = 4 "

                                     "LEFT JOIN custom_values as quoteddocnumbertable "
                                     "ON T.id = quoteddocnumbertable.customized_id and quoteddocnumbertable.custom_field_id = 6 "

                                     "JOIN projects "
                                     "ON T.project_id = projects.id "

                                     "JOIN enumerations "
                                     "ON T.activity_id = enumerations.id "

                                     "JOIN users "
                                     "ON T.user_id = users.id "

                                     "WHERE T.id is not null " + searchphraseformainresults + " "

                                     "GROUP BY users.id, "
                                     "         username ")
                    usernamerowsources = cursor23.fetchall()

                    if filteritemselectedvalue == 'is':

                        return render(request, 'quotation/filteritemtemplateselect.html',
                                      {'filteritemfirstinputboxselectoptions': usernamerowsources,
                                       'filteritemrowid': filteritemrowid})

        if invokedfrom == 'addfilterselectchanged': # when we want to search first click the #Add Filter selectbox and add some filteritems to html
                filteritemrowid = request.POST['filteritemmaxrowid']
                selectedvalue = request.POST['selectedvalue']
                selectedoption = request.POST['selectedoption'] # name which appears for user


                if selectedvalue == 'projectstatus': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 2;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'projectstatus' #attribute for elements

                    filteritemselectoptions[0][0] = 'open' #for inner use
                    filteritemselectoptions[0][1] = 'open' #for the user to show

                    filteritemselectoptions[1][0] = 'closed'
                    filteritemselectoptions[1][1] = "closed"

                if selectedvalue == 'quoteddocdetailsid': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 2;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'quoteddocdetailsid' #attribute for elements

                    filteritemselectoptions[0][0] = 'hasnotvalue' #for inner use
                    filteritemselectoptions[0][1] = 'has not value' #for the user to show

                    filteritemselectoptions[1][0] = 'hasvalue'
                    filteritemselectoptions[1][1] = "has value"

                if selectedvalue == 'quoteddocnumber': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'quoteddocnumber' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                if selectedvalue == 'activityname': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'activityname' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                    filteritemselectoptions[1][0] = 'isnot'
                    filteritemselectoptions[1][1] = "is not"

                    filteritemselectoptions[2][0] = 'none'
                    filteritemselectoptions[2][1] = 'none'

                    filteritemselectoptions[3][0] = 'any'
                    filteritemselectoptions[3][1] = 'any'


                    filteritemselectoptions[0][0] = 'is' #for inner use
                    filteritemselectoptions[0][1] = 'is' #for the user to show

                if selectedvalue == 'datespenton': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'datespenton' #attribute for elements

                    filteritemselectoptions[0][0] = 'between'
                    filteritemselectoptions[0][1] = 'between'

                if selectedvalue == 'timeentryid': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'timeentryid' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                if selectedvalue == 'projectid': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'projectid' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                if selectedvalue == 'userid': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'userid' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

        return render(request, 'quotation/filtertemplatehtml.html',{'selectedoption': selectedoption,
                                                                    'filteritemrowid': filteritemrowid,
                                                                    'filteritemname': filteritemname,
                                                                    'filteritemselectoptions': filteritemselectoptions})
def filtertemplatehtmlontimemanagerform(request):
        invokedfrom = request.POST['invokedfrom']
        searchphraseformainresults = request.POST['searchphraseformainresults'] # 'a' when searchstring is empty
        #import pdb;
        #pdb.set_trace()

        if invokedfrom == 'filteritemselectchanged': # when we want change a filteritems on html (clicking the selectbox on filteritem)
                filteritemselectedvalue = request.POST['filteritemselectedvalue']
                filteritemname = request.POST['filteritemname']
                filteritemrowid = request.POST['filteritemrowid']

                if filteritemname == 'timedoneid':
                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                if filteritemname == 'projectid':
                    if searchphraseformainresults == 'a': # timeentrysearchtemplate does not contain  searchphraseformainresults
                        searchphraseformainresults = 'and name_tblprojects_redmine_ctbltimedone is not null'
                    cursor23 = connection.cursor()
                    cursor23.execute("SELECT "
                                     "projectid_tbltimedone as projectid, "
                                     "name_tblprojects_redmine_ctbltimedone as projectname "

                                     "FROM quotation_tbltimedone "

                                     "WHERE projectid_tbltimedone is not null  " + searchphraseformainresults + " "

                                     "GROUP BY projectid, "
                                     "         projectname ")
                    projectnamerowsources = cursor23.fetchall()

                    if filteritemselectedvalue == 'is':

                        return render(request, 'quotation/filteritemtemplateselect.html',
                                      {'filteritemfirstinputboxselectoptions': projectnamerowsources,
                                       'filteritemrowid': filteritemrowid})

                if filteritemname == 'datespenton':
                        if filteritemselectedvalue == 'between':

                                return render(request, 'quotation/filteritemtemplatebetweeninputbox.html', {'filteritemrowid': filteritemrowid, 'filteritemname': filteritemname})

                        if filteritemselectedvalue == 'today':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'yesterday':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'lessthandaysago':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                if filteritemname == 'timeentryid':
                        if filteritemselectedvalue == 'hasnotvalue':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'hasvalue':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                if filteritemname == 'uploadingtimestamp':
                        if filteritemselectedvalue == 'between':

                                return render(request, 'quotation/filteritemtemplatebetweeninputbox.html', {'filteritemrowid': filteritemrowid, 'filteritemname': filteritemname})

                        if filteritemselectedvalue == 'today':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'yesterday':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'lessthandaysago':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid})

                if filteritemname == 'rowenabledformanager':
                        if filteritemselectedvalue == 'enabled':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

                        if filteritemselectedvalue == 'notenabled':

                                return render(request, 'quotation/filteritemtemplateempty.html', {})

        if invokedfrom == 'addfilterselectchanged': # when we want to search first click the #Add Filter selectbox and add some filteritems to html
                filteritemrowid = request.POST['filteritemmaxrowid']
                selectedvalue = request.POST['selectedvalue']
                selectedoption = request.POST['selectedoption'] # name which appears for user


                if selectedvalue == 'projectid': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'projectid' #attribute for elements

                    filteritemselectoptions[0][0] = 'is' #for inner use
                    filteritemselectoptions[0][1] = 'is' #for the user to show

                if selectedvalue == 'timedoneid': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'timedoneid' #attribute for elements

                    filteritemselectoptions[0][0] = 'is'
                    filteritemselectoptions[0][1] = 'is'

                if selectedvalue == 'datespenton': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'datespenton' #attribute for elements

                    filteritemselectoptions[0][0] = 'today'
                    filteritemselectoptions[0][1] = 'today'

                    filteritemselectoptions[1][0] = 'yesterday'
                    filteritemselectoptions[1][1] = 'yesterday'

                    filteritemselectoptions[2][0] = 'between'
                    filteritemselectoptions[2][1] = 'between'

                    filteritemselectoptions[3][0] = 'lessthandaysago'
                    filteritemselectoptions[3][1] = 'less than days ago'

                if selectedvalue == 'timeentryid':

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 3;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'timeentryid' #attribute for elements

                    filteritemselectoptions[0][0] = 'hasnotvalue' #for inner use
                    filteritemselectoptions[0][1] = 'has not value' #for the user to show

                    filteritemselectoptions[1][0] = 'hasvalue'
                    filteritemselectoptions[1][1] = "has value"

                    filteritemselectoptions[2][0] = 'is'
                    filteritemselectoptions[2][1] = 'is'

                if selectedvalue == 'uploadingtimestamp': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 4;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'uploadingtimestamp' #attribute for elements

                    filteritemselectoptions[0][0] = 'today'
                    filteritemselectoptions[0][1] = 'today'

                    filteritemselectoptions[1][0] = 'yesterday'
                    filteritemselectoptions[1][1] = 'yesterday'

                    filteritemselectoptions[2][0] = 'between'
                    filteritemselectoptions[2][1] = 'between'

                    filteritemselectoptions[3][0] = 'lessthandaysago'
                    filteritemselectoptions[3][1] = 'less than days ago'

                if selectedvalue == 'rowenabledformanager':

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 2;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'rowenabledformanager' #attribute for elements

                    filteritemselectoptions[0][0] = 'enabled' #for inner use
                    filteritemselectoptions[0][1] = 'enabled' #for the user to show

                    filteritemselectoptions[1][0] = 'notenabled'
                    filteritemselectoptions[1][1] = "not enabled"

        return render(request, 'quotation/filtertemplatehtml.html',{'selectedoption': selectedoption,
                                                                    'filteritemrowid': filteritemrowid,
                                                                    'filteritemname': filteritemname,
                                                                    'filteritemselectoptions': filteritemselectoptions})
def filtertemplatehtmlonpurchaseorderpreform(request):
        invokedfrom = request.POST['invokedfrom']
        searchphraseformainresults = request.POST['searchphraseformainresults'] # 'a' when searchstring is empty
        #import pdb;
        #pdb.set_trace()

        if invokedfrom == 'filteritemselectchanged': # when we want change a filteritems on html (clicking the selectbox on filteritem)
                filteritemselectedvalue = request.POST['filteritemselectedvalue']
                filteritemname = request.POST['filteritemname']
                filteritemrowid = request.POST['filteritemrowid']

                if filteritemname == 'dateofcorcreation':
                        if filteritemselectedvalue == 'between':

                                return render(request, 'quotation/filteritemtemplatebetweeninputbox.html', {'filteritemrowid': filteritemrowid, 'filteritemname': filteritemname})
                if filteritemname == 'docnumber':
                        if filteritemselectedvalue == 'is':

                                return render(request, 'quotation/filteritemtemplateinputbox.html', {'filteritemrowid': filteritemrowid, 'filteritemname': filteritemname})

        if invokedfrom == 'addfilterselectchanged': # when we want to search first click the #Add Filter selectbox and add some filteritems to html
                filteritemrowid = request.POST['filteritemmaxrowid']
                selectedvalue = request.POST['selectedvalue']
                selectedoption = request.POST['selectedoption'] # name which appears for user

                if selectedvalue == 'dateofcorcreation': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'dateofcorcreation' #attribute for elements

                    filteritemselectoptions[0][0] = 'between'
                    filteritemselectoptions[0][1] = 'between'


                if selectedvalue == 'docnumber': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'docnumber' #attribute for elements

                    filteritemselectoptions[0][0] = 'is' #for inner use
                    filteritemselectoptions[0][1] = 'is' #for the user to show

        return render(request, 'quotation/filtertemplatehtml.html',{'selectedoption': selectedoption,
                                                                    'filteritemrowid': filteritemrowid,
                                                                    'filteritemname': filteritemname,
                                                                    'filteritemselectoptions': filteritemselectoptions})
