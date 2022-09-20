import argparse
from copy import copy
from pathlib import Path
import sys
from typing import cast, Optional, Union

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy import delete
from sqlalchemy.exc import OperationalError

from langworld_db_data.constants import paths
from langworld_db_data.filetools.csv_xls import read_dicts_from_csv
from langworld_db_data.filetools.json_toml_yaml import read_json_toml_yaml

from langworld_db_pyramid import models


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
        dir_with_feature_profiles: Path = paths.FEATURE_PROFILES_DIR,
        file_with_categories: Path = paths.FILE_WITH_CATEGORIES,
        file_with_countries: Path = paths.FILE_WITH_COUNTRIES,
        file_with_doculects: Path = paths.FILE_WITH_DOCULECTS,
        file_with_encyclopedia_maps: Path = paths.FILE_WITH_MAPS,
        file_with_encyclopedia_map_to_doculect: Path = paths.FILE_WITH_MAP_TO_DOCULECT,
        file_with_encyclopedia_volumes: Path = paths.FILE_WITH_ENCYCLOPEDIA_VOLUMES,
        file_with_genealogy_hierarchy: Path = paths.FILE_WITH_GENEALOGY_HIERARCHY,
        file_with_genealogy_names: Path = paths.FILE_WITH_GENEALOGY_NAMES,
        file_with_listed_values: Path = paths.FILE_WITH_LISTED_VALUES,
        file_with_names_of_features: Path = paths.FILE_WITH_NAMES_OF_FEATURES,
        file_with_value_types: Path = paths.FILE_WITH_VALUE_TYPES,
    ):
        self.ALL_MODELS = (
            models.association_tables.DoculectToFeatureValue,
            models.association_tables.DoculectToGlottocode,
            models.association_tables.DoculectToIso639P3Code,
            models.association_tables.EncyclopediaMapToDoculect,
            models.Doculect,
            models.DoculectFeatureValueInfo,
            models.DoculectType,
            models.Country,
            models.EncyclopediaMap,
            models.EncyclopediaVolume,
            models.Family,
            models.FeatureValue,
            models.FeatureValueType,
            models.Feature,
            models.FeatureCategory,
            models.Glottocode,
            models.Iso639P3Code,
        )

        self.dbsession = dbsession

        self.dir_with_feature_profiles = dir_with_feature_profiles
        self.file_with_categories = file_with_categories
        self.file_with_countries = file_with_countries
        self.file_with_doculects = file_with_doculects
        self.file_with_encyclopedia_maps = file_with_encyclopedia_maps
        self.file_with_encyclopedia_map_to_doculect = file_with_encyclopedia_map_to_doculect
        self.file_with_encyclopedia_volumes = file_with_encyclopedia_volumes
        self.file_with_genealogy_hierarchy = file_with_genealogy_hierarchy
        self.file_with_listed_values = file_with_listed_values
        self.file_with_names_of_features = file_with_names_of_features
        self.file_with_value_types = file_with_value_types

        self.genealogy_names_for_id = {
            row['id']: {
                'en': row['en'],
                'ru': row['ru']
            } for row in read_dicts_from_csv(file_with_genealogy_names)
        }

        # Dictionaries map identifiers to instances of mapped classes:

        self.country_for_id: dict[str, models.Country] = {}
        self.encyclopedia_map_for_id: dict[str, models.EncyclopediaMap] = {}
        self.encyclopedia_volume_for_id: dict[str, models.EncyclopediaVolume] = {}
        self.family_for_id: dict[str, models.Family] = {}

        self.category_for_id: dict[str, models.FeatureCategory] = {}
        self.feature_for_id: dict[str, models.Feature] = {}
        self.glottocode_for_id: dict[str, models.Glottocode] = {}
        self.iso639p3code_for_id: dict[str, models.Iso639P3Code] = {}

        self.listed_value_for_id: dict[str, models.FeatureValue] = {}
        self.value_type_for_name: dict[str, models.FeatureValueType] = {}
        self.custom_value_for_feature_id_and_value_ru: dict[tuple[str, str], models.FeatureValue] = {}
        self.empty_value_for_feature_id_and_type_name: dict[tuple[str, str], models.FeatureValue] = {}

        self.doculect_type_for_id = {
            'language': models.DoculectType(name_en='language', name_ru='язык'),
            'dialect': models.DoculectType(name_en='dialect', name_ru='диалект'),
            'language/dialect': models.DoculectType(name_en='language_dialect', name_ru='язык/диалект')
        }

    def setup_models(self) -> None:
        self._delete_all_data()
        self._populate_all()

    def _delete_all_data(self) -> None:
        for model in self.ALL_MODELS:
            self.dbsession.execute(delete(model))

    def _populate_all(self) -> None:

        self._populate_categories_features_value_types_listed_and_empty_values()
        self._populate_countries()
        self._populate_encyclopedia_maps()
        self._populate_encyclopedia_volumes()
        self._populate_families()
        self._populate_glottocodes()
        self._populate_iso639p3_codes()

        self._populate_doculects_custom_feature_values_and_comments()
        self._set_is_listed_and_has_doculect_to_false_for_listed_values_without_doculects()

    def _populate_categories_features_value_types_listed_and_empty_values(self) -> None:
        # Putting these in one method to emphasize tight coupling
        # between the three operations

        for category_row in read_dicts_from_csv(self.file_with_categories):
            category = models.FeatureCategory(
                man_id=category_row['id'],
                name_en=category_row['en'],
                name_ru=category_row['ru'],
            )
            self.dbsession.add(category)
            self.category_for_id[category_row['id']] = category

        for value_type_row in read_dicts_from_csv(self.file_with_value_types):
            value_type = models.FeatureValueType(
                name=value_type_row['id'],
                entails_empty_value=int(value_type_row['entails_empty_value']),
            )
            self.value_type_for_name[value_type_row['id']] = value_type
            self.dbsession.add(value_type)

        for feature_row in read_dicts_from_csv(self.file_with_names_of_features):
            feature = models.Feature(man_id=feature_row['id'],
                                     name_en=feature_row['en'],
                                     name_ru=feature_row['ru'],
                                     category=self.category_for_id[feature_row['id'].split('-')[0]])

            # adding values of 3 entailing-empty-value types for each feature
            for value_type in [t for t in self.value_type_for_name.values() if t.entails_empty_value]:
                empty_value = models.FeatureValue(
                    is_listed_and_has_doculects=False,
                    man_id='',
                    name_en='',
                    name_ru='',
                    type=value_type,
                )
                feature.values.append(empty_value)
                self.empty_value_for_feature_id_and_type_name[(feature_row['id'], value_type.name)] = empty_value

            self.dbsession.add(feature)
            self.feature_for_id[feature_row['id']] = feature

        # populating values of type 'listed': from file with listed values
        for value_row in read_dicts_from_csv(self.file_with_listed_values):
            value = models.FeatureValue(
                # This will be set to False later if there are no doculects.
                # See comment in models/feature_value.py about conscious choice of this suboptimal algorithm
                is_listed_and_has_doculects=True,
                man_id=value_row['id'],
                name_en=value_row['en'],
                name_ru=value_row['ru'],
                feature=self.feature_for_id[value_row['feature_id']],
                type=self.value_type_for_name['listed'])
            self.dbsession.add(value)
            self.listed_value_for_id[value_row['id']] = value

    def _populate_countries(self) -> None:

        for country_row in read_dicts_from_csv(self.file_with_countries):
            country = models.Country(
                man_id=country_row['id'],
                iso=country_row['ISO 3166-1 alpha-3'],
                is_historical=int(country_row['is_historical']),
                name_en=country_row['en'],
                name_ru=country_row['ru'],
            )
            self.dbsession.add(country)
            self.country_for_id[country_row['id']] = country

    def _populate_encyclopedia_maps(self) -> None:
        for map_row in read_dicts_from_csv(self.file_with_encyclopedia_maps):
            row_for_model = copy(map_row)
            row_for_model['man_id'] = row_for_model.pop('id')
            encyclopedia_map = models.EncyclopediaMap(**row_for_model)
            self.dbsession.add(encyclopedia_map)
            self.encyclopedia_map_for_id[encyclopedia_map.man_id] = encyclopedia_map

    def _populate_encyclopedia_volumes(self) -> None:
        for encyclopedia_row in read_dicts_from_csv(self.file_with_encyclopedia_volumes):
            volume = models.EncyclopediaVolume(**encyclopedia_row)
            self.dbsession.add(volume)
            self.encyclopedia_volume_for_id[volume.id] = volume

    def _populate_families(self) -> None:
        # make initial call to another function that will recursively call itself until all families are processed
        self._process_genealogy_hierarchy(read_json_toml_yaml(self.file_with_genealogy_hierarchy))

    def _process_genealogy_hierarchy(self, items: list, parent: Optional[models.family.Family] = None) -> None:
        if not isinstance(items, list):
            raise TypeError(f'This function cannot be called with {type(items)} ({items})')

        for node in items:
            if not isinstance(node, (str, dict)):
                raise TypeError(f'Node cannot be of type {type(node)} ({node})')

            manual_id = list(node.keys())[0] if isinstance(node, dict) else node

            family = models.Family(
                man_id=manual_id,
                name_en=self.genealogy_names_for_id[manual_id]['en'],
                name_ru=self.genealogy_names_for_id[manual_id]['ru'],
            )
            if parent is not None:
                family.parent = parent

            self.family_for_id[manual_id] = family
            self.dbsession.add(family)

            if isinstance(node, dict):
                # A dictionary in this hierarchy always has only one key,
                # so the node's children are in the first item of .values()
                self._process_genealogy_hierarchy(items=list(node.values())[0], parent=family)

    def _populate_glottocodes(self) -> None:
        # for now, I see it reasonable to only add codes that are present in file with doculects (same for ISO-639-3)
        for row in read_dicts_from_csv(self.file_with_doculects):
            glottocodes = row['glottocode'].split(', ')
            for item in glottocodes:
                if not item:
                    continue
                try:
                    self.glottocode_for_id[item]
                except KeyError:
                    glottocode = models.Glottocode(code=item)
                    self.glottocode_for_id[item] = glottocode
                    self.dbsession.add(glottocode)

    def _populate_iso639p3_codes(self) -> None:
        for row in read_dicts_from_csv(self.file_with_doculects):
            iso_codes = row['iso_639_3'].split(', ')
            for item in iso_codes:
                if not item:
                    continue
                try:
                    self.iso639p3code_for_id[item]
                except KeyError:
                    iso_code = models.Iso639P3Code(code=item)
                    self.iso639p3code_for_id[item] = iso_code
                    self.dbsession.add(iso_code)

    def _populate_doculects_custom_feature_values_and_comments(self) -> None:
        doculect_rows = read_dicts_from_csv(self.file_with_doculects)
        rows_with_encyclopedia_map_to_doculect = read_dicts_from_csv(self.file_with_encyclopedia_map_to_doculect)

        for doculect_type in self.doculect_type_for_id.values():
            self.dbsession.add(doculect_type)

        for doculect_row in doculect_rows:
            doculect_row_to_write = copy(doculect_row)

            # for typechecking only: Doculect has some boolean fields, while original dictionary values are all `str`
            doculect_row_to_write = cast(dict[str, Union[str, bool]], doculect_row_to_write)

            # popping attributes for future IDs as they will all be autogenerated (auto-incremented ID or ForeignKey)

            doculect_row_to_write['man_id'] = doculect_row_to_write.pop('id')

            main_country = self.country_for_id[doculect_row_to_write.pop('main_country_id')]

            volume_id = doculect_row_to_write.pop('encyclopedia_volume_id')
            # should be there for every doculect, actually
            encyclopedia_volume = self.encyclopedia_volume_for_id[volume_id] if volume_id else None

            family = self.family_for_id[doculect_row_to_write.pop('family_id')]

            for bool_key in ('is_extinct', 'is_multiple', 'has_feature_profile'):
                doculect_row_to_write[bool_key] = bool(int(doculect_row_to_write[bool_key]))

            type_of_this_doculect = self.doculect_type_for_id[doculect_row_to_write.pop('type')]

            glottocodes_for_this_doculect = [
                self.glottocode_for_id[glottocode]
                for glottocode in doculect_row_to_write.pop('glottocode').split(', ')
                if glottocode
            ]

            iso_639p3_codes_for_this_doculect = [
                self.iso639p3code_for_id[iso_code]
                for iso_code in doculect_row_to_write.pop('iso_639_3').split(', ')
                if iso_code
            ]

            # POINT OF CREATION OF DOCULECT OBJECT
            doculect = models.Doculect(**doculect_row_to_write)

            doculect.comment_en = ''
            doculect.comment_ru = ''

            for encyclopedia_map_id in [
                    row['encyclopedia_map_id']
                    for row in rows_with_encyclopedia_map_to_doculect
                    if row['doculect_id'] == doculect.man_id
            ]:
                doculect.encyclopedia_maps.append(self.encyclopedia_map_for_id[encyclopedia_map_id])

            if encyclopedia_volume:
                doculect.encyclopedia_volume = encyclopedia_volume
            doculect.family = family
            doculect.glottocodes = glottocodes_for_this_doculect
            doculect.iso_639p3_codes = iso_639p3_codes_for_this_doculect
            doculect.main_country = main_country
            doculect.type = type_of_this_doculect

            if doculect_row_to_write['has_feature_profile'] == 1:
                feature_profile_rows = read_dicts_from_csv(self.dir_with_feature_profiles / f"{doculect_row['id']}.csv")

                for feature_profile_row in feature_profile_rows:

                    if feature_profile_row['feature_id'] == '_aux':
                        if feature_profile_row['comment_en']:
                            doculect.comment_en += f"Feature profile prepared by {feature_profile_row['comment_en']}"
                        if feature_profile_row['comment_ru']:
                            doculect.comment_ru += f"Составитель/редактор реферата: {feature_profile_row['comment_ru']}"
                        continue

                    # 1. Processing value
                    value_type = feature_profile_row['value_type']

                    if value_type == 'listed':
                        value = self.listed_value_for_id[feature_profile_row['value_id']]
                    elif value_type == 'custom':
                        # if value is already in dictionary, use it, else create
                        try:
                            value = self.custom_value_for_feature_id_and_value_ru[(feature_profile_row['feature_id'],
                                                                                   feature_profile_row['value_ru'])]
                        except KeyError:
                            value = models.FeatureValue(is_listed_and_has_doculects=False,
                                                        man_id='',
                                                        name_ru=feature_profile_row['value_ru'],
                                                        name_en='',
                                                        type=self.value_type_for_name['custom'],
                                                        feature=self.feature_for_id[feature_profile_row['feature_id']])
                            self.custom_value_for_feature_id_and_value_ru[(feature_profile_row['feature_id'],
                                                                           feature_profile_row['value_ru'])] = value
                    else:
                        value = self.empty_value_for_feature_id_and_type_name[(feature_profile_row['feature_id'],
                                                                               value_type)]

                    doculect.feature_values.append(value)

                    # 2. Processing comment
                    if feature_profile_row['comment_ru'] or feature_profile_row['comment_en'] or feature_profile_row[
                            'page_numbers']:
                        models.DoculectFeatureValueInfo(
                            doculect=doculect,
                            feature_value=value,
                            page_numbers=feature_profile_row['page_numbers'],
                            text_en=feature_profile_row['comment_en'],
                            text_ru=feature_profile_row['comment_ru'],
                        )  # will be added to dbsession automatically when doculect gets added

            self.dbsession.add(doculect)

    def _set_is_listed_and_has_doculect_to_false_for_listed_values_without_doculects(self) -> None:
        for value in self.listed_value_for_id.values():
            if not value.doculects:
                value.is_listed_and_has_doculects = False


def setup_models(dbsession) -> None:
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


# noinspection PyDefaultArgument
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
