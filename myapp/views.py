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
            package = request.POST['package']
            notification = Notification.objects.all()

            if dateOn != '' and to_date != '':
                notification = notification.filter(
                    RegDate__range=[dateOn, to_date]).order_by('-id')

            if androidid != 'NULL':
                notification = notification.filter(androidid=androidid).order_by('-id')

            if package != 'NULL':
                notification = notification.filter(package=package).order_by('-id')

            return render(request, 'index.html', {'notification': notification, 'dateOn': dateOn,
                                                  'to_date': to_date, 'androidid': androidid})

        else:
            notification = Notification.objects.order_by('-id')
            # users = RegistrationDetais.objects.all()

            ids = RegistrationDetais.objects.values_list('androidid', flat=True)
            pack = Notification.objects.values_list('package', flat=True).distinct()

            return render(request, 'index.html', {"notification": notification, 'ids': ids, 'pack': pack})
    else:
        return render(request, 'login.html')


def adminUserList(request):
    if request.method == 'POST':
        dateOn = request.POST['from_date']
        to_date = request.POST['to_date']
        phone = request.POST['phone']
        userName = request.POST['userName']
        users = RegistrationDetais.objects.all()

        if dateOn != '' and to_date != '':
            users = users.filter(
                RegDate__range=[dateOn, to_date])
        if phone != '':
            users = users.filter(phone=phone)

        if userName != '':
            users = users.filter(username=userName)

        return render(request, 'adminUserList.html', {'users': users, 'dateOn': dateOn,
                                                      'to_date': to_date, 'phone': phone,'userName':userName})
    else:
        users = RegistrationDetais.objects.all()
        return render(request, 'adminUserList.html', {'users': users})


def delete_androidid(request, id):
    Device.objects.get(androidid=id).delete()
    return redirect("adminUserList")


def user_delete_androidid(request, id):
    Device.objects.get(androidid=id).delete()
    return redirect("userdashbord")


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
                    # return redirect('home')
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
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        number = request.POST['number']
        # androidid = request.POST['androidid']
        password = request.POST['password']
        repassword = request.POST['repassword']
        date = datetime.now()

        if password == repassword:
            RegistrationDetais.objects.create(
                username=username, email=email, phone=number, password=password, date=date)
            # Device.objects.create(phone=number,androidid=androidid)
            return redirect('login')

    return render(request, 'registration.html')


def logout(request):
    if 'phone' in request.session:
        del request.session['phone']
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')


# def adddevice(request):
#     if request.method == 'POST':
#         androidid = request.POST['androidid']
#
#
#         # alldevice = Device.objects.filter(androidid=androidid)
#
#     return render(request, 'adddevice.html')
#
#
# def device(request):
#     device = Device.objects.all()
#     return render(request, 'device.html', {"device": device})


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
        # androidlist = androidlist.androidid
        # idList = androidlist.split(", ")
        try:
            users = Device.objects.get(androidid=androidid)
            users.numOfNotif += 1
            users.save()

        except:
            print("Android id is not Register by Admin")

        print("incoming data from", androidid)
        Notification.objects.create(
            RegDate=date, androidid=androidid, package=package, title=title, msg=msg, ntime=ntime)

    if request.method == 'GET':
        date = request.GET.get('date')
        # date = datetime.strptime(date, "%d/%b/%Y %H:%M %p")
        # date.strftime("%Y-%m-%d")
        # date = date.date()
        androidid = request.GET.get('androidid')
        # package = request.GET.get('package')
        package = "SMS"
        title = request.GET.get('title')
        msg = request.GET.get('msg')
        ntime = datetime.now()
        ntime.strftime("%X")
        # androidlist = androidlist.androidid
        # idList = androidlist.split(", ")
        try:
            users = Device.objects.get(androidid=androidid)
            users.numOfNotif += 1
            users.save()

        except:
            print("Android id is not Register by Admin")

        print("incoming data from", androidid)
        Notification.objects.create(
            RegDate=date, androidid=androidid, package=package, title=title, msg=msg, ntime=ntime)

    return HttpResponse("Data Added")


def addAndriodId(request, phone):
    if 'androidid' and 'phone' in request.session:
        andriodUser = RegistrationDetais.objects.get(phone=phone)
        userDetails = Device.objects.values_list('androidid', flat=True).filter(phone=phone)
        if request.method == 'POST':
            andriodid = request.POST['androidid']
            Device.objects.create(phone=phone, androidid=andriodid)

            return redirect('adminUserList')

        return render(request, 'adddevice.html', {'andriodUser': andriodUser, 'userDetails': userDetails})
    else:
        return render(request, 'login.html')


