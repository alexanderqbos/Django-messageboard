import json

from django.db.models.query import QuerySet
from msgserver.models import Message

#
# PURPOSE:
# Class instanced to reflect a custom JSON encoder for the Message model.
#
# PARAMETERS:
# json.JSONEncoder - required for the class to function as a cls field
#
# NOTES:
# uses single method default to override the native json encoder method
#
class MessageEncoder(json.JSONEncoder):
    #
    # PURPOSE:
    # Take in a list casted queryset from a Message model instance and
    # return a dictionary of the values to be encoded.
    #
    # PARAMETERS:
    # self - a reference to this class, no other methods or values exist
    #        so not very important.
    # obj - the object we are encoding into a dictionary.
    #
    # RETURN/SIDE EFFECTS:
    # Returns a dictionary of the values from the list.
    #
    # NOTES:
    # Use isinstance to compare if the list object passed through is from
    # the Message Model.
    #
    def default(self, obj):
        if isinstance(obj, Message):
            return { 'id': obj.id, 'key': obj.key, 'message': obj.message }
        return json.JSONEncoder.default(self, obj)