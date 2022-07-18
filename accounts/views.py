from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from .models import UserProfile
from products.models import Product
import re

# Create your views here.
def signin(request):

  if request.method == "POST" and "btnsignin" in request.POST:
    username = request.POST["username"]
    password = request.POST["password"]
    
    user = auth.authenticate(username=username, password=password)
    if user is not None:
      #الشرط دا علشان يعمل خروج لو قفلت المتصفح
      if "rememberme" not in request.POST:
        request.session.set_expiry(0)
      auth.login(request, user)
      # messages.success(request, "You Are Login")
    else:
      messages.error(request, "Username or password invalid")
      
    return redirect("signin")
  else:
    return render(request, 'accounts/signin.html')


def logout(request):
  if request.user.is_authenticated:
    auth.logout(request)
    return redirect('index')

def signup(request):
  
  if request.method == "POST" and "btnsignup" in request.POST:
    # variables For Fields
    fname = None
    lname = None
    adress1 = None
    adress2 = None
    country = None
    zipcode = None
    mobile = None
    email = None
    gender = None
    age = None
    username = None
    password = None
    terms = None
    is_added = None
    
    # Get Values From Form
    if "fname" in request.POST: fname = request.POST["fname"]
    else : messages.error(request, "Error in Fisrt Name")
    
    if "lname" in request.POST: lname = request.POST["lname"]
    else : messages.error(request, "Error in Last Name")
    
    if "adress1" in request.POST: adress1 = request.POST["adress1"]
    else : messages.error(request, "Error in Adress1")
    
    if "adress2" in request.POST: adress2 = request.POST["adress2"]
    else : messages.error(request, "Error in Adress2")
    
    if "country" in request.POST: country = request.POST["country"]
    else : messages.error(request, "Error in country")
    
    if "zipcode" in request.POST: zipcode = request.POST["zipcode"]
    else : messages.error(request, "Error in zipcode")
    
    if "mobile" in request.POST: mobile = request.POST["mobile"]
    else : messages.error(request, "Error in mobile")
    
    if "email" in request.POST: email = request.POST["email"]
    else : messages.error(request, "Error in Email")
    
    if "gender" in request.POST: gender = request.POST["gender"]
    else : messages.error(request, "Error in Gender")
    
    if "age" in request.POST: age = request.POST["age"]
    else : messages.error(request, "Error in Age")
    
    if "username" in request.POST: username = request.POST["username"]
    else : messages.error(request, "Error in User Name")
    
    if "password" in request.POST: password = request.POST["password"]
    else : messages.error(request, "Error in Password")
    
    if "terms" in request.POST: terms = request.POST["terms"]
    
    
    # Check if Fields is Empty
    if fname and lname and adress1 and adress2 and country and zipcode and mobile and email and gender and age and username and password:
      if terms == "on":
        # Check if username is Taken
        if User.objects.filter(username=username).exists():
          messages.error(request, "This User name Is Taken")
        else:
          # Check if Email is Taken
          if User.objects.filter(email=email).exists():
            messages.error(request, "This Email Is Taken")
          else:
            pattern = "^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"
            if re.match(pattern, email):
              # Create User
              user = User.objects.create_user(
                first_name=fname,
                last_name=lname,
                email=email,
                username=username,
                password=password,
              )
              user.save()
              # Add User Profile
              userprofile = UserProfile(
                user=user,
                adress1=adress1,
                adress2=adress2,
                country=country,
                zipcode=zipcode,
                mobile=mobile,
                )
              userprofile.save()
              
              # # clear All Fields if Success
              # fname = ""
              # lname = ""
              # adress1 = ""
              # adress2 = ""
              # country = ""
              # zipcode = ""
              # mobile = ""
              # email = ""
              # gender = ""
              # age = ""
              # username = ""
              # password = ""
              # terms = None
              
              # Success Message
              messages.success(request, "User is Created")
              is_added = True
            else:
              messages.error(request, "Email InValid")
      else:
        messages.error(request, "You Must Agree The Terms")
    else:
      messages.error(request, "Please Check Empty Fields")

    return render(request, 'accounts/signup.html', {
      "is_added": is_added,
    })
  else:
    return render(request, 'accounts/signup.html')
  

