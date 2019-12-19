import pkgutil
import inspect
import os
import logging

from flask import Blueprint
from routes.mapper import SubMapper

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckan.lib.plugins import DefaultDatasetForm

import ckanext.colorado.helpers as helpers
import ckanext.colorado.logic.action.user as user_action
from ckanext.colorado.model.user import setup as user_extra_model_setup

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


class ColoradoPlugin(plugins.SingletonPlugin, DefaultTranslation, DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'colorado')

    # IConfigurable

    def configure(self, config):
        user_extra_model_setup()

    # IBlueprint

    def get_blueprint(self):
        return _register_blueprints()

    # IActions

    def get_actions(self):
        action_functions = {
            'user_extra_create': user_action.user_extra_create,
            'user_extra_read': user_action.user_extra_read,
            'user_extra_update': user_action.user_extra_update
        }

        return action_functions

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "get_user_types": helpers.get_user_types,
            "get_expertise": helpers.get_expertise,
            "get_insurance_types": helpers.get_insurance_types,
            "get_job_preferences": helpers.get_job_preferences,
            "get_job_types": helpers.get_job_types,
            "get_job_locations": helpers.get_job_locations,
            'get_experiance_level': helpers.get_experiance_level,
            'get_salary_estimate': helpers.get_salary_estimate,
            'pretty_date': helpers.pretty_date,
            'get_recently_updated_datasets': helpers.get_recently_updated_datasets,
            'user_type': helpers.user_type,
            'expertise': helpers.expertise,
            'job_preference': helpers.job_preference,
            'experience': helpers.experience,
            'education': helpers.education,
            'insurance_type': helpers.insurance_type
        }

    # IDatasetForm
    @staticmethod
    def _modify_package_schema(schema):
        package_defaults = [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]

        schema.update({
            'job_type': package_defaults,
            'location': package_defaults,
            'experiance_level': package_defaults,
            'salary_estimate': package_defaults
        })

        return schema

    def create_package_schema(self):
        schema = super(ColoradoPlugin, self).create_package_schema()
        return ColoradoPlugin._modify_package_schema(schema)

    def update_package_schema(self):
        schema = super(ColoradoPlugin, self).update_package_schema()
        return ColoradoPlugin._modify_package_schema(schema)

    def show_package_schema(self):
        schema = super(ColoradoPlugin, self).show_package_schema()
        package_defaults = [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]

        schema.update({
            'job_type': package_defaults,
            'location': package_defaults,
            'experiance_level': package_defaults,
            'salary_estimate': package_defaults
        })

        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    # IFacets
    @staticmethod
    def _extend_search_facets(facets_dict):
        facets_dict[u'job_type'] = u'Job Type'
        facets_dict[u'location'] = u'Location'
        facets_dict[u'experiance_level'] = u'Experiance Level'
        facets_dict[u'salary_estimate'] = u'Salary Estimate'
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        return ColoradoPlugin._extend_search_facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type, package_type):
        return ColoradoPlugin._extend_search_facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        return ColoradoPlugin._extend_search_facets(facets_dict)


    # IRoutes
    def before_map(self, map):
        # Override the package search action.
        with SubMapper(
            map,
            controller='ckanext.colorado.controllers:ColoradoPackageController'
        ) as m:
            m.connect('/dataset/{action}/{id}',
                requirements=dict(action='|'.join([
                    'new_resource',
                    'history',
                    'read_ajax',
                    'history_ajax',
                    'follow',
                    'activity',
                    'groups',
                    'unfollow',
                    'delete',
                    'api_data',
                ])))

        return map
