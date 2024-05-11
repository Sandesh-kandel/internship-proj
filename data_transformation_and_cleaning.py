import pandas as pd

df = pd.read_csv('raw_data.csv')

country_names = []
for index, row in df.iterrows():
    location = row['location']
    location_dict = eval(location)  
    country_names.append(location_dict['countryOrRegion'])

df['location'] = country_names

df.to_csv('modified_data.csv', index=False)
print("The data set where the location colution only has the country names are successfully written to the modified_data.csv")
