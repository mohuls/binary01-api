from django.http import JsonResponse, response
import json
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.forms.models import model_to_dict
from django.core import serializers
from .models import *

from django.shortcuts import render

def room(request):
    return render(request, 'api/room.html', {
        'room_name': 'binary01'
    })

@csrf_exempt
def login(request):
  response = 0

  if request.method == 'POST':
    body = request.body.decode('utf-8')
    data = json.loads(body)
    username=data['username']
    password=data['password']
    if username and password:
      user = authenticate(username=username, password=password)
      if user is not None:
          response = 1
          return JsonResponse({'response': response, 'username': username, 'password': password})
  return JsonResponse({'response': response})

@csrf_exempt
def signup(request):
  response = 0

  if request.method == 'POST':
    body = request.body.decode('utf-8')
    data = json.loads(body)
    email = data['email']
    username=data['username']
    password=data['password']

    if email and username and password:
      if User.objects.filter(email=email).first() is not None:
        response = 1
      else:
        if User.objects.filter(username=username).first() is not None:
          response = 2
        else:
            User.objects.create_user(username, email, password)
            response = 3
            return JsonResponse({'response': response, 'username': username, 'password': password})

  return JsonResponse({'response': response})

@csrf_exempt
def send_msg(request):
  response = 0
  if request.method == 'POST':
    body = request.body.decode('utf-8')
    data = json.loads(body)
    username = data['username']
    message=data['message']

    if username and message:
      user= User.objects.filter(username=username).first()
      
      if user:
        response = 1
        Chat.objects.create(user=user, message=message)
        return JsonResponse({'response': response, 'username': username, 'message': message})

  return JsonResponse({'response': response})


@csrf_exempt
def get_msg(request):
  chat = Chat.objects.all().values()[:20]

  data = {
    'messages': list(chat)
  }
  return JsonResponse(data, safe=False)


@csrf_exempt
def mining_data(request):
  response = 0

  if request.method == 'POST':
    body = request.body.decode('utf-8')
    data = json.loads(body)
    username = data['username']
    password = data['password']
    tokens=data['tokens']
    time=data['time']

    if username and password and tokens and time:
      user = authenticate(username=username, password=password)

      if user is not None:
        user.profile.token = user.profile.token + tokens
        user.profile.mining_time = user.profile.mining_time + time
        user.save()
        response = 1
  return JsonResponse({'response': response})

@csrf_exempt
def get_mining_data(request):
  response = 0

  if request.method == 'POST':
    body = request.body.decode('utf-8')
    data = json.loads(body)
    username = data['username']
    password = data['password']

    if username and password:
      user = authenticate(username=username, password=password)

      if user is not None:
        response = 1
        total_token = user.profile.token
        total_time = user.profile.mining_time
        return JsonResponse({'response': response, 'total_token': total_token, 'total_time': total_time})
  return JsonResponse({'response': response})

@csrf_exempt
def get_user_data(request):
  response = 0
  if request.method == 'POST':
    body = request.body.decode('utf-8')
    data = json.loads(body)
    username = data['username']
    password = data['password']

    if username and password:
      user = authenticate(username=username, password=password)

      if user is not None:
        response = 1
        usrname = user.username
        name = user.first_name
        email = user.email
        token = user.profile.token
        return JsonResponse({'response': response, 'username': usrname,  'name': name, 'email': email, 'token': token})
  return JsonResponse({'response': response})


@csrf_exempt
def airdrop_add_token(request):
  response = 0
  if request.method == 'POST':
    body = request.body.decode('utf-8')
    data = json.loads(body)
    username = data['username']
    password = data['password']

    if username and password:
      user = authenticate(username=username, password=password)

      if user is not None:
        response = 1
        user.profile.token = user.profile.token + 10
        user.save()
        
  return JsonResponse({'response': response})
