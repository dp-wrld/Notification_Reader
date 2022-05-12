from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
import csv


def index(request):
    if 'androidid' and 'phone' in request.session:
        if request.method == 'POST':
            dateOn = request.POST['from_date']
            to_date = request.POST['to_date']
            androidid = request.POST['androidid']
            notification = Notification.objects.all()

            if dateOn != '' and to_date != '':
                notification = notification.filter(
                    RegDate__range=[dateOn, to_date]).order_by('-id')

            if androidid != 'NULL':
                notification = notification.filter(androidid=androidid).order_by('-id')

            return render(request, 'index.html', {'notification': notification, 'dateOn': dateOn,
                                                  'to_date': to_date, 'androidid': androidid})

        else:
            notification = Notification.objects.order_by('-id')
            users = RegistrationDetais.objects.all()
            return render(request, 'index.html', {"notification": notification, 'users': users})
    else:
        return render(request, 'login.html')

def adminUserList(request):
    if request.method == 'POST':
        dateOn = request.POST['from_date']
        to_date = request.POST['to_date']
        androidid = request.POST['androidid']
        print(dateOn, to_date, androidid)
        users = RegistrationDetais.objects.all()

        if dateOn != '' and to_date != '':
            users = users.filter(
                RegDate__range=[dateOn, to_date])
        if androidid != '':
            users = users.filter(androidid=androidid)

        return render(request, 'adminUserList.html', {'users': users, 'dateOn': dateOn,
                                                      'to_date': to_date, 'androidid': androidid})
    else:
        users = RegistrationDetais.objects.all()
        return render(request, 'adminUserList.html', {'users': users})


def adminLogin(request):
    if request.method == 'POST':
        phone = request.POST['number']
        password = request.POST['password']
        user = Login.objects.get(phone=phone)
        try:
            uid = Login.objects.get(phone=phone)
            print(uid)
            if uid:
                print(uid.phone)
                if uid.phone == phone and uid.password == password:
                    print('redirect', {'user': uid})
                    request.session['id'] = uid.id
                    request.session['phone'] = uid.phone
                    print(uid.phone)
                    #return redirect('home')
                    return render(request, 'admindashbord.html', {'uid': uid})
        except:
            message = 'Invalid Data'
            return render(request, 'login.html', {'message': message})
        print(user)
        if user:
            if user.password == password:
                return redirect('index')

    return render(request, 'adminlogin.html')


def login(request):
    if request.method == 'POST':
        phone = request.POST['number']
        password = request.POST['password']
        try:
            uid = RegistrationDetais.objects.get(phone=phone)
            print(uid)
            if uid:
                print(uid.phone)
                if uid.phone == phone and uid.password == password:
                    print('redirect', {'user': uid})
                    request.session['id'] = uid.id
                    request.session['phone'] = uid.phone
                    request.session['androidid'] = uid.androidid
                    print(uid.androidid)
                    return render(request, 'home.html', {'uid': uid})
        except:
            message = 'Email Invalid'
            return render(request, 'login.html', {'message': message})
        message = 'Email And Password Invalid'
        return render(request, 'login.html', {'message': message})

    return render(request, 'login.html')


def registration(request):
    if 'androidid' and 'phone' in request.session:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            number = request.POST['number']
            password = request.POST['password']
            repassword = request.POST['repassword']
            date = datetime.now()

            if password == repassword:
                RegistrationDetais.objects.create(
                    username=username, email=email, phone=number, password=password, date=date)
                Device.objects.create(phone=number)
                return redirect('login')

        return render(request, 'registration.html')
    else:
        return render(request,'login.html')

def logout(request):
    if 'phone' in request.session:
        del request.session['phone']
        return render(request, 'login.html')
    else:
        return render(request, 'home.html')


def adddevice(request):
    if request.method == 'POST':
        dname = request.POST['devicename']
        androidid = request.POST['androidid']
        androidid1 = request.POST['androidid']
        androidid2 = request.POST['androidid']
        phone = request.POST['phone']

        alldevice = Device.objects.filter(androidid=androidid)
        alldevice1 = Device.objects.filter(androidid1=androidid1)
        alldevice2 = Device.objects.filter(androidid2=androidid2)

        if alldevice or alldevice1 or alldevice2:
            message = "duplicate andriod id"
            return render(request, 'adddevice.html', {'message': message})
        elif alldevice != '':
            Device.objects.create(
                dname=dname, androidid=androidid, phone=phone)
            return redirect('device')
        elif alldevice1 != '':
            Device.objects.create(
                dname=dname, androidid1=androidid1, phone=phone)
            return redirect('device')
        elif alldevice2 != '':
            Device.objects.create(
                dname=dname, androidid2=androidid2, phone=phone)
            return redirect('device')


    return render(request, 'adddevice.html')


def device(request):
    device = Device.objects.all()
    return render(request, 'device.html', {"device": device})


