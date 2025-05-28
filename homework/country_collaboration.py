
import os

import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore
import pandas as pd  # type: ignore

def load_affiliations():
    """Carga el archivo scopus-papers.csv y retorna un dataframe con
    la columna 'Affiliations'"""

    dataframe = pd.read_csv(
        (
            "https://raw.githubusercontent.com/jdvelasq/datalabs/"
            "master/datasets/scopus-papers.csv"
        ),
        sep=",",
        index_col=None,
    )[["Affiliations"]]
    return dataframe


def remove_na_rows(affiliations):
    """Elimina las filas con valores nulos en la columna 'Affiliations'"""

    affiliations = affiliations.copy()
    affiliations = affiliations.dropna(subset=["Affiliations"])

    return affiliations


def create_countries_column(affiliations):
    """Transforma la columna 'Affiliations' a una lista de paises."""

    affiliations = affiliations.copy()
    affiliations["countries"] = affiliations["Affiliations"].copy()
    affiliations["countries"] = affiliations["countries"].str.split(";")
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y.split(",") for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y[-1].strip() for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(set)
    affiliations["countries"] = affiliations["countries"].map(sorted)
    affiliations["countries"] = affiliations["countries"].str.join(", ")

    return affiliations

def count_country_frequency(affiliations):
    """Cuenta la frecuencia de cada país en la columna 'countries'"""

    countries = affiliations["countries"].copy()
    countries = countries.str.split(", ")
    countries = countries.explode()
    countries = countries.value_counts()
    #
    countries.to_csv("files/countries.csv")
    #
    return countries


def make_plot(n_countries):
    """Función principal"""

    if not os.path.exists("files"):
        os.makedirs("files")

    affiliations = load_affiliations()
    affiliations = remove_na_rows(affiliations)
    affiliations = create_countries_column(affiliations)
    countries_frequency = count_country_frequency(affiliations)


if __name__ == "__main__":
    make_plot(n_countries=20)