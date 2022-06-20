import argparse
from copy import copy
from functools import partial
from pathlib import Path
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy import delete
from sqlalchemy.exc import OperationalError

from langworld_db_data.langworld_db_data.filetools.csv_xls import read_csv
from langworld_db_data.langworld_db_data.constants.paths import (
    FEATURE_PROFILES_DIR,
    FILE_WITH_CATEGORIES,
    FILE_WITH_COUNTRIES,
    FILE_WITH_DOCULECTS,
    FILE_WITH_ENCYCLOPEDIA_VOLUMES,
    FILE_WITH_LISTED_VALUES,
    FILE_WITH_NAMES_OF_FEATURES,
    FILE_WITH_VALUE_TYPES,
)

from .. import models


class CustomModelInitializer:
    """Class that I created (not Cookiecutter) for (re-)populating
    the database.
    
    Deletes all data from SQL database, then populates it again
    with data from data files imported from main data repository. 
    
    I put the functionality in the separate class 
    to make the distinction between generated and custom code clear, 
    to create separate methods for separate tasks, and to enable testing.
    """

    def __init__(
        self,
        dbsession,
        dir_with_feature_profiles: Path = FEATURE_PROFILES_DIR,
        file_with_categories: Path = FILE_WITH_CATEGORIES,
        file_with_countries: Path = FILE_WITH_COUNTRIES,
        file_with_doculects: Path = FILE_WITH_DOCULECTS,
        file_with_encyclopedia_volumes: Path = FILE_WITH_ENCYCLOPEDIA_VOLUMES,
        file_with_listed_values: Path = FILE_WITH_LISTED_VALUES,
        file_with_names_of_features: Path = FILE_WITH_NAMES_OF_FEATURES,
        file_with_value_types: Path = FILE_WITH_VALUE_TYPES,
    ):
        self.dbsession = dbsession

        self.read_file = partial(read_csv, read_as='dicts')

        self.dir_with_feature_profiles = dir_with_feature_profiles
        self.file_with_categories = file_with_categories
        self.file_with_countries = file_with_countries
        self.file_with_doculects = file_with_doculects
        self.file_with_encyclopedia_volumes = file_with_encyclopedia_volumes
        self.file_with_listed_values = file_with_listed_values
        self.file_with_names_of_features = file_with_names_of_features
        self.file_with_value_types = file_with_value_types

        # Dictionaries map identifiers to instances of mapped classes:

        self.country_for_id = {}
        self.encyclopedia_volume_for_id = {}

        self.category_for_id = {}
        self.feature_for_id = {}

        self.listed_value_for_id = {}
        self.value_type_for_name = {}
        self.empty_value_for_feature_id_and_type_name = {}

        self.doculect_type_for_id = {
            'language': models.DoculectType(name_en='language', name_ru='язык'), 
            'dialect': models.DoculectType(name_en='dialect', name_ru='диалект'), 
            'language/dialect': models.DoculectType(name_en='language_dialect', name_ru='язык/диалект')
        }

    def setup_models(self):
        self._delete_all_data()
        self._populate_all()
    
    def _delete_all_data(self):
        for model_or_table in (
                models.Doculect, models.DoculectType, models.Country, models.EncyclopediaVolume,
                models.FeatureValue, models.FeatureValueType, models.Feature, models.FeatureCategory,
                models.association_tables.doculect_to_feature_value,
        ):
            self.dbsession.execute(delete(model_or_table))

    def _populate_all(self):

        self._populate_categories_features_values()
        self._populate_countries()
        self._populate_encyclopedia_volumes()

        self._populate_doculects_and_custom_feature_values()

    def _populate_categories_features_values(self):
        # Putting these in one method to emphasize tight coupling
        # between the three operations

        for category_row in self.read_file(self.file_with_categories):
            category = models.FeatureCategory(
                man_id=category_row['id'],
                name_en=category_row['en'],
                name_ru=category_row['ru'],
            )
            self.dbsession.add(category)
            self.category_for_id[category_row['id']] = category

        for value_type_row in self.read_file(self.file_with_value_types):
            value_type = models.FeatureValueType(name=value_type_row['id'])
            self.value_type_for_name[value_type_row['id']] = value_type
            self.dbsession.add(value_type)

        for feature_row in self.read_file(self.file_with_names_of_features):
            feature = models.Feature(
                man_id=feature_row['id'],
                name_en=feature_row['en'],
                name_ru=feature_row['ru'],
                category=self.category_for_id[feature_row['id'].split('-')[0]]  # TODO add column feature_id to CSV?
            )

            # adding values of 3 empty types for each feature
            for value_type_name in ('not_stated', 'explicit_gap', 'not_applicable'):
                empty_value = models.FeatureValue(
                        man_id='',
                        name_en='',
                        name_ru='',
                        type=self.value_type_for_name[value_type_name],
                )
                feature.values.append(empty_value)
                self.empty_value_for_feature_id_and_type_name[(feature_row['id'], value_type_name)] = empty_value

            self.dbsession.add(feature)
            self.feature_for_id[feature_row['id']] = feature

        # populating values of type 'listed': from file with listed values
        for value_row in self.read_file(self.file_with_listed_values):
            value = models.FeatureValue(
                man_id=value_row['id'],
                name_en=value_row['en'],
                name_ru=value_row['ru'],
                feature=self.feature_for_id[value_row['feature_id']],
                type=self.value_type_for_name['listed']
            )
            self.dbsession.add(value)
            self.listed_value_for_id[value_row['id']] = value

    def _populate_countries(self):

        for country_row in self.read_file(self.file_with_countries):
            country = models.country.Country(
                man_id=country_row['id'],
                iso=country_row['ISO 3166-1 alpha-3'],
                is_historical=int(country_row['is_historical']),
                name_en=country_row['en'],
                name_ru=country_row['ru'],
            )
            self.dbsession.add(country)
            self.country_for_id[country_row['id']] = country
            
    def _populate_encyclopedia_volumes(self):

        for encyclopedia_row in self.read_file(self.file_with_encyclopedia_volumes):
            volume = models.encyclopedia_volume.EncyclopediaVolume(**encyclopedia_row)
            self.dbsession.add(volume)
            self.encyclopedia_volume_for_id[volume.id] = volume

    def _populate_doculects_and_custom_feature_values(self):
        doculect_rows = self.read_file(self.file_with_doculects)

        for doculect_type in self.doculect_type_for_id.values():
            self.dbsession.add(doculect_type)

        for doculect_row in doculect_rows:
            doculect_row_to_write = copy(doculect_row)

            doculect_row_to_write['man_id'] = doculect_row_to_write['id']
            del doculect_row_to_write['id']  # ID will be autogenerated integer

            main_country = self.country_for_id[doculect_row_to_write['main_country_id']]
            del doculect_row_to_write['main_country_id']  # should be autogenerated from ForeignKey

            encyclopedia_volume = None
            if doculect_row_to_write['encyclopedia_volume_id']:  # should be there for every doculect, actually
                encyclopedia_volume = self.encyclopedia_volume_for_id[doculect_row_to_write['encyclopedia_volume_id']]

            del doculect_row_to_write['encyclopedia_volume_id']

            for bool_key in ('is_extinct', 'is_multiple', 'has_feature_profile'):
                doculect_row_to_write[bool_key] = int(doculect_row_to_write[bool_key])

            type_of_this_doculect = self.doculect_type_for_id[doculect_row_to_write['type']]
            del doculect_row_to_write['type']

            # print(row)
            doculect = models.doculect.Doculect(**doculect_row_to_write)

            doculect.main_country = main_country
            doculect.type = type_of_this_doculect

            if encyclopedia_volume:
                doculect.encyclopedia_volume = encyclopedia_volume

            if doculect_row_to_write['has_feature_profile'] == 1:
                feature_profile_rows = self.read_file(self.dir_with_feature_profiles / f"{doculect_row['id']}.csv")

                for feature_profile_row in feature_profile_rows:

                    if feature_profile_row['feature_id'] == '_aux':
                        continue  # TODO: think about comment for entire feature profile

                    value_type = feature_profile_row['value_type']

                    if value_type == 'listed':
                        value = self.listed_value_for_id[feature_profile_row['value_id']]
                    elif value_type == 'custom':
                        value = models.FeatureValue(
                            man_id='',
                            name_ru=feature_profile_row['value_ru'],
                            name_en='',
                            type=self.value_type_for_name['custom'],
                            feature=self.feature_for_id[feature_profile_row['feature_id']]
                        )
                    else:
                        value = self.empty_value_for_feature_id_and_type_name[
                            (feature_profile_row['feature_id'], value_type)
                        ]
                    doculect.feature_values.append(value)

            self.dbsession.add(doculect)


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    CustomModelInitializer(dbsession).setup_models()


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError as e:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
        print(str(e))
