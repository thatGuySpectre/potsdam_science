import os
import sqlite3
import logging

from itertools import combinations

logger = logging.getLogger()
logging.basicConfig()


connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()


def read():
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


def interactive():
    while True:
        prompt = input()
        out = cursor.execute(prompt).fetchall()
        print(out)


def edges_from_db(where: str):
    sql = f"SELECT Autoren FROM papers WHERE {where};"
    response = cursor.execute(sql).fetchall()
    authors = map(
        lambda x: x[0].split(";"),
        response
    )
    return edges(authors)


def edges(papers: list[list[str]]):
    edg = set()
    for authors in papers:
        for x, y in combinations(authors, 2):
            edg.add(tuple(sorted((x, y))))
    return edg


if __name__ == "__main__":
    print(edges_from_db("Autoren LIKE '%Bargheer%' AND Erscheinungsjahr=2021"))

