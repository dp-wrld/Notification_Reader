from django.urls import path
from myapp import views

urlpatterns = [
    path("index", views.index, name='index'),
    # path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("adminLogin", views.adminLogin, name='adminLogin'),
    # path("adddevice", views.adddevice, name='adddevice'),
    path("logout", views.logout, name='logout'),
    path("adddata/", views.adddata, name='adddata'),
    path("demo", views.demo, name='demo'),
    path("registration", views.registration, name='registration'),
    path("adminUserList", views.adminUserList, name='adminUserList'),
    path("addAndriodId/<phone>", views.addAndriodId, name="addAndriodId"),
    path("delete_androidid/<id>", views.delete_androidid, name="delete_androidid"),
    path("user_delete_androidid/<id>", views.user_delete_androidid, name="user_delete_androidid"),
    path("dashbord", views.dashbord, name='dashbord'),
    path("", views.userdashbord, name='userdashbord'),
    path("export_csv", views.export_csv, name='export_csv'),
    path("forgotpass", views.forgotpass, name='forgotpass'),
    path("livemessage", views.livemessage, name='livemessage'),
    path("sendDataLive", views.sendDataLive, name='sendDataLive'),
    path("forward_message", views.forward_message, name='forward_message'),
    path("forward_message_log", views.forward_message_log, name='forward_message_log'),
    path("delete_forward_url/<id>", views.delete_forward_url, name='delete_forward_url'),
    path("otpgenerator", views.otpgenerator, name='otpgenerator'),
    path("changepass", views.changepass, name='changepass'),
    path("multi_delete_notification",
         views.multi_delete_notification, name='multi_delete_notification'),
    path("all_delete_notification",
         views.all_delete_notification, name='all_delete_notification'),

]



