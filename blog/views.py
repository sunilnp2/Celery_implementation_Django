

# Create your views here.

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from blog.models import *
from blog.forms import *
from django.contrib import auth
from datetime import datetime
from typing import Protocol
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from celery import shared_task
from django.core.mail import send_mail

# Create your views here.

class BaseView(View):
    views = {}

class HomeView(BaseView):
    def get(self,request):
        self.views['blogs'] = Blog.objects.all()
        return render(request, 'index.html', self.views)

# # class TodoView(BaseView):
#     login_required = True
#     def get(self, request):
#         self.views['date'] = datetime.now()
#         username = request.user.username
#         self.views['todos'] = Todo_List.objects.filter(username = username)
#         return render(request, 'todo.html', self.views)

#     def post(self,request):
#         username = request.user.username
#         user = request.user
#         todo = request.POST['todo']

#         if not todo:
#             messages.error(request, 'input field is required')
#             return redirect('list:todo')
#         if user is None:
#             messages.error(request, "You are not registered yet")
#             return redirect('list:signup')

#         list = Todo_List.objects.create(
#                 username = username,
#                 title = todo
#                 )
#         list.save()
#         messages.success(request, "New todo created successfully")
#         return redirect('list:todo')

   


def signup(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    else:
        if request.method == "POST":
            fm = SignupForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, "You are registered successfully")
                return redirect('blog:login')
        else:
            fm = SignupForm()
        return render(request, 'signup.html',{'form':fm})
        

    # return render(request, 'signup.html' {'form':fm})


def login(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    
    else:
        if request.method == "POST":
            # fm = AuthenticationForm()
            fm = AuthenticationForm(request = request ,data = request.POST)
            if fm.is_valid():
                username = fm.cleaned_data['username']
                pw = fm.cleaned_data['password']
                user = auth.authenticate(username = username, password = pw)
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, "You are login successfully")
                    return redirect('blog:home')
        else:
                fm = AuthenticationForm()
        return render(request,'login.html', {'form':fm})

def profile(request):
    user = request.user
    if user.is_authenticated:
     return render(request, 'profile.html')
    else:
        return redirect('blog:home')




def logout(request):
    auth.logout(request)
    return redirect('blog:home')


@shared_task
def send_email(request,title, user, to_email):
    title = title
    mail_subject = f'{user} add a new blog'
    message = render_to_string("show-email.html", {
        'user': user.username,
        'title':title,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    send_mail(mail_subject, message, 'nepalisun22@gmail.com', to_email)
    # if email.send():
    #     messages.success(request, "Email has been send to users email")
    # else:
    #     messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

@login_required
@shared_task
def add(request):
    user_email = []
    email = User.objects.all()
    for e in email:
        user_email.append(e.email)
    print(user_email)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            blog = form.cleaned_data['blog']
            add = form.cleaned_data['add_by']
            image = form.cleaned_data['image']
            obj = Blog.objects.create(title = title, blog = blog, add_by = add, image = image)
            obj.save()
            send_email(request,title, add, user_email)
            messages.success(request, "Blog added successfully")
            return redirect('blog:home')
    else:
        form = BlogForm()
    return render(request, "add_blog.html", {'form':form})


def del_blog(request, pk):
    id = pk
    blog = Blog.objects.get(pk = id)
    blog.delete()
    messages.success(request, "Blog Delete Sucessfully")
    return redirect('blog:home')





