import ckanext.colorado.helpers as helpers
import pkgutil
import inspect
import os
import logging

from flask import Blueprint

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.lib.plugins import DefaultTranslation


log = logging.getLogger(__name__)


def _register_blueprints():
    u'''Return all blueprints defined in the `views` folder
    '''
    blueprints = []

    def is_blueprint(mm):
        return isinstance(mm, Blueprint)

    path = os.path.join(os.path.dirname(__file__), 'views')

    for loader, name, _ in pkgutil.iter_modules([path]):
        module = loader.find_module(name).load_module(name)
        for blueprint in inspect.getmembers(module, is_blueprint):
            blueprints.append(blueprint[1])
            log.debug(u'Registered blueprint: {0!r}'.format(blueprint[0]))
    return blueprints


class ColoradoPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'colorado')

    # IBlueprint
    
    def get_blueprint(self):
        return _register_blueprints()

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "get_user_types": helpers.get_user_types,
            "get_expertise": helpers.get_expertise,
            "get_insurance_types": helpers.get_insurance_types,
            "get_job_preferences": helpers.get_job_preferences,
        }
