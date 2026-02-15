import pandas as pd
import json
import pprint 
import data_cleaning

json_path = "./Files for Miniproject-1/Weather_AQI_feed.json"

#Make a dict based on schema we created. We've decided to also add wind speed.
#first state all the columns you need
environment_dict = {"District_ID":[],"AQI":[], "AQI_category":[], "Temperature_C":[], "Humidity(%)":[], "Precip_mm":[], "Wind_speed(km/h)":[]} 

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    data_districts = data['districts']

    for district in data_districts:
        #Get all the data from json (old version)
        """
        d_ID = district["District_ID"]
        aqi = district["aqi"]["aqi"]
        aqi_cat = district["aqi"]["category"]
        temp = district["weather"]["temp_c"]
        humi = district['weather']["humidity_percent"]
        p_mm = district["weather"]["precip_mm"]
        wind = district['weather']['wind_speed_kmh'] #Gave me an error. wind_speed_kmh does not exists in the last dict in the list.
        """
        #new version
        d_ID = district.get("District_ID")
        aqi = district.get("aqi", {}).get("aqi")
        aqi_cat = district.get("aqi", {}).get("category")
        temp = district.get("weather", {}).get("temp_c")
        humi = district.get("weather", {}).get("humidity_percent")
        p_mm = district.get("weather", {}).get("precip_mm")
        wind = district.get("weather", {}).get("wind_speed_kmh")

        #appending extract datas
        environment_dict["District_ID"].append(d_ID)
        environment_dict["AQI"].append(aqi)
        environment_dict["AQI_category"].append(aqi_cat)
        environment_dict["Temperature_C"].append(temp)
        environment_dict["Humidity(%)"].append(humi)
        environment_dict["Precip_mm"].append(p_mm)
        environment_dict['Wind_speed(km/h)'].append(wind)

#transform to df and then csv
print("Success Extracing Datas")
df = pd.DataFrame(environment_dict)
df_dropped_duplicates = data_cleaning.drop_duplicate(df)

print("Now saving to CSV file...")
df_dropped_duplicates.to_csv('Environment.csv', index=False)
#print(df_dropped_duplicates)
print("Done")




"""
Documentation/Reflection note

-Was able to open json file easily.

-We decided to first create code to retrieve information from JSON, 
and then later create code to handle errors such as missing data.

-The info we want to get was in the list, which is the value for
key 'districts'. Since it is in the list, we used loop to access each
element and get the data.

-First, we extract each value into a corresponding variable, then
we add those variables to the dict. We did it this way because it was hard
to read the code when we did everything all at once.

-At first, we accessed the JSON fields using bracket notation, like 
district["weather"]["wind_speed_kmh"]. 
But this caused a KeyError when the key was missing, so we switched to using 
the .get() method, which safely returns None instead of raising an exception.

"""