from django.shortcuts import render
from .forms import AddEmpForm
from django.conf import settings

#Authentication Imports
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.oauth2.credentials

from django.http import HttpResponseRedirect

#to post to the server
import requests
import json

#to enable transfer over http
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#Email Encodeing Lib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import mimetypes
import base64

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


scope=[
'https://www.googleapis.com/auth/gmail.compose',
'https://www.googleapis.com/auth/plus.profile.language.read',
'https://www.googleapis.com/auth/gmail.send',
'https://www.googleapis.com/auth/userinfo.profile',
'https://www.googleapis.com/auth/gmail.modify',
'https://www.googleapis.com/auth/admin.directory.user',
'https://www.googleapis.com/auth/plus.me',
'https://mail.google.com/',
'https://www.googleapis.com/auth/plus.profile.agerange.read',]

def GoogleAuth(request):
    global scope
    #Tell it the Client credentials & Type of Request(scope)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=scope)
    #Redirect after Authentications
    flow.redirect_uri = settings.DOMAIN + '/FinishAuth/'
    authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')
    return HttpResponseRedirect(authorization_url)

#defining credentials Globaly
credi={}

#Auth part 2
def GetAuthToken(request):
    #capture the Auth code
    code = request.GET.get('code', '')
    state = request.GET.get('state', '')
    global scope
    #The Request
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=scope,
    state=state)
    flow.redirect_uri = settings.DOMAIN + '/FinishAuth/'
    authorization_response = request.get_full_path()
    #Exchange Auth code for Access Key
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    global credi
    credi = credentials_to_dict(credentials)
    return HttpResponseRedirect(settings.DOMAIN + '/AddEmp/')

def create_message(to,subject,message_text):
    message = MIMEText(message_text,'html')
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode())}


#Function to Create Email with Image
def create_message_with_image(to, subject, message_text,file):
  message = MIMEMultipart()
  message['to'] = to
  message['subject'] = subject
  msg = MIMEText(message_text,'html')
  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file.name)
  main_type, sub_type = content_type.split('/', 1)

  if main_type == 'image':
    fp = file
    msg = MIMEImage(fp.read(), _subtype=sub_type)

  msg.add_header('Content-Disposition', 'inline')
  msg.add_header('Content-ID','<renewbuy_logo>')
  message.attach(msg)
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode())}


