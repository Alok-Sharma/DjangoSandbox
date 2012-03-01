from django.shortcuts import render_to_response
#from django_sandbox.forms import LoginForm
#from django.contrib import auth
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django_sandbox.forms import DetailsForm,RegisterForm,ChangePassForm
from django.contrib.auth.models import User
from django.contrib import auth

def redirect_profile(request):
    if request.user.username:
        return HttpResponseRedirect('/accounts/profile/'+request.user.username)
    else:
        return HttpResponseRedirect('/accounts/login/')

def profile_view(request,url_user):
#    if request.user.is_authenticated():
#        return render_to_response('post_login.html',{'user':request.user,'viewer':request.user},context_instance=RequestContext(request))
#    else:
#        user=User.objects.get(username=url_user)
#        return render_to_response('post_login.html',{'user':user,'viewer':request.user},context_instance=RequestContext(request))
#    return HttpResponseRedirect('/accounts/register')
    if url_user:
        user=User.objects.get(username=url_user)
        all_users=User.objects.all()
        return render_to_response('post_login.html',{'user':user,'viewer':request.user,'all_users':all_users},context_instance=RequestContext(request))


def edit_details(request):
    if request.user.is_authenticated():
        if request.method=='POST':
            form=DetailsForm(request.POST)
            if form.is_valid():
                cd=form.cleaned_data
                request.user.first_name=cd['first_name']
                request.user.last_name=cd['last_name']
                request.user.email=cd['email']
                request.user.save()
                return HttpResponseRedirect('/accounts/profile/')
        else:
            pre_firstname=request.user.first_name
            pre_lastname=request.user.last_name
            pre_email=request.user.email
            pre_password=request.user.password
            data={'first_name':pre_firstname,'last_name':pre_lastname,'email':pre_email,'password1':pre_password,'password2':pre_password}
            form=DetailsForm(data)
        return render_to_response('edit_details.html',{'form':form},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/accounts/login')
    
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            userr=User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            userr.first_name=cd['first_name']
            userr.last_name=cd['last_name']
            userr.save()
            user=auth.authenticate(username=cd['username'],password=cd['password1'])
            auth.login(request, user)
            return HttpResponseRedirect('/accounts/profile')
    else:
        form=RegisterForm()
    return render_to_response('registration/register.html',{'form':form},context_instance=RequestContext(request))

def change_pass(request):
    if request.user.is_authenticated():
        if request.method=='POST':
            form=ChangePassForm(request.POST)
            if form.is_valid():
                cd=form.cleaned_data
                if request.user.check_password(cd['old_password']):
                    request.user.set_password(cd['new_password'])
                    request.user.save()
                    return HttpResponseRedirect('/accounts/profile')
                else:
                    err=1
                    form=ChangePassForm()
                    return render_to_response('edit_details.html',{'err':err,'form':form},context_instance=RequestContext(request))
        else:
            form=ChangePassForm()
        return render_to_response('edit_details.html',{'form':form},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/accounts/login')
        
