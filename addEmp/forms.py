from django import forms
import datetime
Company = [('Brokerage','Brokerage'),('Consultance','Consultance')]
Department = [('IT','IT'),('Others','Others')]
Location = [('Gurgoan','Sec-32,Gurgoan'),('Banglore','Banglore')]
Domain = [('.in','.in'),('.com','.com')]
Gender = [('Male','Male'),('Female','Female'),('Others','Others')]
BloodGroup = [('A+','A+'),('B+','B+'),('AB+','AB+'),('O+','O+'),('A-','A-'),('B-','B-'),('AB-','AB-'),('O-','O-')]
MaritialStatus = [('Married','Married'),('Single','Single')]
ReportingManagers = ['vikas.sharma@renewbuy.com','krishna.gupta@renewbuy.com','bharat@renewbuy.com','udit.guta@renewbuy.com']

class DateInput(forms.DateInput):
    input_type = 'date'

class AddEmpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name',max_length=100)
    gender = forms.ChoiceField(label='Gender',choices=Gender)
    bloodGroup = forms.ChoiceField(label='Blood Group',choices=BloodGroup)
    maritialStatus = forms.ChoiceField(label='Maritial Status',choices=MaritialStatus)
    dateOfBirth = forms.DateField(label='Date of Birth',widget=DateInput())
    pemail = forms.EmailField(label=' Personal Email ID',widget=forms.TextInput(attrs={'placeholder': 'you@example.com'}))
    mobileNumber = forms.IntegerField(label='Contact Number',max_value=9999999999, min_value=1000000000)
    department = forms.ChoiceField(label='Department',choices=Department,widget=forms.RadioSelect())
    company = forms.ChoiceField(label='Company',choices=Company,widget=forms.RadioSelect())
    domain = forms.ChoiceField(label='Domain',choices=Domain,widget=forms.RadioSelect())
    designation = forms.CharField(label='Designation',max_length=100)
    reportingManager = forms.EmailField(label='Reporting Manager',max_length=100,widget=forms.TextInput(attrs={'autocomplete':'off'}))
    dateOfJoining = forms.DateField(label='Date of Joining' ,widget=DateInput(),initial=datetime.date.today)
    locationOfJoining = forms.ChoiceField(label='Location of Joining',choices=Location)
    sendEmailReq = forms.BooleanField(label='Send Official Email Request',required = False)
    sendVisCarReq = forms.BooleanField(label='Send Visiting Card Request',initial = True, required = False)
    sendIdCarReq = forms.BooleanField(label='Send ID Card Request',initial = True, required = False)
    sendPartCodeReq = forms.BooleanField(label='Send Partner Code Request',initial = True, required = False)
    sendPanIndiaConf = forms.BooleanField(label='Send Pan India Confirmation',initial = True, required = False)
    sendJoinWelcome = forms.BooleanField(label='Send New Hier Welcome',initial = True, required = False)
    photo = forms.ImageField(label='Photo')
    eAddress = forms.CharField(label='Address',max_length=200)
    visitingCards = forms.IntegerField(label='Number of Visiting Cards',max_value=1000000000000, min_value=1)