def RenderPage(request):
    if request.method == 'POST':
        form = AddEmpForm(request.POST, request.FILES)
        #Setting Required Parameters
        header ={
                    'Authorization':'Bearer '+credi['token'],
                    'Accept':'application/json',
                    'Content-Type':'application/json',
                    }
        UserUrl='https://www.googleapis.com/gmail/v1/users/me/messages/send'
        #compile Data

        #testing mail
        file=request.FILES['photo']
        """
        to_test='krishna.gupta@renewbuy.com'
        subject_test='Hey'
        message_text_test=''
        raw_test= create_message(to_test,subject_test,message_text_test)
        #send Data
        response = requests.post(UserUrl,data='{"raw":"'+raw_test['raw'].decode("utf-8")+'"}',headers=header)
        """
        if(form['sendEmailReq'].value()):
            to='krishna.gupta@renewbuy.com'
            subject='Please Create an Email of the Following Employee'
            message_text='''
            <table style="table-layout:fixed;width:100%;border-collapse: collapse;">
              <tbody>
                <tr>
                  <th style="width:30%;border: 1px solid black;">Name</th>
                  <th style="width:40%;border: 1px solid black;">Personal Email ID</th>
                  <th style="width:10%;border: 1px solid black;">@</th>
                </tr>
                <tr>
                    <td style="border: 1px solid black;">'''+form['first_name'].value()+' '+form['last_name'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['pemail'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['domain'].value()+'''</td>
                </tr>
              </tbody>
            </table>
            '''
            raw = create_message(to,subject,message_text)
            respo = requests.post(UserUrl,data='{"raw":"'+raw['raw'].decode("utf-8")+'"}',headers=header)

        if(form['sendIdCarReq'].value()):
            to='krishna.gupta@renewbuy.com'
            subject='Please Create an ID of the Following Employee'
            message_text='''
            <table style="table-layout:fixed;width:100%;border-collapse: collapse;">
              <tbody>
                <tr>
                  <th style="width:15%;border: 1px solid black;">Employee Name</th>
                  <th style="width:10%;border: 1px solid black;">Blood Group</th>
                  <th style="width:10%;border: 1px solid black;">Maritial Status</th>
                  <th style="width:15%;border: 1px solid black;">Date of Birth</th>
                  <th style="width:15%;border: 1px solid black;">Date of Joining</th>
                  <th style="width:30%;border: 1px solid black;">Designation</th>
                  <th style="width:15%;border: 1px solid black;">Location</th>
                  <th style="width:15%;border: 1px solid black;">Mobile Number</th>
                  <th style="width:35%;border: 1px solid black;">Official Email</th>
                </tr>
                <tr>
                    <td style="border: 1px solid black;">'''+form['first_name'].value()+' '+form['last_name'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['bloodGroup'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['maritialStatus'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['dateOfBirth'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['dateOfJoining'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['designation'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['locationOfJoining'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['mobileNumber'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['first_name'].value()+'.'+form['last_name'].value()+'@renewbuy'+form['domain'].value()+'''</td>
                </tr>
              </tbody>
            </table>
            '''
            raw = create_message(to,subject,message_text)
            respo = requests.post(UserUrl,data='{"raw":"'+raw['raw'].decode("utf-8")+'"}',headers=header)

        if(form['sendVisCarReq'].value()):
            to='krishna.gupta@renewbuy.com'
            subject='Please Create Visiting Cards of the Following Employee'
            message_text='''
                <table style="table-layout:fixed;width:100%;border-collapse: collapse;">
                    <tbody>
                        <tr>
                            <th style="width:15%;border: 1px solid black;">Employee Name</th>
                            <th style="width:15%;border: 1px solid black;">Designation</th>
                            <th style="width:10%;border: 1px solid black;">Mobile Number</th>
                            <th style="width:20%;border: 1px solid black;">Official Email ID</th>
                            <th style="width:5%;border: 1px solid black;">Quantity</th>
                            <th style="width:35%;border: 1px solid black;">Address</th>
                        </tr>
                        <tr>
                            <td style="border: 1px solid black;">'''+form['first_name'].value()+' '+form['last_name'].value()+'''</td>
                            <td style="border: 1px solid black;">'''+form['designation'].value()+'''</td>
                            <td style="border: 1px solid black;">'''+form['mobileNumber'].value()+'''</td>
                            <td style="border: 1px solid black;">'''+form['first_name'].value()+'.'+form['last_name'].value()+'@renewbuy'+form['domain'].value()+'''</td>
                            <td style="border: 1px solid black;">'''+form['visitingCards'].value()+'''</td>
                            <td style="border: 1px solid black;">'''+form['eAddress'].value()+'''</td>
                        </tr>
                    </tbody>
            </table>
            '''
            raw = create_message(to,subject,message_text)
            respo = requests.post(UserUrl,data='{"raw":"'+raw['raw'].decode("utf-8")+'"}',headers=header)

        if(form['sendPartCodeReq'].value()):
            to='krishna.gupta@renewbuy.com'
            subject='Please Generate Partner Code of the Following Employee'
            message_text='''
            <table style="table-layout:fixed;width:100%;border-collapse: collapse;border: 1px solid black;">
              <tbody>
                <tr>
                  <th style="width:13%;border: 1px solid black;">Name</th>
                  <th style="width:7%;border: 1px solid black;">DOJ</th>
                  <th style="width:7%;border: 1px solid black;">Company</th>
                  <th style="width:15%;border: 1px solid black;">Designation</th>
                  <th style="width:19%;border: 1px solid black;">Reporting Manager</th>
                  <th style="width:7%;border: 1px solid black;">Location</th>
                  <th style="width:7%;border: 1px solid black;">Mobile Number</th>
                  <th style="width:19%;border: 1px solid black;">Personal Email ID</th>
                  <th style="width:3%;border: 1px solid black;">Gender</th>
                  <th style="width:2%;border: 1px solid black;">@</th>
                </tr>
                <tr>
                    <td style="border: 1px solid black;">'''+form['first_name'].value()+' '+form['last_name'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['dateOfJoining'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['company'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['designation'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['reportingManager'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['locationOfJoining'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['mobileNumber'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['pemail'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['gender'].value()+'''</td>
                    <td style="border: 1px solid black;">'''+form['domain'].value()+'''</td>
                </tr>
              </tbody>
            </table>
            '''
            raw = create_message(to,subject,message_text)
            respo = requests.post(UserUrl,data='{"raw":"'+raw['raw'].decode("utf-8")+'"}',headers=header)

        if(form['sendPanIndiaConf'].value()):
            to='krishna.gupta@renewbuy.com'
            subject='Confirmation of New Employee'
            message_text=''''''
            raw = create_message(to,subject,message_text)
            respo = requests.post(UserUrl,data='{"raw":"'+raw['raw'].decode("utf-8")+'"}',headers=header)

        if(form['sendJoinWelcome'].value()):
            to='krishna.gupta@renewbuy.com'
            subject='A Warm Welcome to New Employees'
            message_text='''
            <div style="background-color: #68e3ff;">
                <span><img src="cid:renewbuy_logo" alt="Employee" height="80" width="80" style="padding:1px;border:2px solid #021a40;background-color: #f78340;"><b>
                Welcoming '''+form['first_name'].value()+' '+form['last_name'].value()+''' at ReNewBuy as a '''+form['designation'].value()+''' </b></span>
                <hr>
            </div>
            '''
            raw = create_message_with_image(to,subject,message_text,file)
            respo = requests.post(UserUrl,data='{"raw":"'+raw['raw'].decode("utf-8")+'"}',headers=header)

        return HttpResponseRedirect(settings.DOMAIN)

    else:
        form = AddEmpForm()

    return render(request,'addEmp/inputForm.html',{'form':form})
