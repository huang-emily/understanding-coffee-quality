import pandas as pd

# from fatih-boyar github

df = pd.read_csv('processed_data/arabica_data_raw.csv')

df.rename(columns={df.columns[0]: 'ID'}, inplace=True) # changing the uninformative first column to ID
df['ID'] = pd.Series(range(df.shape[0])) # assigning the ID numbers
df.drop('NA', axis='columns', inplace=True) # dropping the NA columns. It's just NA.

df['Color'] = df['Color'].str.lower() # for consistent wording
df['Category One Defects'] = df['Category One Defects'].str.split(' ', n=1, expand=True)[0] # only numeric values
df['Category Two Defects'] = df['Category Two Defects'].str.split(' ', n=1, expand=True)[0] # only numeric values
df.rename(columns={'Moisture': 'Moisture Percentage'}, inplace=True) # this variable is in percentage, changing the name
df['Moisture Percentage'] = df['Moisture Percentage'].str.split(' ', n=1, expand=True)[0] # only numeric values


df.to_csv('processed_data/arabica_data_cleaned.csv')