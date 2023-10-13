import os
import json
import shutil
import subprocess
import kaggle
from collections import Counter
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
import plotly.express as px
from utils.country_codes import run_this

#helpers to download dataset

#make sure to have the kaggle.json file in the main directory
# def get_json_data():
#     main_directory = os.path.dirname(os.path.abspath(__file__))
#     json_file_path = os.path.join(main_directory, '../kaggle.json')
#     with open(json_file_path, 'r') as json_file:
#         json_data = json.load(json_file)
#     username = json_data.get('username')
#     key = json_data.get('key')

#     return [username,key]

#helpers to download dataset
# def dataset_download_kaggle(dataset_owner,dataset_name):
    
#     [username,key] = get_json_data()

#     os.environ['KAGGLE_USERNAME'] = username
#     os.environ['KAGGLE_KEY'] = key
#     # Set the directory where you want to download the dataset
#     download_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#     # Download the dataset
#     kaggle.api.dataset_download_files(dataset_owner + '/' + dataset_name, path=download_dir, unzip=True)


  

def geoplot(ddf):
    run_this()
    with open("country_codes.json", "r") as json_file:
        country_codes = json.load(json_file)
    country_with_code, country = {}, {}
    shows_countries = ", ".join(ddf['country'].dropna()).split(", ")
    for c,v in dict(Counter(shows_countries)).items():
        code = ""
        if c.lower() in country_codes:
            code = country_codes[c.lower()]
        country_with_code[code] = v
        country[c] = v

    data = [dict(
            type = 'choropleth',
            locations = list(country_with_code.keys()),
            z = list(country_with_code.values()),
            colorscale = [[0,"rgb(5, 10, 172)"],[0.65,"rgb(40, 60, 190)"],[0.75,"rgb(70, 100, 245)"],\
                        [0.80,"rgb(90, 120, 245)"],[0.9,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
            autocolorscale = False,
            reversescale = True,
            marker = dict(
                line = dict (
                    color = 'gray',
                    width = 0.5
                ) ),
            colorbar = dict(
                autotick = False,
                title = ''),
          ) ]

    layout = dict(
        title = 'The number of content by country',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection = dict(
                type = 'Mercator'
            )
        )
    )

    fig = dict( data=data, layout=layout )
    iplot( fig, validate=False, filename='d3-world-map' )
    return country
  

def convert_duration(s):
  try:
    return int(s.split()[0])
  except ValueError:
    return 0
  

def pre_process(df):
    #Handling Missing Values
    df['country'] = df['country'].fillna(df['country'].mode()[0])
    df['date_added'] = df['date_added'].fillna(df['date_added'].mode()[0])
    df['rating'] = df['rating'].fillna(df['country'].mode()[0])
    df = df.dropna( how='any',subset=['cast', 'director'])
    #Renaming listen in column and retaining only one value
    df = df.rename(columns = {"listed_in":"Genre"})
    df['Genre'] = df['Genre'].apply(lambda x: x.split(",")[0])
    df['Genre'].head()
    df['year_add'] = df['date_added'].apply(lambda x: x.split(" ")[-1])
    df['month_add'] = df['date_added'].apply(lambda x: x.split(" ")[0])
    return df