def home(request):
    if 'phone' in request.session:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')


def dashbord(request):
    if 'phone' in request.session:
        userslist = RegistrationDetais.objects.values_list("phone","username")
        # print(userslist)
        form = {}
        for i,j in userslist:
            deviceAll = list(Device.objects.values_list("numOfNotif", "androidid").filter(phone=i))

            form[i,j] = deviceAll

        print(form)

        return render(request, 'admindashbord.html', {'form': form})
    else:
        return render(request, 'login.html')


def userdashbord(request):
    if 'phone' in request.session:
        phone = request.session['phone']
        print("-----", phone)
        users = RegistrationDetais.objects.get(phone=phone)
        users_ids = Device.objects.values_list('androidid', flat=True).filter(phone=phone)
        usersId = {i: i for i in users_ids}
        # print(usersId)
        if request.method == 'POST':
            userAndroidId = request.POST['androidid']
            Device.objects.create(phone=phone, androidid=userAndroidId)
            print("Added :",userAndroidId)
        return render(request, 'home.html', {'usersId': usersId, 'users': users})
    else:
        return render(request, 'login.html')

from random import randint
import requests

def forgotpass(request):
    if request.method == 'POST':
        newpass = request.POST['newpass']
        repass = request.POST['repass']
        fotp = request.POST['fotp']
        otp1 = request.POST['passotp']
        fphone = request.POST['passphone']

        if fotp == otp1:
            if newpass==repass:
                RegistrationDetais.objects.filter(phone=fphone).update(password=newpass)
            else:
                HttpResponse("Password is not same")
        else:
            HttpResponse("Invalid OTP")
        return redirect('login')
    return render(request, 'forgotpassword.html')

def otpgenerator(request):
    if request.method == 'POST':
        mobNum = request.POST['fphone']
        otp = randint(10000, 99999)
        print(otp)
        url = "http://quicksms.highspeedsms.com/sendsms/sendsms.php?username=BREbonrix&password=sales55&type=TEXT&sender=BONRIX&mobile={0}&message=Your%20OTP%20for%20login%20verification%20is%20:=%20{1}".format(
            mobNum, otp)
        print(mobNum)
        requests.get(url)
        return render(request,'forgotpassword.html',{'otp':otp,'mobNum':mobNum})
    return render(request, 'generatOTP.html')

def changepass(request):
    print("hellooo")
    if 'phone' in request.session:
        phone = request.session['phone']
        oldpass = RegistrationDetais.objects.values_list("password", flat=True).filter(phone=phone)
        oldpass = list(oldpass)
        if request.method == 'POST':
            newpass = request.POST['newpass']
            repass = request.POST['repass']

            if newpass in oldpass:
                RegistrationDetais.objects.filter(phone=phone).update(password=repass)
                return redirect('userdashbord')
            else:
                return HttpResponse("Enter the Correct Password")
        return render(request, 'changepass.html')
    else:
        return render(request, 'login.html')


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


# from django.db.models import Q
def demo(request):
    if 'phone' in request.session:
        # androidid = request.session['androidid']

        phone = request.session['phone']
        androidlist = Device.objects.values_list('androidid', flat=True).filter(phone=phone)
        packlist = Notification.objects.values_list('package', flat=True).filter(androidid__in=androidlist)

        notif = Notification.objects.filter(androidid__in=androidlist)
        if request.method == 'POST':
            dateOn = request.POST['from_date']
            to_date = request.POST['to_date']
            androidid = request.POST['androidid']
            package = request.POST['package']

            if dateOn != '' and to_date != '':
                notif = notif.filter(
                    RegDate__range=[dateOn, to_date])

            if androidid != 'NULL':
                notif = Notification.objects.filter(androidid=androidid)

            if package != 'NULL':
                notif = Notification.objects.filter(package=package)

            notif = notif.order_by('-id')

            return render(request, 'demo.html', {'notif': notif, 'dateOn': dateOn,
                                                 'to_date': to_date, 'androidid': androidid})

        else:
            notif = Notification.objects.filter(androidid__in=androidlist).order_by('-id')
            ids = {i: i for i in androidlist}
            pack = {i: i for i in packlist}

        return render(request, 'demo.html', {'notif': notif, 'ids': ids, 'pack': pack})
    else:
        return render(request, 'login.html')