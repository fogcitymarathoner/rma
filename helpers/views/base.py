# -*- coding: utf-8 -*-
"""
helpers.views.base

A set of base view classes:
* BasePublicTemplateView -- for public views (no authentication)
* BaseAuthTemplateView -- for views restricted to authenticated user
* BaseProtectedTemplateView -- for views restricted to staff
* BaseAjaxProcessFormView -- view for ajax form submissions
* AjaxActionView - view for handling ajax requests

* created: 2013-09-25 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-09-28 kchan
"""

from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    Http404
)
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormMixin

from garage.utils import DataObject
from helpers.urlhelpers import login_url
from helpers.views.mixins import AuthMixin, JsonResponseMixin
from helpers.views.settings import RESPONSE_ERRORS



# template views
# * the following are subclasses of django's TemplateView with added
#   AuthMixin for authentication.

class BaseAuthTemplateView(AuthMixin, TemplateView):
    """
    Class for views accessible only by authenticated users.
    """

    def get(self, request, *args, **kwargs):
        """Process GET request."""
        if not self.authenticated(request):
            orig_url = request.get_full_path()
            url = login_url(orig_url=orig_url, redirect_back=True)
            return HttpResponseRedirect(url)
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)


class BasePublicTemplateView(BaseAuthTemplateView):
    """
    Base view for public pages (no authentication).
    """

    authenticate_requests = False

    def get(self, request, *args, **kwargs):
        """Process GET request."""
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class BaseProtectedTemplateView(BaseAuthTemplateView):
    """
    Class for view accessible only by staff.
    """

    def get(self, request, *args, **kwargs):
        """Process GET request."""
        if not self.user_is_staff(request):
            raise Http404
        else:
            context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


# base form views
# * the following are various subclasses of form views

class BaseAjaxProcessFormView(JsonResponseMixin, AuthMixin, FormMixin, View):
    """
    Special base class to handle ajax form submissions
    * this view does not use templates and only accepts POST requests.
    * this view does not accept GET requests (override the ``get``
      method to handle GET requests).
    * this view enforces authentication using the AuthMixin.
    * returns json response.
    """

    http_method_names = ['get', 'post', 'put', 'delete']

    # subclass must set form_class
    form_class = None

    # default error response class
    error_response_class = HttpResponseBadRequest

    # default error messages
    error_msgs = RESPONSE_ERRORS

    def get(self, request, *args, **kwargs):
        """
        Process GET request.
        * this view does not accept GET requests (POST only), so we
          return a default (400 BAD REQUEST) error.
        * subclass should override this method if you are supporting
          GET requests.

        :returns: json response
        """
        return self.error()

    def get_error_msg(self, error):
        """
        Helper method to return error messge.

        :param error: error message keyword (badrequest, forbidden, etc.)
        :returns: error message string
        """
        return self.error_msgs.get(error, "Error")

    def error(self, message=None, response=None):
        """
        Return an error response.

        :param message: error message to return in response
        :param response: response class (default: ``error_response_class``)
        :returns: json response
        """
        if not message:
            message = self.get_error_msg('badrequest')
        if not response:
            response = self.error_response_class
        return self.json_response(response, message)

    def forbidden(self, message=None):
        """
        Return an unauthorized/forbidden response.

        :param message: error message to return in response
        :returns: json response
        """
        return self.error(message=self.get_error_msg('forbidden'),
                          response=HttpResponseForbidden)

    def post(self, request, *args, **kwargs):
        """
        Process form submission.

        :returns: json response
        """
        if not self.authenticated(request):
            return self.forbidden()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def put(self, *args, **kwargs):
        """
        From django docstring for ProcessFormView:
        # PUT is a valid HTTP verb for creating (with a known URL) or editing an
        # object, note that browsers only support POST for now.
        """
        return self.post(*args, **kwargs)


class AjaxActionView(BaseAjaxProcessFormView):
    """
    Class to handle ajax form submissions
    * To use this base class, subclass and set ``form_class`` and
      override the ``get_response_data`` and/or ``form_valid`` methods
      to return the appropriate data for your frontend template js
      code.
    """

    # subclass must set form_class
    form_class = None

    def get_response_data(self, form):
        """
        Method called by ``form_valid`` to return response data.
        * subclass should override.

        :param: validated form (with cleaned_data)
        :returns: data to return in response (must be dict).
        """
        data = dict(form.cleaned_data)
        return data

    def form_valid(self, form):
        """
        Process submitted data.

        :returns: json response (200 OK with data)
        """
        result = {}
        response_data = self.get_response_data(form)
        response = HttpResponse
        result.update({
            'request_status': 0,
            'msg': 'Successful!',
            'data': response_data
        })
        return self.json_response(response, result)

    def form_invalid(self, form):
        """
        Process invalid submission.
        """
        return self.error()
