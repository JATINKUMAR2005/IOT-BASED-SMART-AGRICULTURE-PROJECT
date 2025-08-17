from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.



def checksession(request):
    if "login_id" in request.session:
        user_id = request.session["login_id"]
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
    else:
        user = None

    context = {
        "user": user,
    }
    return context

def message_notify(request):
    latest_messages = ContactMessage.objects.all()
    latest_complaints = Complaint.objects.all()

    # Create a new context dictionary
    context = {
        "unread_messages": latest_messages.count(),  # Count all messages
        "unread_complaints": latest_complaints.count(),  # Count all complaints
        "latest_messages": latest_messages,
        "latest_complaints": latest_complaints,
    }

    return context


#################################################    ADMIN PART     ######################################################################
def home(request):
    context = checksession(request)
    context.update(message_notify(request))
    contacts = ContactMessage.objects.all()

    users = User.objects.filter(role="user")  # Only fetch users with role='user'
    total_users = users.count()
    total_sensors = users.count()*5

    context["contacts"] = contacts
    context["users"] = users  # Pass filtered users to template
    context["total_users"] = total_users
    context["total_sensors"] = total_sensors

    return render(request, "admin/adminindex.html", context)

def Login (request):
    return render(request,"admin/signin.html")

def SignUp (request):
    return render(request,"admin/signup.html")

def profile(request):
    context = checksession(request)
    context.update(message_notify(request))
    return render(request, "admin/profile.html",context)

def IR_sensor (request):
    context = checksession(request)
    context.update(message_notify(request))
    return render(request,"admin/IR sensor.html",context)

def WL_sensor (request):
    context = checksession(request)
    context.update(message_notify(request))
    return render(request,"admin/WL sensor.html",context)

def Flame_sensor (request):
    context = checksession(request)
    context.update(message_notify(request))
    return render(request,"admin/Flame sensor.html",context)

def Soil_sensor (request):
    context = checksession(request)
    context.update(message_notify(request))
    return render(request,"admin/Soil sensor.html",context)

def Smoke_sensor (request):
    context = checksession(request)
    context.update(message_notify(request))
    return render(request,"admin/Smoke sensor.html",context)


def register_user(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        role = "admin"
        phone = request.POST.get("phone")
        profile = request.FILES.get("profile")
        gender = request.POST.get("gender")

        print(username)
        print(email)
        print(password)
        print(first_name)
        print(last_name)
        print(role)
        print(phone)
        print(profile)
        print(gender)

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print("This Account Already Exists")
            return redirect(SignUp)

            # Create and save the new user
        insertuser = User(
        username = username,
        email=email,
        password=password,
        First_name=first_name,
        Last_name=last_name,
        role=role,
        phone=phone,
        profile=profile,
        gender=gender,
        )
        insertuser.save()
        print("Registration Successful")
        return redirect(Login)

    return render(request, "admin/signup.html")

def view_users(request):
    context = checksession(request)
    context.update(message_notify(request))
    users = User.objects.filter(role="user")
    context["users"] = users
    return render(request, "admin/view_user.html", context)

def edit_profile(request):
    context = checksession(request)
    context.update(message_notify(request))
    users = User.objects.filter(role="admin")
    context["users"] = users
    return render(request, "admin/edit_profile.html", context)


def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id, role="user")  # Only delete regular users
        user.delete()
        print("User deleted successfully")
    except:
        print("User does not exist")
    return redirect(view_users)


def delete_admin(request, user_id):
    try:
        user = User.objects.get(id=user_id, role="admin")  # Only delete regular users
        user.delete()
        print("User deleted successfully")
    except:
        print("User does not exist")
    return redirect(edit_profile)


def checkuser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = "admin"

        print(email)
        print(password)

        try:
            userdata = User.objects.get(email=email,password=password,role=role)
            request.session["login_id"] = userdata.id
            request.session["login_name"] = userdata.username
            request.session["login_email"] = userdata.email
            request.session["login_role"] = userdata.role
            request.session.save()
            print("Login Successful")
            return redirect(home)
        except:
            print("Invalid Details")
            pass
    return render(request, "admin/signin.html")

def logout(request):
    try:
        del request.session["login_id"]
        del request.session["login_name"]
        del request.session["login_email"]
        del request.session["login_role"]
        print("Logout Successful")
        return redirect(Login)
    except :
        pass

def manage_contact(request):
    context = checksession(request)
    context.update(message_notify(request))
    contacts = ContactMessage.objects.all()  # Fetch all contact messages
    context["contacts"] = contacts
    return render(request, "admin/manage_contact.html", context)

def complaint(request):
    context = checksession(request)
    context.update(message_notify(request))
    complaints = Complaint.objects.all().order_by("-created_at")
    context["complaints"] = complaints
    return render(request, "admin/Complaint.html", context)

def delete_contact(request, manage_contact_id):
    try:
        contactdata = ContactMessage.objects.get(id=manage_contact_id)
        contactdata.delete()
        print("Contact Message Deleted Successful")
        return redirect(manage_contact)
    except:
        pass
    return redirect(manage_contact)

def delete_complaint(request, complaint_id):
    try:
        complaintdata = Complaint.objects.get(id=complaint_id)
        complaintdata.delete()
        print("Complaint Deleted Successful")
        return redirect(complaint)
    except:
        pass
    return redirect("complaint")

def resolve_complaint(request, complaint_id):
    try:
        complaintdata = Complaint.objects.get(id=complaint_id)
        complaintdata.status = "Success"  # ✅ Mark as resolved
        complaintdata.save()
        print("Complaint marked as resolved.")
    except Complaint.DoesNotExist:
        print("Complaint not found.")
    return redirect(complaint)






