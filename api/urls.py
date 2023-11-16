from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema

from . import views

urlpatterns = [
    path("", GraphQLView.as_view(grapiql=True, schema=schema)),
]