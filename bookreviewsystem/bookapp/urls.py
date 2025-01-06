"""
URL configuration for bookreviewsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='indexPage'),
    path('log', views.loginPage),
    path('adminlog', views.adminloginPage),
    path('publisherlog', views.publisherloginPage),
    path('usersign', views.userSignupPage),
    path('publishersign', views.PublisherSignupPage),
    path('userinfo', views.adduserAction),
    path('publisherinfo', views.addpublisherAction),
    path('home', views.homepage),
    path('loginaction', views.userloginAction),
    path('logout', views.userlogoutAction),
    path('publishbook', views.Bookpublishpage),
    path('publishhome', views.publisherhomepage),
    path('adminhome', views.adminhomepage),
    path('adminlogAction', views.adminloginAction),
    path('publisherlogaction', views.publisherloginAction),
    path('addbookactn', views.addbookaction),
    path('publisherallbooks', views.publisherallbookspage, name='publisherallbooks'),
    path('booldel/<id>', views.deletebookaction),
    path('updatebook', views.updatebookaction),
    path('userallbooks', views.userallbookspage),
    path('library', views.userlibrarypage),
    path('addtolib/<int:book_id>/', views.library, name='library'),
    path('librarybookdel/<id>', views.deletefromLibrary),
    path('reviewsubaction', views.submit_review),
    path('review', views.reviewpage),
    path('adminpublisherdisp', views.adminpublisherdisplay),
    path('adminreviewdisp', views.adminreviewdisplay),
    path('adminusermanage', views.adminusermanagepage),
    path('userdel/<id>', views.userdeleteaction),
    path('adminpublishermanage', views.adminpublishermanagepage),
    path('pubdel/<id>', views.publisherdeleteaction),
    path('adminreviewmanage', views.adminreviewmanagepage),
    path('reviewdel/<id>', views.reviewdeleteaction),
    path('publisherupdate/<id>', views.publisherupdateaction),
    path('userupdate/<id>', views.userupdateaction),
    path('homeuserupd/<id>', views.homeuserupdateaction),
    path('homepublisherupd/<id>', views.homepublisherupdateaction),
    path('publisherreview', views.publisherreviewpage),
    path('adminbook', views.adminBookdisplay),
    path('adminbookmanage', views.adminbookmanage),
    path('bkdel/<id>', views.admindeletebookaction),
    path('adbookupdate/<id>', views.adminupdatebookaction),
    path('pubcopyrights', views.publishercopyrightspage),
    path('copyright/<int:id>', views.copyrightformpage),
    path('requestremoval', views.copyrightapplyaction),
    path('remreqdisp', views.removalrequestpage),
    path('reqapprove/<id>', views.requestaccept),
    path('reqreject/<id>', views.requestreject),
    path('remreqbook/<id>/<rid>', views.rembookreq),
    path('remreq/<int:id>', views.remrequest)

]
