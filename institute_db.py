import sqlite3

connection = sqlite3.connect("intitutes.sqlite")
cursor = connection.cursor()


def create():
    sql = """
    CREATE TABLE IF NOT EXISTS institutes(
    id PRIMARY KEY,
    institute1 STRING,
    institute2 STRING,
    weight INTEGER
    );
    """

    cursor.execute(sql)

    connection.commit()

    with open("department_edges_complete.csv") as f:
        edges = list(map(lambda x: x.strip().split(";"), f.readlines()))
        edges = [(i, j, int(k)) for (i, j, k) in edges]

        sql = """
        INSERT INTO institutes(institute1, institute2, weight) VALUES (?,?,?)
        """

        for edge in edges:
            cursor.execute(sql, edge)

        connection.commit()


def interactive():
    while True:
        key = input()
        sql = f"SELECT * FROM institutes WHERE {key};"

        values = cursor.execute(sql).fetchall()

        print(values)


if __name__ == "__main__":
    interactive()
