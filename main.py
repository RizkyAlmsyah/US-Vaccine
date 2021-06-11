#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask
import pandas as pd
import geopandas as gpd

app = Flask(__name__)
@app.route('/daily=doses-country/<nameCountry>', methods=['GET'])
def getDailyDosesCountry(nameCountry):
    df = pd.read_csv('data/us-daily-covid-vaccine-doses-administered.csv')
    df.drop(columns='Code', inplace=True)
    df_daily_doses_country = df.loc[(df['Entity']).str.lower() == str.lower(nameCountry)]
    if df_daily_doses_country.empty:
        return json.dumps({'data': "can't find state " + str(nameCountry)})
    else:
        result = df_daily_doses_country.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)


@app.route('/total-doses-country/<nameCountry>', methods=['GET'])
def getTotalDosesCountry(nameCountry):
    df = pd.read_csv('data/us-total-covid-19-vaccine-doses-administered.csv')
    df.drop(columns='Code', inplace=True)
    df_total_doses_country = df.loc[(df['Entity']).str.lower() == str.lower(nameCountry)]
    if df_total_doses_country.empty:
        return json.dumps({'data': "can't find state " + str(nameCountry)})
    else:
        result = df_total_doses_country.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

@app.route('/vaccines-per-100/<nameCountry>', methods=['GET'])
def getVaccinePer100(nameCountry):
    df = pd.read_csv('data/us-state-covid-vaccines-per-100.csv')
    df.drop(columns='Code', inplace=True)
    df_vaccine_per_100 = df.loc[(df['Entity']).str.lower() == str.lower(nameCountry)]
    if df_vaccine_per_100.empty:
        return json.dumps({'data': "can't find state " + str(nameCountry)})
    else:
        result = df_vaccine_per_100.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

@app.route('/total-people-vaccinated/<nameCountry>', methods=['GET'])
def getTotalPeopleVaccinated(nameCountry):
    df = pd.read_csv('data/us-covid-19-total-people-vaccinated.csv')
    df.drop(columns='Code', inplace=True)
    df_total_people_vaccinated = df.loc[(df['Entity']).str.lower() == str.lower(nameCountry)]
    if df_total_people_vaccinated.empty:
        return json.dumps({'data': "can't find state " + str(nameCountry)})
    else:
        result = df_total_people_vaccinated.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

@app.route('/share-fully-vaccinated/<nameCountry>', methods=['GET'])
def getShareFullyVaccinated(nameCountry):
    df = pd.read_csv('data/us-covid-share-fully-vaccinated.csv')
    df.drop(columns='Code', inplace=True)
    df_share_fully_vaccinated = df.loc[(df['Entity']).str.lower() == str.lower(nameCountry)]
    if df_share_fully_vaccinated.empty:
        return json.dumps({'data': "can't find state " + str(nameCountry)})
    else:
        result = df_share_fully_vaccinated.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

@app.route('/share-vaccine-doses-used/<nameCountry>', methods=['GET'])
def getShareVaccineDosesUsed(nameCountry):
    df = pd.read_csv('data/us-share-covid-19-vaccine-doses-used.csv')
    df.drop(columns='Code', inplace=True)
    df_share_vaccinate_doses = df.loc[(df['Entity']).str.lower() == str.lower(nameCountry)]
    if df_share_vaccinate_doses.empty:
        return json.dumps({'data': "can't find state " + str(nameCountry)})
    else:
        result = df_share_vaccinate_doses.to_json(orient="index")
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

@app.route('/vaccine-state-total-per-day/<date>', methods=['GET'])
def getVaccineStatePerDay(date):
    df = pd.read_csv('data/us-total-covid-19-vaccine-doses-administered.csv')
    df.drop(columns='Code', inplace=True)
    df.rename(columns={'Entity': 'STATE_NAME'}, inplace=True)
    df_perDay = df.loc[(df['Day'] == date)]
    if df_perDay.empty:
        return json.dumps({'data': "can't find date in " + str(date)})
    else:
        df_gd = gpd.read_file('https://docs.mapbox.com/mapbox-gl-js/assets/us_states.geojson')
        df_join = df_gd.merge(df_perDay, how = "left", on = "STATE_NAME")
        result = df_join.to_json()
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)
    
    

app.run()