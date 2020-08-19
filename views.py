from django.shortcuts import render

from numberplate import Main
from numberplate.models import RegistrationModel,ComplaintModel
from numberplate.forms import RegistrationForm, LoginForm,ComplaintForm

import datetime
import smtplib
import traceback
import sys

def registration(request):
    status = False

    if request.method == "GET":
        # Get the posted form
        registrationForm = RegistrationForm(request.GET)

        if registrationForm.is_valid():

            regModel = RegistrationModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.address = registrationForm.cleaned_data["address"]
            regModel.gender = registrationForm.cleaned_data["gender"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]
            regModel.aadharno= registrationForm.cleaned_data["aadharno"]
            regModel.vehicleno = registrationForm.cleaned_data["vehicleno"]

            user = RegistrationModel.objects.filter(username=regModel.username).first()

            if user is not None:
                status = False
            else:
                try:
                    regModel.save()
                    status = True
                except:
                    status = False
    if status:
        return render(request, 'index.html', locals())
    else:
        response = render(request, 'registration.html', {"message": "User All Ready Exist"})

    return response


def login(request):
    uname = ""
    upass = ""
    if request.method == "GET":
        # Get the posted form
        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            if uname == "admin" and upass == "admin":
                request.session['username'] = "admin"
                request.session['role'] = "admin"

                return render(request, 'adminhome.html', {})

        user = RegistrationModel.objects.filter(username=uname, password=upass).first()

        if user is not None:
            request.session['username'] = uname
            request.session['role'] = "user"
            response = render(request, 'home.html', {"username": uname})
        else:
            response = render(request, 'index.html', {"message": "Invalid Credentials"})

    return response


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})


def postComplaint(request):

    status = False
    complaintForm = ComplaintForm(request.POST, request.FILES)

    if complaintForm.is_valid():
        print("in if")
        complaintModel = ComplaintModel()
        complaintModel.vehicleno = ""
        complaintModel.photo = complaintForm.cleaned_data["photo"]
        complaintModel.complaintdate = datetime.datetime.now()
        complaintModel.description = complaintForm.cleaned_data["description"]

        try:
            print("in if path","before model")
            complaintModel.save()
            status = True
        except:
            status = False

        try:
            print("in try 2",)
            last=ComplaintModel.objects.last()
            print("image path ",str(last.photo))
            imgpath = "C:/Users/ayane/PycharmProjects/NumbePlateRecongnization1/"+str(last.photo)
            print("in if path", imgpath)

            vehicleno = Main.findVehicleNumber(imgpath)
            print("vehicle no is find")
            try:
                print("mail will be sent1")
                user = RegistrationModel.objects.get(vehicleno=vehicleno)
                print("mail will be sent2")
                sendEmail(user.email, "Your Vehicle Detected its Number is " +vehicleno)
                print("after email sent", "before model")
                print("mail is sent")
            except Exception as e:
                print("Owner is not Registred Still")
            ComplaintModel.objects.filter(id=last.id).update(vehicleno=vehicleno)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            status = False

        if status:
            print("in if 5")
            response = render(request, 'postcomplaint.html', {"message": "Complaint Posted Successfully"})
        else:
            print("in if 6")
            response = render(request, 'postcomplaint.html', {"message": "Complaint Failed"})
        return response

def viewcomplaints(request):

    complaints = []

    role=request.session['role']

    if role=="admin":
        for complaint in ComplaintModel.objects.all():
            complaint.photo = str(complaint.photo).split("/")[1]
            complaints.append(complaint)
    else:
        user = RegistrationModel.objects.get(username=request.session['username'])
        vno=user.vehicleno
        for complaint in ComplaintModel.objects.filter(vehicleno=vno):
            complaint.photo = str(complaint.photo).split("/")[1]
            complaints.append(complaint)

    return render(request, "viewcomplaints.html", {"complaints": complaints})

def deleteComplaint(request):
    if request.method == "GET":
        try:
            ComplaintModel.objects.filter(id=request.GET['id']).delete()
            status = True
        except:
            status = False

        if status:

            complaints = []

            for complaint in ComplaintModel.objects.all():
                complaint.photo = str(complaint.photo).split("/")[1]
                complaints.append(complaint)

            response = render(request, 'viewcomplaints.html', {"complaints": complaints})
        else:
            response = render(request, 'viewcomplaints.html', {"message": request.GET['id']})

    return response

def sendEmail(email, subject):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("ayanehsan@gmail.com", "12abAB@@")
    server.sendmail("ayanehsan@gmail.com", email, subject)
