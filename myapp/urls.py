from django.urls import path
from myapp import views
from django.contrib import admin

urlpatterns = [
    path("index", views.index, name='index'),
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("adminLogin", views.adminLogin, name='adminLogin'),
    path("adddevice", views.adddevice, name='adddevice'),
    path("logout", views.logout, name='logout'),
    path("adddata/", views.adddata, name='adddata'),
    path("demo", views.demo, name='demo'),
    path("registration", views.registration, name='registration'),
    path("adminUserList", views.adminUserList, name='adminUserList'),
    path("addAndriodId/<phone>", views.addAndriodId, name="addAndriodId"),
    path("addAndriodId1/<phone>", views.addAndriodId1, name="addAndriodId1"),
    path("addAndriodId2/<phone>", views.addAndriodId2, name="addAndriodId2"),
    path("dashbord", views.dashbord, name='dashbord'),
    path("userdashbord", views.userdashbord, name='userdashbord'),
    path("export_csv", views.export_csv, name='export_csv'),
    path("searchuser", views.searchuser, name='searchuser'),
    path("multi_delete_notification",
         views.multi_delete_notification, name='multi_delete_notification'),
    path("all_delete_notification",
         views.all_delete_notification, name='all_delete_notification'),
]
