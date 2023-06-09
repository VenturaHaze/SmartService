"""
Script: data_preparation_time_series_unit_test.py
========================

This script serves to test the data processing steps implemented in `data_preparation_time_series.py`.
The script employs Python's unittest module to ensure the consistency and correctness of transformations applied to the original data. The primary functionalities include:

1. Loading both the original and processed datasets.
2. Checking the number of unique values in the "PC6_WeekIndex" column in both datasets.
3. Sampling 5000 random observations from the processed data.
4. Filtering the original data to match the "PC6_WeekIndex" in the processed data.
5. Sorting both datasets by "PC6" + "Date".
6. Iterating over all rows in the processed data, fetch the corresponding row from the original data and ensure that the target column value matches.

Requirements:
- The original and processed datasets must be CSV files and must exist in the same directory as the script.
"""

import unittest
import pandas as pd
from tqdm import tqdm

class TestProcessedData(unittest.TestCase):
    def test_target_column(self):

        # Load the original and processed datasets
        original_data = pd.read_csv('final_data_SE_cleaned.csv')
        processed_data = pd.read_csv('final_data_SE_cleaned_processed.csv')

        # unique values in PC6_WeekIndex should be equal in both datasets
        print(processed_data['PC6_WeekIndex'].nunique())
        print(original_data['PC6_WeekIndex'].nunique())

        # Define the target column
        TARGET_COLUMN = 'kWh'

        # Randomly sample 10000 observations from the processed data and discard the rest
        processed_data = processed_data.sample(n=5000, random_state=1)

        # by definition, the processed data should have fewer rows than the original data
        self.assertTrue(len(processed_data) < len(original_data))

        # Only keep rows in the original data that match the "PC6_WeekIndex" in the processed data
        matching_rows = original_data['PC6_WeekIndex'].isin(processed_data['PC6_WeekIndex'])
        original_data = original_data[matching_rows]

        # unique values in PC6_WeekIndex should be equal in both datasets
        print(processed_data['PC6_WeekIndex'].nunique())
        print(original_data['PC6_WeekIndex'].nunique())
        self.assertTrue(processed_data['PC6_WeekIndex'].nunique() == original_data['PC6_WeekIndex'].nunique())

        # after filtering, the number of rows in the original data should be equal to the number of rows in the processed data
        self.assertTrue(len(processed_data) == len(original_data))

        # sort both datasets by "PC6" + "Date"
        processed_data = processed_data.sort_values(by=['PC6', 'Date'])
        original_data = original_data.sort_values(by=['PC6', 'Date'])


        print(processed_data.head())
        print(original_data.head())

        # Iterate over all rows in the processed data
        for _, row in tqdm(processed_data.iterrows()):
            identifier = row['PC6_WeekIndex']

            # Fetch the corresponding row from the original data
            original_row = original_data[original_data['PC6_WeekIndex'] == identifier]

            # Assert that the target column value matches
            self.assertEqual(original_row[TARGET_COLUMN].values[0], row[TARGET_COLUMN + '(t-0)'])
            # print(f"Original: {original_row[TARGET_COLUMN].values[0]}, Processed: {row[TARGET_COLUMN + '(t-0)']}")

if __name__ == '__main__':
    unittest.main()