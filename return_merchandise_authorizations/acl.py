__author__ = 'marc'
"""
ACL utilities for assigning and enforcing role-based acl
"""

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
def assign_admin(user):
    g_user = Group.objects.get(name='user')
    g_approver = Group.objects.get(name='approver')
    g_poweruser = Group.objects.get(name='poweruser')
    g_admin = Group.objects.get(name='admin')

    g_admin.user_set.add(user)
    g_approver.user_set.add(user)
    g_poweruser.user_set.add(user)
    g_user.user_set.add(user)

    user.is_staff = True
    user.is_superuser = True
    user.save()
def assign_poweruser(user):
    g_user = Group.objects.get(name='user')
    g_approver = Group.objects.get(name='approver')
    g_poweruser = Group.objects.get(name='poweruser')
    g_admin = Group.objects.get(name='admin')

    g_admin.user_set.remove(user)
    g_approver.user_set.add(user)
    g_poweruser.user_set.add(user)
    g_user.user_set.add(user)

    user.is_staff = False
    user.is_superuser = False
    user.save()
def assign_approver(user):
    g_user = Group.objects.get(name='user')
    g_approver = Group.objects.get(name='approver')
    g_poweruser = Group.objects.get(name='poweruser')
    g_admin = Group.objects.get(name='admin')

    g_admin.user_set.remove(user)
    g_approver.user_set.add(user)
    g_poweruser.user_set.remove(user)
    g_user.user_set.add(user)

    user.is_staff = False
    user.is_superuser = False
    user.save()
def assign_user(user):

    g_user = Group.objects.get(name='user')
    g_approver = Group.objects.get(name='approver')
    g_poweruser = Group.objects.get(name='poweruser')
    g_admin = Group.objects.get(name='admin')

    g_admin.user_set.remove(user)
    g_approver.user_set.remove(user)
    g_poweruser.user_set.remove(user)
    g_user.user_set.add(user)

    user.is_staff = False
    user.is_superuser = False
    user.save()
def assign_viewer(user):
    g_user = Group.objects.get(name='user')
    g_approver = Group.objects.get(name='approver')
    g_poweruser = Group.objects.get(name='poweruser')
    g_admin = Group.objects.get(name='admin')

    g_admin.user_set.remove(user)
    g_approver.user_set.remove(user)
    g_poweruser.user_set.remove(user)
    g_user.user_set.remove(user)

    user.is_staff = False
    user.is_superuser = False
    user.save()

def user_role_required_class_method(f):
        def wrap(self, request, *args, **kwargs):
            #this check the session if userid key exist, if not it will redirect to login page
            if request.user.groups.filter(name='user').exists() is False:
                    return HttpResponseRedirect(reverse('operation_not_allowed'))
            return f(self, request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap



def admin_role_required_class_method(f):
        def wrap(self, request, *args, **kwargs):
            #this check the session if userid key exist, if not it will redirect to login page
            if request.user.groups.filter(name='admin').exists() is False:
                    return HttpResponseRedirect(reverse('operation_not_allowed'))
            return f(self, request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


def user_role(u):
    """
    :return user's role or access level - user, viewer, approver, poweruser, admin
    :param u:
    :return:
    """
    if u.groups.filter(name='admin').exists() and \
        u.groups.filter(name='approver').exists() and \
        u.groups.filter(name='poweruser').exists() and \
        u.groups.filter(name='user').exists() and \
        u.is_staff and u.is_superuser:
        return ('admin')
    if u.groups.filter(name='approver').exists() and \
        u.groups.filter(name='poweruser').exists() and \
        u.groups.filter(name='user').exists():
        return ('poweruser')
    if u.groups.filter(name='approver').exists() and \
        u.groups.filter(name='user').exists():
        return ('approver')
    if u.groups.filter(name='user').exists():
        return ('user')
    if u.groups.filter(name='admin').exists() == False and \
        u.groups.filter(name='approver').exists() == False and \
        u.groups.filter(name='poweruser').exists() == False and \
        u.groups.filter(name='user').exists() == False:
        return ('viewer')

def user_role_required(f):
        def wrap(request, *args, **kwargs):
            #this check the session if userid key exist, if not it will redirect to login page
            if request.user.groups.filter(name='user').exists() is False:
                    return HttpResponseRedirect(reverse('operation_not_allowed'))
            return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap


def admin_role_required(f):
        def wrap(request, *args, **kwargs):
            #this check the session if userid key exist, if not it will redirect to login page
            if request.user.groups.filter(name='admin').exists() is False:
                    return HttpResponseRedirect(reverse('operation_not_allowed'))
            return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