#################################################    USER PART     ######################################################################

def userlogin(request):
    return render(request, "USER/login.html")

def sensor(request):
    return render(request, "USER/sensors.html")

def usersignup(request):
    return render(request, "USER/signup.html")

def userhome(request):
    return render(request, "USER/userindex.html")

def userabout(request):
    return render(request, "USER/about.html")

def usercontact(request):
    return render(request, "USER/contact.html")

def userfeature(request):
    return render(request, "USER/feature.html")

def userproject(request):
    return render(request, "USER/project.html")

def usercomplaint(request):
    return render(request, "USER/complaint.html")

def userservice(request):
    return render(request, "USER/service.html")

def userflamesensor(request):
    fire_sensors = FireLevelSensor.objects.all()
    context = {
        'fire_sensors':fire_sensors
    }
    return render(request, "USER/User Flame sensor.html",context)

def userirsensor(request):
    ir_sensors = IRSensor.objects.all()
    context = {
        'ir_sensors':ir_sensors
    }
    return render(request, "USER/User IR sensor.html",context)

def usersmokesensor(request):
    smoke_sensors = SmokeSensor.objects.all()
    context = {
        'smoke_sensors': smoke_sensors
    }
    return render(request, "USER/User Smoke sensor.html",context)

def usersoilsensor(request):
    soil_sensors = SoilMoistureSensor.objects.all()
    context = {
        'soil_sensors': soil_sensors
    }
    return render(request, "USER/User Soil sensor.html",context)

def userwlsensor(request):
    water_sensors = WaterLevelSensor.objects.all().order_by('-timestamp')
    context = {
        'water_sensors': water_sensors
    }
    return render(request, "USER/User WL sensor.html",context)


def register_Customer(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        role = "user"
        phone = request.POST.get("phone")
        profile = request.FILES.get("profile")
        gender = request.POST.get("gender")

        print(username)
        print(email)
        print(password)
        print(first_name)
        print(last_name)
        print(role)
        print(phone)
        print(profile)
        print(gender)

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            print("This Account Already Exists")
            return redirect(usersignup)

        try:
            # Create and save the new user
            insertuser = User(
                username = username,
                email=email,
                password=password,
                First_name=first_name,
                Last_name=last_name,
                role=role,
                phone=phone,
                profile=profile,
                gender=gender,
            )
            insertuser.save()
            print("Registration Successful")
            return redirect('/')

        except:
            print("Error occurred:")
            pass
    return render(request, "USER/signup.html")

def check_Customer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = "user"

        try:
            userdata = User.objects.get(email=email,password=password,role=role)
            request.session["login_id"] = userdata.id
            request.session["login_name"] = userdata.username
            request.session["login_email"] = userdata.email
            request.session["login_role"] = userdata.role
            print("Login Successful")
            return redirect(userhome)
        except:
            print("Invalid Details")
            pass
    return render(request, "USER/login.html")


def clear_logout(request):
    try:
        del request.session["login_id"]
        del request.session["login_name"]
        del request.session["login_email"]
        del request.session["login_role"]
        print("Logout Successful")
        return redirect(userhome)
    except :
        pass

def contact_view(request):
    uid = request.session["login_id"]
    if request.method == "POST":
        # Capturing form values into variables
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(name)
        print(email)
        print(subject)
        print(message)

        # Save to database
        insertcontact = ContactMessage(user_id=User(id=uid),name=name, email=email, subject=subject, message=message)
        insertcontact.save()

        print ("Message sent successfully!")

    return render(request, "USER/contact.html")  # Render the form for GET requests


def complaint_form(request):
    uid = request.session.get("login_id")  # Get logged-in user ID

    if not uid:
        print("Please log in first.")
        return redirect("login")  # Redirect if not logged in

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("message")

        # Ensure the user exists
        try:
            user_instance = User.objects.get(id=uid)
        except User.DoesNotExist:
            print("User does not exist.")
            return redirect("login")

        # Save the complaint to the database
        Complaint.objects.create(user_id=user_instance, name=name, email=email, mobile=mobile, message=message)
        print("Complaint submitted successfully.")

        return redirect(complaints_userside)  # Redirect to complaint page

    # Fetch all complaints and render the page
    complaints = Complaint.objects.all().order_by("-created_at")
    return render(request, "USER/complaint.html", {"complaints": complaints})

def complaints_userside(request):
    context = checksession(request)
    complaintss = Complaint.objects.all().order_by("-created_at")
    context["complaints"] = complaintss
    return render(request, "USER/view_complaint.html", context)

def live_sensor_data(request):
    try:
        latest_water = WaterLevelSensor.objects.latest('timestamp')
        latest_soil = SoilMoistureSensor.objects.latest('timestamp')
        latest_ir = IRSensor.objects.latest('timestamp')
        latest_smoke = SmokeSensor.objects.latest('timestamp')
        latest_fire = FireLevelSensor.objects.latest('timestamp')

        data = {
            'water_level': latest_water.level,
            'water_updated': latest_water.timestamp.strftime("%Y-%m-%d %H:%M:%S"),

            'soil_moisture': latest_soil.moisture_percent,
            'soil_updated': latest_soil.timestamp.strftime("%Y-%m-%d %H:%M:%S"),

            'ir_status': latest_ir.value,
            'ir_updated': latest_ir.timestamp.strftime("%Y-%m-%d %H:%M:%S"),

            'smoke_status': latest_smoke.ppm,
            'smoke_updated': latest_smoke.timestamp.strftime("%Y-%m-%d %H:%M:%S"),

            'fire_status': latest_fire.level,
            'fire_updated': latest_fire.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=200)