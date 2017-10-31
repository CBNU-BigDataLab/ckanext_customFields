#encoding: utf-8

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class CustomFieldsPlugin(plugins.SingletonPlugin,
    toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IFacets)

    def dataset_facets(self, facets_dict, package_type):
	#facets_dict['num_resources'] = toolkit._('Number of Resources')
	facets_dict['language'] = toolkit._('Languages')
        facets_dict['dataset_format'] = 'Dataset Format'
        facets_dict['topic'] = 'Topic'
       
	return facets_dict
    def organization_facets(self, facets_dict, organization_type, package_type):
        facets_dict['language'] = toolkit._('Languages')
        facets_dict['dataset_format'] = 'Dataset Format'
        facets_dict['topic'] = 'Topic'
        return facets_dict

    def _modify_package_schema(self, schema):
	# Our custom field
        schema.update({
		'language': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')],
        })

        schema.update({
		'dataset_format': [toolkit.get_validator('ignore_missing'),
				   toolkit.get_converter('convert_to_extras')],
        })  

        schema.update({
                'topic': [toolkit.get_validator('ignore_missing'),
                          toolkit.get_converter('convert_to_extras')],
        })

				
	return schema

    def create_package_schema(self):
	# Get default schema
	schema = super(CustomFieldsPlugin, self).create_package_schema()
	schema = self._modify_package_schema(schema)
	return schema

    def update_package_schema(self):
        # Get default schema
        schema = super(CustomFieldsPlugin, self).update_package_schema()
	schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        # Get default schema
        schema = super(CustomFieldsPlugin, self).show_package_schema()
        # Our custom field
        schema.update({
                'language': [toolkit.get_converter('convert_from_extras'),
				toolkit.get_validator('ignore_missing')],
        })

        schema.update({
		'dataset_format': [toolkit.get_converter('convert_from_extras'),
                                toolkit.get_validator('ignore_missing')],
        })
        schema.update({
                'topic': [toolkit.get_converter('convert_from_extras'),
                          toolkit.get_validator('ignore_missing')],
        })

        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
    
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')
