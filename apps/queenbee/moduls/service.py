from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.utils import label_for_field
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import admin
import traceback, logging, json

from apps.cms.models import Service
from apps.cms.forms import ServiceForm
from apps.queenbee.permissions import permission_required