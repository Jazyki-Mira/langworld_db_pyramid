from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / 'langworld_db_data' / 'data'

ASSETS_DIR = DATA_DIR / 'assets'
FILE_WITH_MAP_TO_DOCULECT = ASSETS_DIR / 'encyclopedia_map_to_doculect.csv'
FILE_WITH_MAPS = ASSETS_DIR / 'encyclopedia_maps.csv'
FILE_WITH_ENCYCLOPEDIA_VOLUMES = ASSETS_DIR / 'encyclopedia_volumes.csv'

INVENTORIES_DIR = DATA_DIR / 'inventories'
FILE_WITH_COUNTRIES = INVENTORIES_DIR / 'countries.csv'
FILE_WITH_CATEGORIES = INVENTORIES_DIR / 'feature_categories.csv'
FILE_WITH_DOCULECTS = INVENTORIES_DIR / 'doculects.csv'
FILE_WITH_GENEALOGY_HIERARCHY = INVENTORIES_DIR / 'genealogy_families_hierarchy.yaml'
FILE_WITH_GENEALOGY_NAMES = INVENTORIES_DIR / 'genealogy_families_names.csv'
FILE_WITH_LISTED_VALUES = INVENTORIES_DIR / 'features_listed_values.csv'
FILE_WITH_NAMES_OF_FEATURES = INVENTORIES_DIR / 'features.csv'
FILE_WITH_VALUE_TYPES = INVENTORIES_DIR / 'feature_value_types.csv'

FEATURE_PROFILES_DIR = DATA_DIR / 'feature_profiles'
