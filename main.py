#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask
import pandas as pd

app = Flask(__name__)
@app.route('/dailyDosesCountry/<nameCountry>', methods=['GET'])
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


@app.route('/totalDosesCountry/<nameCountry>', methods=['GET'])
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

@app.route('/totalPeopleVaccinated/<nameCountry>', methods=['GET'])
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

@app.route('/shareFullyVaccinated/<nameCountry>', methods=['GET'])
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

@app.route('/shareVaccineDosesUsed/<nameCountry>', methods=['GET'])
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

app.run()