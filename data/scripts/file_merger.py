import pandas as pd

coffee2025 = pd.read_csv('processed_data/arabica_data_cleaned.csv')
coffee2023 = pd.read_csv('files_from_fatih/arabica_ratings_raw.csv')

# convert problem columns using object type to float64 type (or some kind of numeric type)
coffee2023['Total Cup Points'] = pd.to_numeric(coffee2023['Total Cup Points'], errors='coerce')
coffee2023['Category One Defects'] = pd.to_numeric(coffee2023['Category One Defects'], errors='coerce')
coffee2023['Category Two Defects'] = pd.to_numeric(coffee2023['Category Two Defects'], errors='coerce')

# use this list of columns as the order every time
common_columns = ['Country of Origin', 'Farm Name', 'Lot Number',
       'Mill', 'ICO Number', 'Company', 'Altitude', 'Region', 'Producer',
       'Number of Bags', 'Bag Weight', 'In-Country Partner', 'Harvest Year',
       'Grading Date', 'Owner', 'Variety', 'Status', 'Processing Method',
       'Aroma', 'Flavor', 'Aftertaste', 'Acidity', 'Body', 'Balance',
       'Uniformity', 'Clean Cup', 'Sweetness',
       'Total Cup Points', 'Category One Defects',
       'Quakers', 'Color', 'Category Two Defects', 'Expiration',
       'Certification Body', 'Certification Address', 'Certification Contact']

# combine the dataframe
coffee2025_common = coffee2025[common_columns]
coffee2023_common = coffee2023[common_columns]
combined_coffee = pd.concat([coffee2025_common, coffee2023_common], axis=0, ignore_index=True)

# verify the columns look good
combined_coffee.info()

#output back out
combined_coffee.to_csv('processed_data/arabica_data_combined.csv')
