# coding: utf-8
import logging

from . import ADMIN_CONFIGURERS
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import redirect
from core.utils import import_symbol
from django.conf import settings


logger = logging.getLogger('konkord')


@staff_member_required
def config_index(request):
    return HttpResponseRedirect(
        reverse('admin_config_form', args=('core',)))


@staff_member_required
def restart_engine(request, config):
    from .utils import restart_engine
    restart_engine()
    return HttpResponseRedirect(
        reverse('admin_config_form', args=(config,)))


@staff_member_required
def config_form(request, config_group, template='adminconfig/index.html'):
    config_groups = [(x[0], x[1]) for x in ADMIN_CONFIGURERS]
    config_class = [x[2] for x in ADMIN_CONFIGURERS if x[0] == config_group]
    if len(config_class) > 0:
        if len(config_class) > 1:
            logger.warning(
                u'More than one config group "%(c_group)s" found.'
                u'Only first is taken.' % {
                    'c_group': config_group,
                })
        config_class = config_class[0]
    else:
        raise Http404

    try:
        config_class = import_symbol(config_class)
        configurer = config_class()
        configurer.load_data()

        form_class = configurer.get_form()
        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_multipart():
                form = form_class(request.POST, request.FILES)

            if form.is_valid():
                configurer.load_data_from_form(form.cleaned_data)
                configurer.handle_files(request.FILES)
                configurer.save_data()
                messages.success(
                    request, _(u'Configuration saved successfully.'))
            return redirect(request.path)
        else:
            form = form_class(initial=configurer.get_initial_data_for_form())
    except AttributeError as e:
        form = None
        logger.error(
            u'Cannot generate the config form for admin: %s' % str(e))
        if settings.DEBUG:
            raise  e

    return render(request, template, {
        'config_groups': config_groups,
        'active_group': config_group,
        'form': form,
    })
