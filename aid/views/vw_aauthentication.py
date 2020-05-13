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

from django.contrib.auth import login, authenticate
from aid.forms import SignUpForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from aid.forms import SignUpForm
from aid.token import account_activation_token

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from aid.token import account_activation_token
from django.core.mail import EmailMessage

# import pdb;
# pdb.set_trace()
def aauthenticationsignup(request):
        if request.method == 'POST':
                form = SignUpForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    subject = 'Activate Your Aid Account'
                    message = render_to_string('aid/aaccount_activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                        subject, message, 'szluka.mate@gmail.com',
                        [user.email])  # , cc=[cc])
                    email.content_subtype = "html"
                    email.send()
                    return HttpResponseNotFound('account_activation_sent')
        else:
                form = SignUpForm()
        return render(request, 'aid/aauthenticationsignup.html', {'form': form})

def aauthenticationactivate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True

        cursor1 = connection.cursor()
        cursor1.execute(
            "UPDATE auth_user SET "
            "email_confirmedflag_tblauth_user='1' "
            "WHERE id = %s ", [user.id])
        user.save()
        login(request, user)
        return redirect('aorderprocess')
    else:
        return HttpResponseNotFound('account_activation_invalid')
