import os
import pandas as pd


def generate_file_name(prefix: str, extension: str) -> str:
    return prefix + "_" + extension


def delete_file(file_path: str, file_name: str) -> None:
    os.remove(file_name)
    os.remove(file_path)


def find_by_city_name(city):
    df = pd.read_csv("files/iata_codes_db.csv", sep=",", engine="python")
    results = df[df["City"].str.contains(city)]
    res = results.to_dict("records")
    return res[0]['iata code']


def find_by_airport_name(airport):
    df = pd.read_csv("files/iata_codes_db.csv", sep=",", engine="python")
    results = df[df["Airport"].str.contains(airport)]
    res = results.to_dict("records")
    return res[0]['iata code']
