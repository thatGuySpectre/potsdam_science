import os
from itertools import combinations


def write_all():

    with open("all.csv", "w") as out:
        for file in os.listdir("data"):
            with open(os.path.join("data", file)) as f:
                out.writelines(
                    map(lambda x: " ||| ".join((x[2], x[3], x[4], x[9], x[23])) + "\n",
                        filter(
                            lambda x: len(x) == 24,
                            map(
                                lambda x: x.strip().split("\t"),
                                f.readlines()[1:])
                        )
                    )
                )


def get_auths():
    authors = {}
    with open("all.csv") as f:
        auths = f.readlines()
        auths = map(
            lambda x: x.strip().split(" ||| ")[0].strip(" ;,").split(";"),
            auths
        )
        auths = map(
            lambda x: set(map(lambda y: y.strip(), x)),
            auths
        )
        for paper in auths:
            for author in paper:
                if author in authors:
                    authors[author] += 1
                else:
                    authors[author] = 1

    remove = []
    add = {}
    for key in authors.keys():
        if "|||" in key:
            new = key.strip("| ")
            if new in authors:
                authors[new] += authors[key]
            add[new] = authors[key]
            remove.append(key)
    for k in remove:
        authors.pop(k)
    authors.update(add)

    with open("authors.csv", "w") as f:
        f.writelines("\n".join(map(lambda x: f"{x[0]}:{x[1]}", authors.items())))


def connections():
    connect = set()

    with open("all.csv") as f:
        all_papers = f.readlines()
    all_papers = map(
        lambda x: x.strip().split(" ||| ")[0].strip(" ;,").split(";"),
        all_papers
    )
    all_papers = map(
        lambda x: set(map(lambda y: y.strip(), x)),
        all_papers
    )

    for paper in all_papers:
        paper_auths = list(map(
            lambda x: x.strip(" |"),
            paper
        ))

        for x, y in combinations(set(paper_auths), 2):
            connect.add(tuple(sorted((x, y))))

    print(connect)
    print(len(connect))


def top_authors(cutoff=5):
    with open("authors.csv") as f:
        auths = map(
            lambda x: x.strip("\n").split(":"),
            f.readlines()
        )
    top_auths = filter(
        lambda x: int(x[1]) > cutoff,
        auths
    )
    with open("top_authors.csv", "w") as f:
        f.write("\n".join(
            [":".join(a) for a in top_auths]
        ))


def top_connections(n=5):
    connect = {}

    with open("top_authors.csv") as f:
        auths = set(map(
            lambda x: x.strip("\n").split(":")[0],
            f.readlines()
        ))

    with open("all.csv") as f:
        info = f.readlines()
    info = map(
        lambda x: x.strip().split(" ||| ")[0].strip(" ;,").split(";"),
        info
    )
    info = map(
        lambda x: set(map(lambda y: y.strip(), x)),
        info
    )

    for paper in info:
        paper_auths = list(map(
            lambda x: x.strip(" |"),
            paper
        ))

        for x, y in combinations(paper_auths, 2):
            if {x, y}.issubset(auths):
                if tuple(sorted((x, y))) in connect:
                    connect[tuple(sorted((x, y)))] += 1
                else:
                    connect[tuple(sorted((x, y)))] = 1

    connect = {i: j for (i, j) in connect.items() if j >= n}

    with open("connections.csv", "w") as f:
        f.write("\n".join(map(
            lambda x: ";".join(x),
            connect
        )))


if __name__ == "__main__":
    top_authors(1)
    top_connections()
