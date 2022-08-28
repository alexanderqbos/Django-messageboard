from msgserver.models import Message
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.core import exceptions

import json

from msgserver.test_forms.createMessage import CreateMessage
from msgserver.models import Message
from msgserver.test_forms.updateMessage import UpdateMessage
from msgserver.MessageEncode import MessageEncoder

#
# PURPOSE:
# View loaded at the '/get/<str::key>' url of msgserver app, used to display messages at
# the passed in key
#
# PARAMETERS:
# request - required for the view function definition
# key - the key used to filter database response
#
# RETURN/SIDE EFFECTS:
# Returns simple string in HttpResponse of <key>: <message>
#
# NOTES:
# Displays a single message and key, only function I have done proper error display...
# more error checking when I have conditions for testing.
#
def get_message(request, key):
    message = Message.objects.filter(key=str(key))
    if(len(message) == 1):
        return HttpResponse(f'{message[0].key}: {message[0].message}')
    else:
        return HttpResponse(f'No row found with key {key}')

#
# PURPOSE:
# View loaded at the '/create/' url of msgserver app, used to make new entries
# in the Message model.
#
# PARAMETERS:
# Request - required for the view function definition
#
# RETURN/SIDE EFFECTS:
# Returns a template render for the form
#
# NOTES:
# Creates the message, and is validated by the Model constraints. If the key is in use
# a message should be posted.
#
def create_message(request):
    context={}

    if request.method == 'POST':
        form = CreateMessage(request.POST)
        context.clear()
        context['form'] = form
        if form.is_valid():
            try:
                message_instance = Message.objects.create(
                    key=form.data['key'],
                    message=form.cleaned_data['message'])
                message_instance.save()
            except IntegrityError:
                context['key_error'] = True
                return render(request, 'create.html', context)

            return HttpResponseRedirect('/msgserver/')
        return render(request, 'create.html', context)
    else:
        form = CreateMessage(initial={'key': '', 'message': ''})
    context.clear()
    context['form'] = form
    return render(request, 'create.html', context)

#
# PURPOSE:
# View loaded at the '/update/<str::key>' url of msgserver app, showing a form
# for a specified key in the url
#
# PARAMETERS:
# Request - required for the view function definition
# key - the value passed into the url used to filter the database for an existing
#       value to be updated.
#
# RETURN/SIDE EFFECTS:
# Returns a rendered template using Jinja template engine.
#
# NOTES:
# No error checking for the invalid key! the update will fail but the page will load
# no matter if the key is valid, shouldn't load page if key is invalid and should 
# give an invalid key message.
#
def update_message(request, key):
    try:
        message_instance = Message.objects.get(key=str(key))
    except exceptions.ObjectDoesNotExist:
        return HttpResponse('Invalid key used')
    if request.method == 'POST':
        form = UpdateMessage(request.POST)

        if form.is_valid():
            message_instance.message = form.cleaned_data['message']
            message_instance.save()
            return HttpResponseRedirect('/msgserver/')
    else:
        form = UpdateMessage(initial={'message': message_instance.message})

    context={
        'form': form,
        'key': key
    }
    return render(request, 'update.html', context)

#
# PURPOSE:
# View loaded at the '/' url of msgserver app, generates a JSON of messages
# stored in the Message model
#
# PARAMETERS:
# Request - required for the view function definition
#
# RETURN/SIDE EFFECTS:
# Returns a HttpResponse of the json data.
#
# NOTES:
# Uses the MessageEncoded.py definition as cls value to properly encode the
# database response that is cast to a list.
#
def index(request):
    data = list(Message.objects.all()) # cast to list required for MessageEncoder classes default method.
    data = json.dumps(data, cls=MessageEncoder)
    return HttpResponse(data)
