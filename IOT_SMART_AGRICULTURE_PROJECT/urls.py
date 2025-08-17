"""
URL configuration for IOT_SMART_AGRICULTURE_PROJECT project.

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
from django.conf.urls.static import static
from django.conf import settings
from AGRICULTURE_APP.views import *

urlpatterns = [
###############################################################   START ADMIN PART   ########################################################
    path('admin/', admin.site.urls),
    path('login', Login),
    path('signup', SignUp),
    path('home', home),
    path('complaint', complaint),
    path('IR_sensor', IR_sensor),
    path('WL_sensor', WL_sensor),
    path('Soil_sensor', Soil_sensor),
    path('Smoke_sensor', Smoke_sensor),
    path('Flame_sensor', Flame_sensor),
    path('register_user', register_user),
    path("view_users", view_users),
    path("edit_profile", edit_profile),
    path('delete_user/<int:user_id>/', delete_user),
    path('delete_admin/<int:user_id>/', delete_admin),
    path('checkuser', checkuser),
    path('logout', logout),
    path("manage_contact/", manage_contact),
    path("delete-contact/<int:manage_contact_id>/", delete_contact),
    path('delete-complaint/<int:complaint_id>', delete_complaint),
    path('resolve-complaint/<int:complaint_id>/', resolve_complaint),


###############################################################   END ADMIN PART   ########################################################


###############################################################   START USER PART   ########################################################

    path('',userlogin),
    path('usersignup',usersignup),
    path('userhome',userhome),
    path('profile',profile),
    path('userabout',userabout),
    path('usercontact', usercontact),
    path('userfeature',userfeature),
    path('sensor',sensor),
    path('userproject',userproject),
    path('usercomplaint',usercomplaint),
    path('userservice',userservice),

    ##SENSORS PANEL
    path('userflamesensor',userflamesensor),
    path('userirsensor',userirsensor),
    path('usersmokesensor',usersmokesensor),
    path('usersoilsensor',usersoilsensor),
    path('userwlsensor',userwlsensor),
    ##SENSORS PANEL END

    path('register_Customer',register_Customer),
    path('check_Customer',check_Customer),
    path('clear_logout',clear_logout),
    path('view_contact', contact_view),
    path("complaints", complaint_form),
    path("complaints_userside", complaints_userside),
    path('api/live-sensors/', live_sensor_data),


###############################################################   END USER PART   ########################################################


    ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)