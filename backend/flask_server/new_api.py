from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
import json
import numpy as np
import os.path
from collections import deque
from graph_tool import Graph, GraphView
from graph_tool.search import bfs_search, BFSVisitor
from graph_tool.topology import shortest_path
from graph_tool.centrality import betweenness, closeness
from graph_tool.clustering import local_clustering
from graph_tool.topology import label_biconnected_components
import pickle

app = Flask(__name__)
CORS(app)
api = Api(app)

graph = Graph(directed=False)

graph_picklefile = "fake_graph.pickle"

# Load data just in case
graph_data_str = open("../facebook_graph.json")
graph_data = json.load(graph_data_str)

if os.path.isfile(graph_picklefile):
  print("Reading graph from file")
  with open(graph_picklefile, "rb") as in_file:
    graph = pickle.load(in_file)
else:
  print("Creating graph from data")
  # Read the friendship graph
  graph_data = {int(key):value for key, value in graph_data.items()}

  id_map = {}

  v_name = graph.new_vertex_property("string")
  v_photo_filename = graph.new_vertex_property("string")

  # Add vertices to graph
  for key, obj in sorted(graph_data.items()):
    v = graph.add_vertex()
    v_name[v] = obj["name"]
    v_photo_filename[v] = 'profile_images/' + obj["photo_filename"]
    id_map[obj["name"]] = int(key)

  # Add edges to graph
  for my_id, obj in sorted(graph_data.items()):
    for friend_key in obj["friends"]:
      friend_id = int(friend_key)
      graph.add_edge(graph.vertex(my_id), graph.vertex(friend_id))

  graph.vertex_properties["name"] = v_name
  graph.vertex_properties["photo_filename"] = v_photo_filename
  
  # Save graph into pickle file
  with open(graph_picklefile, "wb") as out_file:
    pickle.dump(graph, out_file)
  print("Done creating graph")

shortest_path_args = {
  'source': fields.Integer(required=True),
  'target': fields.Integer(required=True)
}

induced_subgraph_args = {
  'root': fields.Integer(required=True),
  'limit': fields.Integer(required=True)
}

class WholeGraph(Resource):
  def get(self):
    return graph_data

class InducedSubgraph(Resource):
  def set_properties(self, subgraph):
    v_betweenness, e_betweenness = betweenness(subgraph)
    subgraph.vertex_properties["vertex_betweenness"] = v_betweenness
    subgraph.edge_properties["edge_betweenness"] = e_betweenness
    v_closeness = closeness(subgraph)
    subgraph.vertex_properties["closeness"] = v_closeness
    l_clustering = local_clustering(subgraph)
    subgraph.vertex_properties["local_clustering"] = l_clustering
    bicomp, articulation, nc = label_biconnected_components(subgraph)
    subgraph.vertex_properties["articulation"] = articulation
    return subgraph

  @use_args(induced_subgraph_args)
  def get(self, args):
    from depth_first_searcher import dfs_search_with_limit
    root = int(args["root"])
    limit = int(args["limit"])
    vertices = dfs_search_with_limit(graph, graph.vertex(root), limit)
    v_filter = graph.new_vertex_property('bool')
    for v in vertices:
      v_filter[v] = True
    subgraph = GraphView(graph, v_filter)
    from graph_tool.stats import remove_parallel_edges
    remove_parallel_edges(subgraph)
    subgraph = self.set_properties(subgraph)
    from graph_json_builder import create_json_graph
    return create_json_graph(subgraph)

class ShortestPath(Resource):
  @use_args(shortest_path_args)
  def get(self, args):
    source = int(args["source"])
    target = int(args["target"])
    vertex_list, edge_list = shortest_path(graph, graph.vertex(source), graph.vertex(target))
    print(vertex_list)
    ret = [{"id": graph.vertex_index[v], "name": graph.vertex_properties["name"][v], "photo_filename": graph.vertex_properties["photo_filename"][v]} for v in vertex_list]
    return ret

class Test(Resource):
  def get(self):
    return "test"

api.add_resource(ShortestPath, '/shortest_path')
api.add_resource(WholeGraph, '/whole_graph')
api.add_resource(InducedSubgraph, '/induced_subgraph')
api.add_resource(Test, '/test')

# api.add_resource(CutVertices, '/cut_vertices')

if __name__ == '__main__':
  app.run(debug=True)
