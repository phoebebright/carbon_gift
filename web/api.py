# tastypie doesn't like doing orm posts, see https://groups.google.com/forum/#!topic/django-tastypie/BoU5tsQZWOo

from tastypie import fields
from tastypie.resources import Resource, ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import SessionAuthentication, Authentication, BasicAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization, ReadOnlyAuthorization
from tastypie.exceptions import NotFound, BadRequest
from tastypie.paginator import Paginator

from web.models import *


from django.contrib.auth import get_user_model
User = get_user_model()

from django.http import Http404
from django.utils.timesince import timesince
from django.contrib.humanize.templatetags.humanize import naturalday
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.core.exceptions import ValidationError

from tastypie.bundle import Bundle

from datetime import date, datetime, time


class GMDAuthentication(Authentication):
    pass

class GMDAuthorization(Authorization):
    # for resources with user, only permit access to records for current user

    def __init__(self, owner=None, *args, **kwargs):
        self.owner = owner


    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # if this is a user resource check whole object
        if bundle.obj == bundle.request.user:
            return True
        else:
            return bundle.obj.user == bundle.request.user

class UserPendingPoints(ModelResource):

    class Meta:
        queryset = Points.objects.filter(pending=True)
        include_resource_uri = False
        resource_name = 'user_pending_points'
        allowed_methods = ['get']
        filtering = {
            'user_id': ('exact',),
        }

        authorization = GMDAuthorization()
        authentication = GMDAuthentication()

    def dehydrate(self, bundle):
        bundle.data['created_date'] = timesince(bundle.obj.created)
        bundle.data['name'] = bundle.obj.object.name
        bundle.data['points'] = 2
        return bundle
