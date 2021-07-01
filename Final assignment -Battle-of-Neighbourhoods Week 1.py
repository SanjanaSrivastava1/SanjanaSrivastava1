#!/usr/bin/env python
# coding: utf-8

# #Description of the Problem and Discussion of the Background

# Deciding where to open a new venue in London (outside Inner City Limits)

# London is a great city. It is diverse, multicultural and full of opportunities. But there is also another side to its popularity and appeal. London is an expensive place to live and thrive. Many businesses want to open a venue here and many pay top price to have their window on Piccadilly or Oxford Street. But what about those, who want to start their own business and cannot really afford to open in the City yet? Where is it best to open a new place? Where will it be cheapest and will have enough people living around to be popular? Where the competition is not too overwhelming?
# 
# All these questions and more will be answered below. The whole process will be carried out via the below plan:
# 
# 1.a. Name of the London Boroughs, area and population from web scrapping
# 
# 1.b. Filter the boroughs to get the best candidates for the analysis.
# 
# 1.c. Use Foresquare Data to obtain info about most popular venues.
# 
# 3.a. Maximize the number of clusters.
# 
# 3.b. Visualization using Chloropleth Map
# 
# First time enterpreneurs, who want to start their first business. Below dataset will give a comprehensive insight into where best to open a new venue, to maximise the value for money.
# 
# People who already run a business and want to branch out. Given the extra information, it may provide valuable information before decision making.
# 
# Initial Data Preparation (Week 1) 2.1. Get The Names of Boroughs, Areas, Population, Coordinates from Wikipedia 2.2. Processing the Information From Wiki To Make Necessary Lists 2.3. Check and Compare with Google Search and Refine if Necessary
# First, we get the nessessary information on London Boroughs, dropping the extras, that will not be needed for the analysis.

# In[3]:



from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import requests

url='https://en.wikipedia.org/wiki/List_of_London_boroughs'

LDF=pd.read_html(url, header=0)[0]

LDF.head()


# In[ ]:


LF = LDF.drop(['Status','Local authority','Political control','Headquarters','Nr. in map'], axis=1)
LF['Inner'].replace(np.nan,'0', inplace=True)
LF['Borough'].replace('Barking and Dagenham [note 1]','Barking and Dagenham', inplace=True)
LF['Borough'].replace('Greenwich [note 2]','Greenwich', inplace=True)
LF['Borough'].replace('Hammersmith and Fulham [note 4]','Hammersmith and Fulham', inplace=True)
Inn = ['Camden','Greenwich','Hackney','Hammersmith and Fulham','Islington','Kensington and Chelsea','Lewisham','Lambeth','Southwark','Tower Hamlets','Wandsworth','Westminster']
LF.head()
LF['Inner'] = '0'
LF.head()


# In[ ]:


LF['Inner'] = LF.Borough.isin(Inn).astype(int)
Out = LF[LF.Inner == 0]
Out = Out.drop(['Inner'], axis=1)
df = Out.rename(columns = {"Area (sq mi)": "Area", 
                            "Population (2013 est)[1]":"Population"})
geolocator = Nominatim(user_agent="London_explorer")
df['Co-ordinates']= df['Borough'].apply(geolocator.geocode).apply(lambda x: (x.latitude, x.longitude))
df[['Latitude', 'Longitude']] = df['Co-ordinates'].apply(pd.Series)
df.head()


# In[ ]:


Max_Rent = ['102.25','150.75','97','150.75','118.5','129.25','140','102.25','107.75','140','86','161.5','161.5','140','123.75','134.5','118.5','140','129.25','145.25']
df['Max_Rent'] = Max_Rent

df["Max_Rent"] = pd.to_numeric(df["Max_Rent"])
fin = df[df.Max_Rent <= 125]
fin

Long_list = fin['Longitude'].tolist()
Lat_list = fin['Latitude'].tolist()
print ("Old latitude list: ", Lat_list)
print ("Old Longitude list: ", Long_list)

replace_longitudes = {-106.6621329:0.0799, -2.8417544: 0.1837}
replace_latitudes = {50.7164496:51.6636, 51.0358628: 51.5499}

longtitudes_new = [replace_longitudes.get(n7,n7) for n7 in Long_list]
latitudes_new = [replace_latitudes.get(n7,n7) for n7 in Lat_list]

fin = fin.drop(['Co-ordinates', 'Longitude'], axis=1)

fin['Longitude'] = longtitudes_new
fin['Latitude'] = latitudes_new
fin


# In[ ]:


from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
address = 'London'

geolocator = Nominatim(user_agent="London_explorer")
location = geolocator.geocode(address)
London_latitude = location.latitude
London_longitude = location.longitude
print('The geograpical coordinates of London are {}, {}.'.format(London_latitude, London_longitude))


# In[ ]:



get_ipython().system('pip install folium')
import folium

Fin_Brgh = folium.Map(location=[London_latitude, London_longitude], zoom_start=12)


for lat, lng, label in zip(fin['Latitude'], fin['Longitude'], 
                            fin['Borough']):
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=9,
        popup=label,
        color='Red',
        fill=True,
        fill_color='#Blue',
        fill_opacity=0.7).add_to(Fin_Brgh)
Fin_Brgh

