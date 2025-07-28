from pathlib import Path
from typing import Dict, Set, Tuple

from langworld_db_data.constants.literals import ATOMIC_VALUE_SEPARATOR
from tinybear.csv_xls import read_dicts_from_csv
from langworld_db_pyramid import models


class TestDataCounter:
    def __init__(self, test_data_dir: Path):
        self.test_data_dir = test_data_dir
        self.doculects = read_dicts_from_csv(self.test_data_dir / "doculects.csv")
        self.feature_profiles_dir = test_data_dir / "feature_profiles"

    def count_countries(self) -> int:
        """Count number of countries in countries.csv."""
        return len(read_dicts_from_csv(self.test_data_dir / "countries.csv"))

    def count_doculects(self) -> int:
        """Count number of doculects in doculects.csv."""
        return len(self.doculects)

    def count_doculect_types(self) -> int:
        """Count number of doculect types in doculects.csv."""
        return len({d["type"] for d in self.doculects})

    def count_encyclopedia_maps(self) -> int:
        """Count number of encyclopedia maps in encyclopedia_maps.csv."""
        return len(read_dicts_from_csv(self.test_data_dir / "encyclopedia_maps.csv"))

    def count_encyclopedia_volumes(self) -> int:
        """Count number of encyclopedia volumes in encyclopedia_volumes.csv."""
        return len(read_dicts_from_csv(self.test_data_dir / "encyclopedia_volumes.csv"))

    def count_features(self) -> int:
        """Count number of features in features.csv."""
        return len(read_dicts_from_csv(self.test_data_dir / "features.csv"))

    def count_feature_categories(self) -> int:
        """Count number of feature categories in feature_categories.csv."""
        return len(read_dicts_from_csv(self.test_data_dir / "feature_categories.csv"))

    def count_feature_value_types(self) -> int:
        """Count number of feature value types in feature_value_types.csv."""
        return len(read_dicts_from_csv(self.test_data_dir / "feature_value_types.csv"))

    def count_glottocodes(self) -> int:
        """Count number of unique glottocodes in doculects.csv."""
        unique_glottocodes: Set[str] = set()
        for doculect in self.doculects:
            glottocode = doculect["glottocode"]
            if glottocode:
                # Split by comma in case there are multiple codes
                unique_glottocodes.update(glottocode.split(", "))

        return len(unique_glottocodes)

    def count_iso639p3codes(self) -> int:
        """Count number of unique ISO 639-3 codes in doculects.csv."""
        unique_iso_codes: Set[str] = set()
        for doculect in self.doculects:
            iso_code = doculect["iso_639_3"]
            if iso_code:
                # Split by comma in case there are multiple codes
                unique_iso_codes.update(iso_code.split(", "))
        return len(unique_iso_codes)

    def count_listed_values(self) -> int:
        """Count number of listed values in features_listed_values.csv."""
        return len(read_dicts_from_csv(self.test_data_dir / "features_listed_values.csv"))

    def count_compound_listed_values(self) -> int:
        """Count number of unique compound listed values across all feature profiles."""
        unique_compound_values: Set[str] = set()

        for file in self.feature_profiles_dir.glob("*.csv"):
            rows = read_dicts_from_csv(file)
            for row in rows:
                if row["value_type"] == "listed" and ATOMIC_VALUE_SEPARATOR in row["value_id"]:
                    # Add the entire compound value ID
                    unique_compound_values.add(row["value_id"])

        return len(unique_compound_values)

    def count_unique_custom_values(self) -> int:
        """Count number of unique custom values across all feature profiles."""
        unique_custom_values: Set[Tuple[str, str]] = set()
        for file in self.feature_profiles_dir.glob("*.csv"):
            rows_with_custom_values = {
                (row["feature_id"], row["value_ru"])
                for row in read_dicts_from_csv(file)
                if row["value_type"] == "custom"
            }
            unique_custom_values.update(rows_with_custom_values)
        return len(unique_custom_values)

    def count_doculects_by_country(self, country_id: str) -> int:
        """Count number of doculects in doculects.csv that belong to a specific country.

        Args:
            country_id: The country ID (e.g., 'afg' for Afghanistan)

        Returns:
            Number of doculects associated with the given country
        """
        return len([d for d in self.doculects if d["main_country_id"] == country_id])

    def count_doculects_by_encyclopedia_volume(self, volume_id: str) -> int:
        """Count number of doculects in doculects.csv that belong to a specific encyclopedia volume.

        Args:
            volume_id: The ID of the encyclopedia volume (e.g., '11')

        Returns:
            Number of doculects associated with the given encyclopedia volume
        """
        return len([d for d in self.doculects if d["encyclopedia_volume_id"] == volume_id])

    def get_expected_model_counts(self) -> Dict[type, int]:
        """Get expected counts for all models based on CSV files."""
        return {
            models.Country: self.count_countries(),
            models.Doculect: self.count_doculects(),
            models.DoculectType: self.count_doculect_types(),
            models.EncyclopediaMap: self.count_encyclopedia_maps(),
            models.EncyclopediaVolume: self.count_encyclopedia_volumes(),
            models.Feature: self.count_features(),
            models.FeatureCategory: self.count_feature_categories(),
            models.FeatureValue: (
                self.count_listed_values()
                + self.count_features() * 3  # 3 value types with empty values
                + self.count_compound_listed_values()
                + self.count_unique_custom_values()
            ),
            models.FeatureValueType: self.count_feature_value_types(),
            models.Glottocode: self.count_glottocodes(),
            models.Iso639P3Code: self.count_iso639p3codes(),
        }