@csrf_exempt
def adddata(request):
    if request.method == 'POST':
        date = request.POST['date']
        date = datetime.strptime(date, "%d/%b/%Y %H:%M %p")
        date.strftime("%Y-%m-%d")
        date = date.date()
        androidid = request.POST['androidid']
        package = request.POST['package']
        title = request.POST['title']
        msg = request.POST['msg']
        ntime = datetime.now()
        ntime.strftime("%X")

        users = RegistrationDetais.objects.get(androidid=androidid)
        users.ncount += 1
        users.save()
        print("incoming data")
        Notification.objects.create(
             RegDate=date, androidid=androidid, package=package, title=title, msg=msg, ntime=ntime)

    return HttpResponse("Data Added")


def addAndriodId(request, phone):

    if 'androidid' and 'phone' in request.session:
        andriodUser = RegistrationDetais.objects.get(phone=phone)
        if request.method == 'POST':
            andriodid = request.POST['androidid']

            andriodUser.androidid = andriodid
            andriodUser.save()

            return redirect('adminUserList')

        return render(request, 'adddevice.html', {'andriodUser': andriodUser})
    else:
        return render(request,'login.html')


def addAndriodId1(request, phone):
    if 'androidid' and 'phone' in request.session:
        andriodUser = RegistrationDetais.objects.get(phone=phone)
        if request.method == 'POST':
            andriodid = request.POST['androidid1']

            andriodUser.androidid1 = andriodid
            andriodUser.save()

            return redirect('adminUserList')

        return render(request, 'adddevice1.html', {'andriodUser': andriodUser})
    else:
        return render(request, 'login.html')


def addAndriodId2(request, phone):
    if 'androidid' and 'phone' in request.session:
        andriodUser = RegistrationDetais.objects.get(phone=phone)
        if request.method == 'POST':
            andriodid = request.POST['androidid2']

            andriodUser.androidid2 = andriodid
            andriodUser.save()

            return redirect('adminUserList')

        return render(request, 'adddevice2.html', {'andriodUser': andriodUser})
    else:
        return render(request, 'login.html')


def home(request):
    if 'phone' in request.session:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')


def dashbord(request):
    if 'androidid' and 'phone' in request.session:
        users = RegistrationDetais.objects.all()
        return render(request, 'admindashbord.html', {'users': users})
    else:
        return render(request,'login.html')

def userdashbord(request):
    if 'androidid' and 'phone' in request.session:
        androidid = request.session['androidid']
        users = RegistrationDetais.objects.get(androidid=androidid)
        return render(request, 'home.html', {'users': users})
    else:
        return render(request,'login.html')

def searchuser(request):
    query = request.POST['queryuser']
    queryuser = RegistrationDetais.objects.filter(username__icontains=query)
    return render(request, 'searchuser.html', {"queryuser": queryuser})
    # return HttpResponse('search is working')


def export_csv(request):
    if 'androidid' and 'phone' in request.session:
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(['RegDate', 'ntime', 'androidid',
                        'title', 'msg', 'package'])

        androidid = request.session['androidid']
        userlist = Notification.objects.filter(androidid=androidid)
        for notification in userlist.values_list('RegDate', 'ntime', 'androidid', 'title', 'msg', 'package'):
            writer.writerow(notification)

        response['Content-Disposition'] = 'attachment; filename="notification.csv"'

        return response
    else:
        return render(request, 'login.html')


def multi_delete_notification(request):
    if 'androidid' and 'phone' in request.session:
        if request.method == "POST":
            product_ids = request.POST.getlist('id[]')
            print("delete this id ----------->", product_ids)
            for id in product_ids:
                notification = Notification.objects.get(pk=id)
                notification.delete()
                print(" employe  delete this id ----------->", id)
            return redirect('')
    else:
        return render(request, 'login.html')


def all_delete_notification(request):
    if 'androidid' and 'phone' in request.session:
        if request.method == "POST":
            all_delete = Notification.objects.filter()
            all_delete.delete()
            print("All notification deleted")
            return redirect('')

    else:
        return render(request, 'login.html')

from django.db.models import Q
def demo(request):
    if 'androidid' and 'phone' in request.session:
        androidid = request.session['androidid']
        # phone = request.session['phone']
        notif = Notification.objects.filter(androidid=androidid)
        if request.method == 'POST':
            dateOn = request.POST['from_date']
            to_date = request.POST['to_date']
            androidid = request.POST['androidid']

            if dateOn != '' and to_date != '':
                notif = notif.filter(
                    RegDate__range=[dateOn, to_date])

            if androidid != 'NULL':
                notif = Notification.objects.filter(androidid=androidid)

            notif = notif.order_by('-id')

            return render(request, 'demo.html', {'notif': notif, 'dateOn': dateOn,
                                                 'to_date': to_date, 'androidid': androidid})

        else:
            notif = notif.order_by('-id')
            ids = RegistrationDetais.objects.all()
            ids = ids.filter(androidid=androidid)
            print(ids)

        return render(request, 'demo.html', {'notif': notif,'ids':ids})
    else:
        return render(request, 'login.html')