def profile(request):
  
  # الجزء دا لما هيدوس علي الزرار يهبعت التعديلات
  if request.method == "POST" and "btnsignsave" in request.POST:
    if request.user is not None and not request.user.is_anonymous:
      
      userprofile = UserProfile.objects.get(user=request.user)
      if request.POST["fname"] and request.POST["lname"] and request.POST["adress1"] and request.POST["adress2"] and request.POST["country"] and request.POST["zipcode"] and request.POST["mobile"] and request.POST["gender"] and request.POST["age"] and request.POST["email"] and request.POST["username"] and request.POST["password"]:
        
        request.user.first_name = request.POST["fname"]
        request.user.last_name = request.POST["lname"]
        userprofile.adress1 = request.POST["adress1"]
        userprofile.adress2 = request.POST["adress2"]
        userprofile.country = request.POST["country"]
        userprofile.zipcode = request.POST["zipcode"]
        userprofile.mobile = request.POST["mobile"]
        userprofile.gender = request.POST["gender"]
        userprofile.age = request.POST["age"]
        # request.user.email = request.POST["email"]
        # request.user.username = request.POST["username"]
        # دا شرط علشان لو عدلت الباسورد يروح متشفر لقاعدة البيانات وميحصلش مشكلة
        if not request.POST["password"].startswith("pbkdf2_sha256$"):
          
          request.user.set_password(request.POST["password"])
          
        request.user.save()
        userprofile.save()
        # السطر دا علشان لما نغير الباسورد مش يعمل خروج ولاكن يظل علي نفس الصفحة
        # auth.login(request, request.user)
        messages.success(request, "Your Info Was Updated")
      else:
        messages.error(request, "Please Check Your Data")
    return redirect("profile")
  else:
    # الجزء دا علشان لما ادخل علي البروفايل يجبلي بيانات المستخدم
    if request.user is not None:
      # لو اليوز موجود هبعت القيم دي لصفحة البروفايل علشان تظهرلي كقيمة للمدخلات
      context = None
      # الشرط دا لتجنب خطا مستخدم مجهول اوغير معروف
      # if not request.user.is_anonymous:
      if request.user.id != None:
        userprofile = UserProfile.objects.get(user=request.user)
        context={
          'fname': request.user.first_name,
          'lname': request.user.last_name,
          'adress1': userprofile.adress1,
          'adress2': userprofile.adress2,
          'country': userprofile.country,
          'zipcode': userprofile.zipcode,
          'mobile': userprofile.mobile,
          'gender': userprofile.gender,
          'age': userprofile.age,
          'email': request.user.email,
          'username': request.user.username,
          'password': request.user.password,
        }
      return render(request, 'accounts/profile.html', context)
    else:
      # لو اليوزر مش موجود هترجعلي الرساله اللي عملتها في صفحة البروفايل
      return redirect("profile")
    
    
# This Function To add Favorites to user
def add_fav_products(request, id):
  # add id to request علشان انا عاوز اجيب رقم المنتج
  if request.user.is_authenticated and not request.user.is_anonymous:
    # التحقق من المنتج موجود في المفضلة ام لا
    prod_fav_id = Product.objects.get(id=id)
    if UserProfile.objects.filter(user=request.user, fav_products=prod_fav_id).exists():
      messages.error(request, "the product Exists Now")
    else:
    # اضافة امنتج للمفضلة لو مش موجود 
      userprofile = UserProfile.objects.get(user=request.user)
      userprofile.fav_products.add(prod_fav_id)
      messages.success(request, "Product Have in Favorietes")
    
  else:
    # لو مش مسجل دخول يبقي ملوش مفضلة 
    messages.error(request, "You Must Be Login")
  # التوجية لما تستدعيها علي صفحة المنتج الواحد
  return redirect('/products/details/'+ str(id))


# To render The Favorites Products
def favorites(request):
  context= None
  if request.user.is_authenticated and not request.user.is_anonymous:
    userinfo = UserProfile.objects.get(user=request.user)
    user_fav_products = userinfo.fav_products.all()
    context = {
      # ليه products علشان انا عامل في صفحة برودكتس لوب علي برودكتس
      'products': user_fav_products,
    }
  return render(request, 'products/products.html', context)