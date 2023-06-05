import os
import sqlite3
import logging

from typing import Union

from itertools import combinations

logger = logging.getLogger()
logging.basicConfig()


connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()


def build_db():
    headers = {
        'DokumentID': "STRING PRIMARY KEY",
        'Dokumenttyp': "STRING",
        'Autoren': "STRING",
        'Herausgeber': "STRING",
        'Haupttitel': "STRING",
        'Abstract': "STRING",
        'Auflage': "STRING",
        'Verlagsort': "STRING",
        'Verlag': "STRING",
        'Erscheinungsjahr': "INT",
        'Seitenzahl': "INT",
        'Titel': "STRING",
        'Bandzahl': "INT",
        'ISBN': "STRING",
        'Hochschulschrift': "STRING",
        'Konferenzname': "STRING",
        'QuelleTitel': "STRING",
        'QuelleJahrgang': "INT",
        'QuelleHeftnummer': "INT",
        'QuelleErsteSeite': "INT",
        'QuelleLetzteSeite': "INT",
        'URN': "STRING",
        'DOI': "STRING",
        'Abteilungen': "STRING"}

    sql = f"CREATE TABLE IF NOT EXISTS papers({', '.join([f'{k} {v}' for k, v in headers.items()])});"
    cursor.execute(sql)
    connection.commit()

    count = 0
    err_count = 0

    for file in os.listdir("data"):
        with open(os.path.join("data", file)) as f:
            f.readline()
            for i, line in enumerate(f):
                l = list(map(str.strip, line.split("\t")))
                if len(l) == 24:
                    vals = line.strip().split("\t")
                    sql = "INSERT OR REPLACE INTO papers VALUES (" + 23*"?," + "?);"
                    cursor.execute(sql, l)
                    count += 1
                else:
                    logger.info(f"Length not correct: {len(l)}")
                    err_count += 1
            connection.commit()

    logger.warning(f"Wrote {count} rows, discarded {err_count}")


def query(sql):
    return cursor.execute(sql).fetchall()


def interactive():
    while True:
        prompt = input()
        out = cursor.execute(prompt).fetchall()
        print(out)


def edges_full(where: str):
    sql = f"SELECT Autoren FROM papers WHERE {where};"
    response = cursor.execute(sql).fetchall()
    authors = map(
        lambda x: x[0].split(";"),
        response
    )
    return _edges(authors)


AND = "AND"
OR = "OR"


def edges_simple(mode: Union[AND, OR] = AND,
                 strict: bool = False,
                 *,
                 DokumentID: str = None,
                 Dokumenttyp: str = None,
                 Autoren: str = None,
                 Herausgeber: str = None,
                 Haupttitel: str = None,
                 Abstract: str = None,
                 Auflage: str = None,
                 Verlagsort: str = None,
                 Verlag: str = None,
                 Erscheinungsjahr: int | list[int] = None,
                 Seitenzahl: int | list[int] = None,
                 Titel: str = None,
                 Bandzahl: int | list[int] = None,
                 ISBN: str = None,
                 Hochschulschrift: str = None,
                 Konferenzname: str = None,
                 QuelleTitel: str = None,
                 QuelleJahrgang: int | list[int] = None,
                 QuelleHeftnummer: int | list[int] = None,
                 QuelleErsteSeite: int | list[int] = None,
                 QuelleLetzteSeite: int | list[int] = None,
                 URN: str = None,
                 DOI: str = None,
                 Abteilungen: str = None,
                 ):
    args = locals().copy()
    args.pop("mode")

    int_args = {k : v for (k, v) in args.items() if type(v) == int}
    str_args = {k : v for (k, v) in args.items() if type(v) == str}
    lst_args = {k : v for (k, v) in args.items() if type(v) in (tuple, list, set)}

    conditions = []

    if mode not in {"OR", "AND"}:
        raise ValueError

    for key, val in str_args.items():
        if strict:
            conditions += [f" {key}={val} "]
        else:
            conditions += [f" {key} LIKE '%{val}%' "]
    for key, val in int_args.items():
        conditions += [f" {key}={val} "]
    for key, val in lst_args.items():
        conditions += [f" {key} IN ({','.join(map(str, val))}) "]

    if len(conditions) == 0:
        conditions.append("1=1")

    return edges_full(mode.join(conditions))


def _edges(papers: list[list[str]]):
    edg = set()
    for authors in papers:
        for x, y in combinations(authors, 2):
            edg.add(tuple(sorted((x, y))))
    return edg


if __name__ == "__main__":
    print(edges_full("Autoren LIKE '%Bargheer%' AND Erscheinungsjahr=2021"))

