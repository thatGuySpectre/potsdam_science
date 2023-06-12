import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


min_papers_per_author=2 # Mindestzahl an Papers für zu berücksichtigende Autor:innen



with open("institutes.csv") as institute_file:
    institutes = list(set(map(
        lambda x: x.strip().split(":")[0],
        institute_file.readlines()
    )))

with open("authors.csv") as authors_file:
    authors_all_with_paper_number = list(map(
        lambda x: x.strip().split(":"),
        authors_file.readlines()
    ))
authors_reduced=list(set([author for author, papers in authors_all_with_paper_number if int(papers)>=min_papers_per_author]))
print(f'number of authors: {len(authors_all_with_paper_number)}, with more than {min_papers_per_author} paper: {len(authors_reduced)}')
#print(authors_reduced)







# ich will ein Dict haben, das mir für einen Autor ein Dict gibt, das die Zahl der Paper dieses Autors pro Institut enthält

# erst mal schauen, was für Paper Andrey Cherstvy geschrieben hat

test_author="Neher"
counter=0
with open("all.csv") as all:
    for line in all.readlines() :
        if test_author in line:
            #print(line)
            counter=counter+1
print(f"total papers by {test_author}: {counter}")

# get number of published papers per author and institute
with open("all.csv") as all:
    # for efficiency, get tuples of authors and institutes once
    paper_authors_institute = list(map(
        lambda x: (x.strip().split("||| ")[0], x.strip().split("||| ")[4].strip()),   #[x.strip().split("||| ")[i] for i in (0,4)],
        all.readlines()
    ))
    author_institute_papers={}
    author_counter=0
    for author in authors_reduced:
        author_counter=author_counter+1
        author_institute_papers[author]=dict([(institute,len([1 for authors1, institute1 in paper_authors_institute if author in authors1 and institute1 == institute])) for institute in institutes])
        if author_counter%100==0:
            print(f"calculating papers per department for author {author_counter}/{len(authors_reduced)}")

            #[dict(institute,len({institute1 for authors1, institute1 in paper_authors_institute if author in authors1 and institute1 == institute})) for institute in institutes]
print(author_institute_papers["Kleinpeter, Erich"])

edges = []

for index_1, institute_1 in enumerate(institutes):
    print(f"calculating department {index_1}...")
    for institute_2 in institutes[index_1+1:]:
        common_author_count=0
        for author in authors_reduced:
            count_1 = author_institute_papers[author][institute_1]
            count_2 = author_institute_papers[author][institute_2]
            common_author_count=common_author_count+min(count_1, count_2)
        if common_author_count>0:
            edges.append((institute_1,institute_2,common_author_count))

        #print(f'{institute_1} x {institute_2}')

print(edges)

with open("department_edges_complete.csv", 'w') as department_edges_file:
    for edge in edges:
        print(f"{edge[0]};{edge[1]};{edge[2]}", file=department_edges_file)

G = nx.Graph();
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

large_threshold=10
elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > large_threshold]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= large_threshold]

pos = nx.kamada_kawai_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=50)

# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1)
nx.draw_networkx_edges(
    G, pos, edgelist=esmall, width=1, alpha=0.5, edge_color="b", style="dashed"
)

# node labels
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
# edge weight labels
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)

#nx.draw_networkx(G, pos=pos, node_size=20, font_size=12, font_weight="light", font_color="red")

plt.show()

# edges: gewichtet, stärke=sum(über autoren) min(veröffentlichungen institut 1, 2)