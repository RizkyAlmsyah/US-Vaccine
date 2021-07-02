#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify
import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime

from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/daily-doses-country/<nameCountry>', methods=['GET'])
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

@app.route('/total-people-vaccinated/<date>', methods=['GET'])
def getTotalVaccinated(date):
    df = pd.read_csv('data/us-covid-19-total-people-vaccinated.csv')
    df.drop(columns='Code', inplace=True)
    df.rename(columns={'Entity': 'STATE_NAME'}, inplace=True)
    df_perDay = df.loc[(df['Day'] == date)]
    if df_perDay.empty:
        return json.dumps({'data': "can't find date in " + str(date)})
    else:
        df_population = pd.read_csv('data/population.csv')
        df_join_pop = df_perDay.merge(df_population, how = "left", on = "STATE_NAME")
        df_join_pop['Percent'] = df_join_pop['people_vaccinated'] / df_join_pop['Pop'] * 100
        #geo json
        df_gd = gpd.read_file('data/coordinates.geojson')
        df_gd.loc[(df_gd['STATE_NAME']).str.lower() == str.lower('new york'), 'STATE_NAME'] = 'New York State'
        df_join = df_gd.merge(df_join_pop, how = "left", on = "STATE_NAME")
        result = df_join.to_json()
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

@app.route('/share-people-vaccinated/<date>', methods=['GET'])
def getShareVaccinated(date):
    df = pd.read_csv('data/us-covid-19-share-people-vaccinated.csv')
    df.drop(columns='Code', inplace=True)
    df.rename(columns={'Entity': 'STATE_NAME'}, inplace=True)
    df_perDay = df.loc[(df['Day'] == date)]
    if df_perDay.empty:
        return json.dumps({'data': "can't find date in " + str(date)})
    else:
        df_gd = gpd.read_file('data/coordinates.geojson')
        df_join = df_gd.merge(df_perDay, how = "left", on = "STATE_NAME")
        result = df_join.to_json()
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)


@app.route('/total-people-fully-vaccinated/<date>', methods=['GET'])
def getTotalFullyVaccinated(date):
    df = pd.read_csv('data/us-covid-number-fully-vaccinated.csv')
    df.drop(columns='Code', inplace=True)
    df.rename(columns={'Entity': 'STATE_NAME'}, inplace=True)
    df_perDay = df.loc[(df['Day'] == date)]
    if df_perDay.empty:
        return json.dumps({'data': "can't find date in " + str(date)})
    else:
        df_population = pd.read_csv('data/population.csv')
        df_join_pop = df_perDay.merge(df_population, how = "left", on = "STATE_NAME")
        df_join_pop['Percent'] = df_join_pop['people_fully_vaccinated'] / df_join_pop['Pop'] * 100
        #geo json
        df_gd = gpd.read_file('data/coordinates.geojson')
        df_gd.loc[(df_gd['STATE_NAME']).str.lower() == str.lower('new york'), 'STATE_NAME'] = 'New York State'
        df_join = df_gd.merge(df_join_pop, how = "left", on = "STATE_NAME")
        result = df_join.to_json()
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)
    
@app.route('/share-people-fully-vaccinated/<date>', methods=['GET'])
def getSharePeopleFullyVaccinated(date):
    df = pd.read_csv('data/us-covid-share-fully-vaccinated.csv')
    df.drop(columns='Code', inplace=True)
    df.rename(columns={'Entity': 'STATE_NAME'}, inplace=True)
    df_perDay = df.loc[(df['Day'] == date)]
    if df_perDay.empty:
        return json.dumps({'data': "can't find date in " + str(date)})
    else:
        df_gd = gpd.read_file('data/coordinates.geojson')
        df_join = df_gd.merge(df_perDay, how = "left", on = "STATE_NAME")
        result = df_join.to_json()
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)

@app.route('/predict-vaccine-total-next-date/<country>/<date>', methods=['GET'])
def getPredictVaccineNextDate(country,date):
    df = pd.read_csv('data/us-total-covid-19-vaccine-doses-administered.csv')
    df.drop(columns='Code', inplace=True)
    df.rename(columns={'Entity': 'STATE_NAME'}, inplace=True)
    df['Day'] = pd.to_datetime(df['Day'])
    df_country = df.loc[(df['STATE_NAME']).str.lower() == str.lower(country)]
    if df_country.empty:
        return json.dumps({'data': "can't find country " + str(country)})
    else:
        #Machine Learning do the works 
        df_country = df_country.set_index('Day')
        X = (df_country.index -  df_country.index[0]).days.to_numpy()
        Y = df_country.total_vaccinations.values
        predict_day = (pd.Timestamp(date) - df_country.index[-1] ).days
        s = len(X) + predict_day
        reg = LinearRegression().fit(X.reshape(-1,1), Y)
        predict_total = reg.predict(np.array(s).reshape(-1,1))
        a = int(predict_total[0])

        #check population
        df_population = pd.read_csv('data/population.csv')
        country_pop = df_population.loc[df_population['STATE_NAME'].str.lower() == str.lower(country) ]
        pop = country_pop.Pop.values
        b = int(pop[0])
        percent = round(a/b * 100)
        if(a <= b):
            return jsonify({'state': country,
                            'date': date,
                            'predict': a,
                            'total population': b,
                            'total vaccine': str(percent) + "%"})
        else:
            return jsonify({'state': country,
                            'date': date,
                            'predict': b,
                            'total population': b,
                            'total vaccine': str(100) + "%" })

        
@app.route('/predict-vaccine-total-next-day/<country>/<days>', methods=['GET'])
def getPredictVaccineNextDay(country,days):
    df = pd.read_csv('data/us-total-covid-19-vaccine-doses-administered.csv')
    df.drop(columns='Code', inplace=True)
    df.rename(columns={'Entity': 'STATE_NAME'}, inplace=True)
    df['Day'] = pd.to_datetime(df['Day'])
    df_country = df.loc[(df['STATE_NAME']).str.lower() == str.lower(country)]
    if df_country.empty:
        return json.dumps({'data': "can't find country " + str(country)})
    else:
        #Machine Learning do the works 
        df_country = df_country.set_index('Day')
        X = (df_country.index -  df_country.index[0]).days.to_numpy()
        Y = df_country.total_vaccinations.values
        s = 149 + int(days)
        reg = LinearRegression().fit(X.reshape(-1,1), Y)
        predict_total = reg.predict(np.array(s).reshape(-1,1))
        a = int(predict_total[0])

        #check population
        df_population = pd.read_csv('data/population.csv')
        country_pop = df_population.loc[df_population['STATE_NAME'].str.lower() == str.lower(country) ]
        pop = country_pop.Pop.values
        b = int(pop[0])
        percent = round(a/b * 100)
        if(a <= b):
            return jsonify({'state': country,
                            'days': days,
                            'predict': a,
                            'total population': b,
                            'total vaccine': str(percent) + "%"})
        else:
            return jsonify({'state': country,
                            'days': days,
                            'predict': b,
                            'total population': b,
                            'total vaccine': str(100) + "%" })


app.run()