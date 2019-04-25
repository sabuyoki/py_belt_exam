from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import random,bcrypt
from datetime import datetime
from .models import *

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if 'status' not in request.session:
        request.session['status'] = ''
    errors = User.objects.regi_validator(request.POST)
    if errors:
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request,'index.html')
    else:
        User.objects.create(first_name=request.POST['fname'],
        last_name=request.POST['lname'],
        email_address=request.POST['email'],
        pass_word=bcrypt.hashpw(request.POST['pass_word'].encode(), bcrypt.gensalt()))
        id = str(User.objects.last().id)
        context = {'quotes': Quote.objects.all()}
        request.session['status'] = 'registered'
        request.session['rid'] = id
        request.session['name'] = str(request.POST['fname']) + " " + str(request.POST['lname'])
        return render(request, 'wall.html', context)

def login(request):
    if 'status' not in request.session:
        request.session['status'] = ''
    errors = LogManager.log_validator(request.POST)
    if errors:
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request,'index.html')
    else:
        user = User.objects.get(email_address = request.POST['email'])
        if bcrypt.checkpw(request.POST['pass_word'].encode(), user.pass_word.encode()):
            context = {'quotes': Quote.objects.all()}
            request.session['status'] = 'logged in'
            request.session['rid'] = user.id
            request.session['name'] = str(user.first_name) + " " + str(user.last_name)
            return render(request, 'wall.html', context)
        else:
            messages.error(request, 'Your password failed')
            request.session.clear()
            return render(request,'index.html')

def quote_post(request):
    if 'rid' in request.session:
        errors = Quote.objects.quote_validator(request.POST)
        if errors:
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                context = {'user': User.objects.filter(id=int(request.session['rid']))}
                return render(request, 'wall.html', context)
        else:
            Quote.objects.create(author=request.POST['author'], quotes=request.POST['quote'], quoted_by=User.objects.get(id=int(request.session['rid'])))
            context = {'quotes': Quote.objects.all()}
            return render(request, 'wall.html', context)
    return redirect('/clear')

def quote_list(request):
    context = {'quotes': Quote.objects.all()}
    return render(request, 'wall.html', context)

def quote_user_list(request, id):
    context = {'quotes': Quote.objects.filter(quoted_by=id)}
    return render(request, 'list.html', context)

def edit_user(request):
    context = {'user': User.objects.filter(id=int(request.session['rid']))}
    return render(request, 'edit.html', context)

def update_user(request):
    errors = User.objects.user_edit_validator(request.POST)
    if errors:
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            context = {'user': User.objects.filter(id=int(request.session['rid']))}
            return render(request, 'edit.html', context)
    else:
        user_to_update = User.objects.get(id=int(request.session['rid']))	
        user_to_update.first_name = request.POST['fname']
        user_to_update.last_name = request.POST['lname']
        user_to_update.email_address = request.POST['email']
        user_to_update.save()
        request.session['name'] = str(request.POST['fname']) + " " + str(request.POST['lname'])
        return redirect('/quote_list')

def delete(request, id):
    quote_to_delete = Quote.objects.get(id=id)	
    quote_to_delete.delete()
    context = {'quotes': Quote.objects.all()}
    return redirect('/quote_list')

def clear(request):
    request.session.clear()
    return redirect('/')

def like_quote(request, id):
    quote_like_by = User.objects.get(id=int(request.session['rid']))
    quote_to_like = Quote.objects.get(id=id)
    quote_to_like.liked_by.add(quote_like_by)
    quote_like_by.liked_quotes.add(quote_to_like)
    
    context = {'quotes': Quote.objects.all()}
    return redirect('/quote_list', context)
