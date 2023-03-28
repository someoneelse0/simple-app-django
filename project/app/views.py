from django.shortcuts import render,redirect,HttpResponse
from app.models import Clients
from passlib.hash import pbkdf2_sha512
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.mail import send_mail

def index(req):
    if not "user" in req.COOKIES:
        return redirect("/login")
    else:
        return render(req,"index.html")

def login(req):
    if not "user" in req.COOKIES:
        return render(req,"login.html")
    else:
        return redirect("/")

def loginn(req):
    username=req.POST["username"]
    key=req.POST["key"]
    o=Clients.objects.filter(username__icontains=username)
    oo=0
    for i in o:
        oo=pbkdf2_sha512.verify(key,i.keykey)
    if oo:
        res=redirect("/")
        res.set_cookie("user",username)
        return res
    else:
        return redirect("/login")

def logout(req):
    res=render(req,"logout.html")
    res.delete_cookie("user")
    return res

def config(req):
    if not "user" in req.COOKIES:
        return redirect("/login")
    else:
        return render(req,"config.html")

def signup(req):
    if not "user" in req.COOKIES:
        return render(req,"signup.html")
    else:
        return redirect("/")

def signupp(req):
    username=req.POST["username"]
    key=req.POST["key"]
    keyy=pbkdf2_sha512.hash(key,rounds=512000,salt=b"0t1u2v3w4x5y6z")
    if Clients.objects.create(username=username,keykey=keyy):
        res=render(req,"signupp.html")
        res.set_cookie("user",username)
        return res
    else:
        return render(req,"/signup")

def mailer(req):
    if not "user" in req.COOKIES:
        return redirect("/login")
    else:
        return render(req,"mailer.html")

def m(req):
    if not "user" in req.COOKIES:
        return redirect("/login")
    else:
        if(send_mail(req.POST["su"],req.POST["me"]+" This message was send by "+req.COOKIES["user"],req.POST["fr"],[req.POST["to"]],fail_silently=False)):
            return HttpResponse("OK");
        else:
            return HttpResponse("ERROR")


def chat(req):
    if not "user" in req.COOKIES:
        return redirect("/login")
    else:
        if req.method=="POST" and req.FILES["f"]:
            mf=req.FILES["f"]
            fs=FileSystemStorage()
            fn=fs.save(mf.name,mf)
            uploaded=fs.url(fn)
            up=fn
            return render(req,"chatt.html",{"uploaded":uploaded,"up":up})
        else:
            return render(req,"chatt.html")

def delaccper(req):
    if not "user" in req.COOKIES:
        return redirect("/login")
    else:
        c=Clients.objects.get(username=req.COOKIES["user"])
        res=render(req,"delaccper.html")
        res.delete_cookie("user")
        return res
