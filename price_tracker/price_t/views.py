from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse 
# from django.contrib.auth  import authenticate,  login
from django.contrib.auth.models import User, auth
from price_t.models import Products
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup as bs
from django.views.decorators.cache import never_cache

data=[]
email=""

from django.core.mail import send_mail

subject = 'HTML Email from Django'
message = 'This is a test HTML email sent from Django.'
from_email = 'dpkgtm12@gmail.com'
recipient_list = ['noreply.dpkgtm12@example.com']
html_message = '<p>This is an <strong>HTML</strong> email.</p>'

@never_cache
def home(request):
    # send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    if 'name' in request.session:
        return render(request,"after_login.html")
    print("YES")
    return render(request,"home.html")

@csrf_exempt
def register(request):
    if 'name' in request.session:
            return render(request,"after_login.html")
    if request.method == "POST": 
        name = request.POST.get("name","default")
        email = request.POST.get("email","default")
        password = request.POST.get("password","default")
        if User.objects.filter(email = email).exists():
            return "User already exists"
        else:
            user=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            user.save()
            return redirect(login)
    if 'name' in request.session:
        del request.session['name']
        auth.logout(request)
    return render(request,"register.html")

@csrf_exempt
@never_cache
def login(request):
    if request.method == "POST":
        username=request.POST.get("username","default")
        password=request.POST.get("password","default")
        user=auth.authenticate(username=username,password=password)
        if user is None:
            return  HttpResponse("Invalid username or password")
        else:
            auth.login(request,user)
            d={"x":user.first_name}
            global email
            request.session['username'] = username
            request.session['name'] = user.first_name
            email=username
            # print(request.session.name)
            return render(request,"after_login.html")
    if 'name' in request.session:
        del request.session['name']
        auth.logout(request)
    return redirect(home)

def logout(request):
    del request.session['name']
    auth.logout(request)
    return redirect(home)

def scrap_details(ur):
    url=requests.get(ur)
    soup=bs(url.text)
    price=0
    img_url=""
    pro_name=""
    #ScrapPrice
    elements=soup.find("div",class_="_2c7YLP UtUXW0 _6t1WkM _3HqJxg")
    if elements:
        a=elements.find("div",class_="_1YokD2 _2GoDe3")
        if a:
            b=a.find("div",class_="_1YokD2 _3Mn1Gg col-8-12")
            if b:
                c=b.find("div",class_="aMaAEs")
                if c:
                    d=c.find("div",class_="dyC4hf")
                    if d:
                        e=d.find("div",class_="_25b18c")
                        if e:
                            f=e.find("div",class_="_30jeq3 _16Jk6d")
                            # print(f.text)
                            price=float("".join(f.text[1:].split(",")))
    #Scrap Image
    elements = soup.find("div", class_="_2c7YLP UtUXW0 _6t1WkM _3HqJxg")
    if elements:
        a = elements.find("div", class_="_1YokD2 _2GoDe3")
        if a:
            b = a.find("div", class_="_1YokD2 _3Mn1Gg col-5-12 _78xt5Y")
            if b:
                c = b.find("div", class_="_1AtVbE col-12-12")
                if c:
                    d = c.find("div", class_="_1iyjIJ")
                    if d:
                        e = d.find("div", class_="_3li7GG")
                        if e:
                            f = e.find("div", class_="_1BweB8")
                            if f:
                                g=f.find("div", class_="_3kidJX")
                                
                                if g:
                                        i=g.find("img")
                                        # print(i)
                                        img_url=i["src"].replace("/0/0","/714/857")

    elements = soup.find("div", class_="_2c7YLP UtUXW0 _6t1WkM _3HqJxg")
    if elements:
            a = elements.find("div", class_="_1YokD2 _2GoDe3")
            if a:
                b = a.find("div", class_="_1YokD2 _3Mn1Gg col-8-12")
                if b:
                    c = b.find("div", class_="aMaAEs")
                    if c:
                        d = c.find("h1", class_="yhB1nd")
                        
                        if d:
                            e = d.find("span", class_="B_NuCI")
                            # print(e.text)
                            pro_name = e.text
    return price,img_url,pro_name

def add_product(request):
    global data
    if request.method == "POST":
        pro_url=request.POST.get("url")
        if pro_url=="":
            return render(request,"after_login.html")
        x=list(scrap_details(pro_url))
        x.append(pro_url)
        data=dict(zip(["price","img_url","pro_name","product_url"],x))
        return render(request,"add.html",data)
    return redirect(home)

def add(request):
    if request.method == "POST":
        x=Products(product_name=data["pro_name"],product_url=data["product_url"],product_price=data["price"],email=request.session["username"])
        x.save()
        return redirect(home)
    return redirect(home)


def show_products(request):
    if request.method == "POST":
        products = Products.objects.filter(email=email)
        l=[]
        for i in products:
            pro_url=i.product_url
            x=list(scrap_details(pro_url))
            data=dict(zip(["price","img_url","name"],x))
            l.append(data)
        return render(request, "show_product.html",{'products': l})
    else:
        return redirect(home) 


def delete_product(request):
    if request.method == "POST":
        products = Products.objects.filter(email=request.session["username"])
        l=[]
        for i in products:
            pro_url=i.product_url
            x=list(scrap_details(pro_url))
            data=dict(zip(["price","img_url","name"],x))
            data['id']=i.id
            l.append(data)
        return render(request, "delete_product.html",{'products': l})
    else:
        return redirect(home) 
    
def delete(request,id):
    member = Products.objects.get(id=id)
    member.delete()
    return redirect(delete_product)

def contact(request):
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")
  
# conn.close()