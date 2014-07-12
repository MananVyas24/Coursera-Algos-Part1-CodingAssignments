"""
The file contains the edges of a directed graph. Vertices are labeled as positive integers from 1 to 875714.
Every row indicates an edge, the vertex label in first column is the tail and the vertex label in second column is the head
(recall the graph is directed, and the edges are directed from the first column vertex to the second column vertex).
So for example, the 11th row looks likes : "2 47646". This just means that the vertex with label 2 has an outgoing edge
to the vertex with label 47646.

Your task is to code up the algorithm from the video lectures for computing strongly connected components (SCCs),
and to run this algorithm on the given graph.

Output Format: You should output the sizes of the 5 largest SCCs in the given graph, in decreasing order of sizes,
separated by commas (avoid any spaces). So if your algorithm computes the sizes of the five largest SCCs to be
500, 400, 300, 200 and 100, then your answer should be "500,400,300,200,100". If your algorithm finds less than 5 SCCs,
then write 0 for the remaining terms. Thus, if your algorithm computes only 3 SCCs whose sizes are 400, 300, and 100,
then your answer should be "400,300,100,0,0".
434821,968,459,313,211
"""

import zipfile
import os
import sys


def initialize_input(filename):
    extracted_filename = os.getcwd() + os.sep + "SCC.txt"

    if os.path.isfile(extracted_filename):
        os.unlink(extracted_filename)

    with zipfile.ZipFile(filename, 'r') as z:
        z.extractall()

    with open(extracted_filename, 'r') as file:
        print("Reading from input file to memory...")
        file_content = file.readlines()
    print("Done.")

    if os.path.isfile(extracted_filename) and file.closed:
        os.unlink(extracted_filename)

    input_vertices = {}
    number_of_ticks = int(len(file_content) / 100000)
    lines_per_tick = int(len(file_content) / number_of_ticks)
    print("Processing input data...")
    for index, line in enumerate(file_content):
        if index > 0 and index % lines_per_tick == 0:
            print(int(((index / lines_per_tick) / number_of_ticks) * 100), "% done.")

        row = line.split()
        start_vertex_id, end_vertex_id = int(row[0]), int(row[1])

        if start_vertex_id in input_vertices:
            start_vertex = input_vertices[start_vertex_id]
        else:
            start_vertex = Vertex(start_vertex_id)
            input_vertices[start_vertex_id] = start_vertex

        if end_vertex_id in input_vertices:
            end_vertex = input_vertices[end_vertex_id]
        else:
            end_vertex = Vertex(end_vertex_id)
            input_vertices[end_vertex_id] = end_vertex

        start_vertex.outgoing.add(end_vertex)
        end_vertex.incoming.add(start_vertex)

    return sorted(input_vertices.values(), key=lambda vertex: vertex.vertex_id)


class Vertex(object):

    def __init__(self, vertex_id):
        self._vertex_id = vertex_id
        self.incoming = set()
        self.outgoing = set()
        self.explored = False
        self.finish_time = 0

    @property
    def vertex_id(self):
        return self._vertex_id

    def __eq__(self, another_vertex):
        return self._vertex_id == another_vertex._vertex_id

    def __hash__(self):
        return hash(self._vertex_id)


if len(sys.argv) > 1:
    init_vertices = initialize_input(sys.argv[1])

    print("Number of vertices in graph: " + str(len(init_vertices)))
    print("Running DFS-Loop on reversed graph to assign finish times to nodes...")

    finish_time = 0
    for v in reversed(init_vertices):
        if not v.explored:
            # had to implement non-recursive Depth-First search
            # cause recursive calls fail with "stack level too deep" error
            vertex_stack = [v]
            while len(vertex_stack) != 0:
                vertex = vertex_stack[-1]
                vertex.explored = True
                pushed_new_vertex_to_stack = False
                for start_vertex in vertex.incoming:
                    if not start_vertex.explored:
                        vertex_stack.append(start_vertex)
                        pushed_new_vertex_to_stack = True
                        break
                if pushed_new_vertex_to_stack:
                    continue
                vertex_stack.pop()
                finish_time += 1
                vertex.finish_time = finish_time

    # We could maintain separate queue which could collect graph nodes when they are assigned a finish time
    # to avoid additional sorting here which of course increases the running time of the algorithm.
    # But we'll keep this code just for simplicity having in mind that it's possible to get rid of it when necessary.
    print("Sorting vertices by finish time...")
    init_vertices.sort(key=lambda vertex: vertex.finish_time)

    # mark all vertices unexplored again
    for vertex in init_vertices:
        vertex.explored = False

    print("Running DFS-Loop on direct graph and counting SCCs sizes...")
    scc_sizes = []
    for v in reversed(init_vertices):
        if not v.explored:
            vertex_stack = [v]
            scc_size = 0
            while len(vertex_stack) != 0:
                vertex = vertex_stack[-1]
                vertex.explored = True
                pushed_new_vertex_to_stack = False
                for end_vertex in vertex.outgoing:
                    if not end_vertex.explored:
                        vertex_stack.append(end_vertex)
                        pushed_new_vertex_to_stack = True
                        break
                if pushed_new_vertex_to_stack:
                    continue
                vertex_stack.pop()
                scc_size += 1
            scc_sizes.append(scc_size)

    while len(scc_sizes) < 5:
        scc_sizes.append(0)

    scc_sizes.sort(reverse=True)
    print("Got sizes of 5 biggest SCCs: " + ",".join(map(str, scc_sizes[0:5])))
else:
    print("File name of a ZIP archive should be specified as the only one argument!")