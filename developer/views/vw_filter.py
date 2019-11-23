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
def filtertemplatehtmlontimemanagerdevform(request):
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


        if invokedfrom == 'addfilterselectchanged': #  when we want to search first click the #Add Filter selectbox and add some filteritems to html
                filteritemrowid = request.POST['filteritemmaxrowid']
                selectedvalue = request.POST['selectedvalue']
                selectedoption = request.POST['selectedoption'] # name which appears for user


                if selectedvalue == 'projectid': # here the value is text without space and small letter i.e. customerdescription

                    # Creates a  list containing #h lists, each of #w items, all set to 0
                    w, h = 2, 1;
                    filteritemselectoptions = [[0 for x in range(w)] for y in range(h)]

                    filteritemname = 'projectid' # attribute for elements

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

                    filteritemselectoptions[0][0] = 'notenabled' #for inner use
                    filteritemselectoptions[0][1] = 'not enabled' #for the user to show

                    filteritemselectoptions[1][0] = 'enabled'
                    filteritemselectoptions[1][1] = "enabled"


        return render(request, 'quotation/filtertemplatehtml.html',{'selectedoption': selectedoption,
                                                                    'filteritemrowid': filteritemrowid,
                                                                    'filteritemname': filteritemname,
                                                                    'filteritemselectoptions': filteritemselectoptions})
