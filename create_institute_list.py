import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

institute_list = {}

with open("all.csv") as all_file, open("institutes.csv", 'w') as institute_file:
    institutes_with_multiples = list(map(
        lambda x: x.strip().split("||| ")[4],
        all_file.readlines()
    ))
    institutes=set(institutes_with_multiples)
    for institute in institutes:
        print(f"{institute}:{institutes_with_multiples.count(institute)}", file=institute_file)
print(institutes)
