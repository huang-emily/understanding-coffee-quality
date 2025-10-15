import pandas as pd
import numpy as np
import os

# THIS FILE MUST BE IN THE SAME DIRECTORY AS YOUR SCRAPPED DATA

# all the files from working directory:
data_dir = os.getcwd() + "/scraped_data"
dir = pd.DataFrame({'files': os.listdir(path=data_dir)})
# only the files we scraped from the database
coffee_list = dir[dir['files'].str.contains('coffee')].reset_index(drop=True)

# splitting the file names so we can see the table names
coffee_list_split_temp = coffee_list['files'].str.split('_', n=3, expand=True)
col1 = coffee_list_split_temp[0] + '_' + coffee_list_split_temp[1] + '_' + coffee_list_split_temp[2]
coffee_list_split = pd.DataFrame({'coffee': col1,
                                     'tables': coffee_list_split_temp[3]})

# see which coffees do not have 4 tables
table_counts = coffee_list_split.groupby('coffee').count()
print(table_counts[table_counts['tables'] != 4])

df_list = []
# skips here in case something happened with parsing
# add as (page, row)
skips = []

for page in range(1, 9):
    if page == 8:
        last_row = 45
    else:
        last_row = 51

    for row in range(1, last_row):
        if (page, row) in skips:
            print('skipping pg{} row{}'.format(page, row))
            pass
        else:
            df0 = pd.read_csv('scraped_data/coffee_pg{}_row{}_table0.csv'.format(page, row))
            df1 = pd.read_csv('scraped_data/coffee_pg{}_row{}_table1.csv'.format(page, row))
            df2 = pd.read_csv('scraped_data/coffee_pg{}_row{}_table2.csv'.format(page, row))
            df3 = pd.read_csv('scraped_data/coffee_pg{}_row{}_table3.csv'.format(page, row))

            # df0
            """
            Unnamed: 0                  0                      1                   2  \
            0           0  Country of Origin               Colombia      Number of Bags   
            1           1          Farm Name       Finca El Paraiso          Bag Weight   
            2           2         Lot Number             CQU2022015  In-Country Partner   
            3           3               Mill       Finca El Paraiso        Harvest Year   
            4           4         ICO Number                    NaN        Grading Date   
            5           5            Company   Coffee Quality Union               Owner   
            6           6           Altitude              1700-1930             Variety   
            7           7             Region         Piendamo,Cauca              Status   
            8           8           Producer  Diego Samuel Bermudez   Processing Method   
                                    3  
            0                        1  
            1                    35 kg  
            2    Japan Coffee Exchange  
            3              2021 / 2022  
            4     September 21st, 2022  
            5     Coffee Quality Union  
            6                 Castillo    
            """
            df0.columns = ['zero','one','two','three','four']
            colnames1 = df0['one'].tolist()
            colnames2 = df0['three'].tolist()
            data1 = df0['two'].tolist()
            data2 = df0['four'].tolist()

            df0_processed = pd.DataFrame([(data1+data2)], columns=(colnames1+colnames2))

            # df1: The cupping scores are stored in this table
            """
            Unnamed: 0           0     1                 2      3
            0           0       Aroma  8.58        Uniformity  10.00
            1           1      Flavor  8.50         Clean Cup  10.00
            2           2  Aftertaste  8.42         Sweetness  10.00
            3           3     Acidity  8.58           Overall   8.58
            4           4        Body  8.25           Defects   0.00
            5           5     Balance  8.42  Total Cup Points  89.33
            """
            df1.columns = ['zero','one','two','three','four']
            colnames1 = df1['one'].tolist()
            colnames2 = df1['three'].tolist()
            data1 = df1['two'].tolist()
            data2 = df1['four'].tolist()

            df1_processed = pd.DataFrame([(data1+data2)], columns=(colnames1+colnames2))

            # df2
            """
            Unnamed: 0                     0               1                     2  \
            0           0              Moisture          11.8 %                 Color   
            1           1  Category One Defects  0 full defects  Category Two Defects   
            2           2               Quakers               0                   NaN   
                            3  
            0           Green  
            1  3 full defects  
            2             NaN    
            """

            df2.columns = ['zero','one','two','three','four']
            colnames1 = df2['one'].tolist()
            colnames2 = df2['three'].tolist()
            data1 = df2['two'].tolist()
            data2 = df2['four'].tolist()

            df2_processed = pd.DataFrame([(data1+data2)], columns=(colnames1+colnames2))

            # df3
            """
            Unnamed: 0                      0  \
            0           0             Expiration   
            1           1     Certification Body   
            2           2  Certification Address   
            3           3  Certification Contact   
                                                            1  
            0                               September 21st, 2023  
            1                              Japan Coffee Exchange  
            2  〒413-0002 静岡県熱海市伊豆山１１７３−５８ 1173-58 Izusan, Ata...  
            3            松澤　宏樹　Koju Matsuzawa - +81(0)9085642901    
            """

            df3.columns = ['zero','one','two']
            colnames1 = df3['one'].tolist()
            data1 = df3['two'].tolist()

            df3_processed = pd.DataFrame([data1], columns=colnames1)
            df = pd.concat([df0_processed, df1_processed, df2_processed, df3_processed], axis=1)
            df = df.rename(columns={np.nan: "NA"})
            df_list.append(df)

df_final = pd.concat(df_list, axis=0)
print(df_final.columns)
print(df_final.shape)
print(df_final.head())
df_final.to_csv('processed_data/arabica_data_raw.csv')

