from django.shortcuts import render, get_object_or_404, redirect
from myApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    posts = Post.objects.all()

    context = {
        'posts':posts
    }
    
    return render(request,'index.html',context)

def detail(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method == "POST":
        adet = int(request.POST["number"])
        
        if Sepet.objects.filter(car=post):
            urun = Sepet.objects.get(car=post)
            urun.adet += adet
            urun.fiyat += adet * post.fiyat
            post.stok -= adet
            urun.save()
        else:
            sepet = Sepet(car = post, user = request.user, adet=adet, fiyat=adet*post.fiyat)
            sepet.save()
            
    context={
        "post":post
    }
    return render(request,'detail.html',context)

def about(request):

    return render(request,'about.html')

def sepet(request):
    urunler = Sepet.objects.all()
    tolamfiyat = 0
    if request.method == "POST":
        adetkey = list(request.POST)[1] # number4
        adetid = adetkey[6:]
        adet = request.POST[adetkey]
        urun = Sepet.objects.get(id=adetid)
        fiyat=float(urun.fiyat) / float(urun.adet)
        print(fiyat)
        urun.adet = adet
        urun.fiyat = fiyat * float(adet)
        for i in urunler:
            tolamfiyat += i.fiyat
        
        urun.save()
        
        
    context = {
        'urunler':urunler,
        'tolamfiyat': tolamfiyat,
    }
    return render(request,'sepet.html', context)

def deleteSepet(request, id):
    urun = Sepet.objects.get(id=id)
    urun.delete()
    
    return redirect('sepet')

# USER
def userLogin(request):
    
    if request.method == "POST":
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username = username, password=password)
        
        if user is not None:
            login(request,user)
            
            return redirect('index')
        # {'email':value, 'password':value}
        print(username)
        print(password)
    
    return render(request,'users/login.html')

def userLogout(request):
    logout(request)
    
    return redirect('index')

def userRegister(request):
    
    if request.method == "POST":
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request,'users/register.html',{
                    "hata":"Aynı ada sahip kullanıcı adı var"
                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, 'users/register.html', {
                        "hata": "Email daha önce kullanılmış!"
                    })
                else:
                    # ====
                    usersave = UserSave(user=username, password=password1)
                    usersave.save()
                    # ====
                    user = User.objects.create_user(first_name=name,
                                                    last_name=surname,
                                                    email=email,
                                                    username=username,
                                                    password=password1)
                    user.save()
                    return redirect('index')
        else:
            return render(request, 'users/register.html', {
                        "hata": "password aynı değil!!"
                    })    
                
    return render(request,'users/register.html')
    
def userChangePassword(request):
    user = User.objects.get(username=request.user)
    usersave = UserSave.objects.get(user=request.user)
    
    if request.method == "POST":
        password_old = request.POST['password_old']
        password_new = request.POST['password_new']
        password_renew = request.POST['password_renew']
        if password_old == usersave.password:
            if password_new == password_renew:
                user.set_password(password_new)
                user.save()
                usersave.password = password_new
                usersave.save()
                return redirect('index')
            else:
                return render(request,'users/changepassword.html', {"hata":"Şifreler aynı değğil!!"})
        else:
            return render(request, 'users/changepassword.html', {"hata": "Eski şifre yanlış!!"})
    return render(request, 'users/changepassword.html')