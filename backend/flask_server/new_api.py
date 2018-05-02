from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
import json
import numpy as np
import os.path
from collections import deque
from graph_tool import Graph
from graph_tool.search import bfs_search, BFSVisitor
from graph_tool.topology import shortest_path
import pickle

app = Flask(__name__)
CORS(app)
api = Api(app)

graph = Graph(directed=False)

graph_picklefile = "fake_graph.pickle"

if os.path.isfile(graph_picklefile):
  print("Reading graph from file")
  with open(graph_picklefile, "rb") as in_file:
    graph = pickle.load(in_file)
else:
  print("Creating graph from data")
  # Read the friendship graph
  graph_data = json.load(open("../facebook_graph.json"))
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

class ShortestPath(Resource):
  class VisitorExample(BFSVisitor):
    def __init__(self, name, pred, dist):
      self.name = name
      self.pred = pred
      self.dist = dist

    def discover_vertex(self, u):
      print("-->", self.name[u], "has been discovered!")

    def examine_vertex(self, u):
      print(self.name[u], "has been examined...")

    def tree_edge(self, e):
      self.pred[e.target()] = int(e.source())
      self.dist[e.target()] = self.dist[e.source()] + 1

  @use_args(shortest_path_args)
  def get(self, args):
    source = int(args["source"])
    target = int(args["target"])
    """
    dist = g.new_vertex_property("int")
    pred = g.new_vertex_property("int")
    bfs_search(graph, graph.vertex(source), VisitExample(v_name, pred, dist))
    return "Finding shortest path from " + str(args["source"]) + " to " + str(args["sink"]) + " has length " + str(self.breadth_first_search(source, sink))
    """
    vertex_list, edge_list = shortest_path(graph, graph.vertex(source), graph.vertex(target))
    print(vertex_list)
    ret = [{"id": graph.vertex_index[v], "name": graph.vertex_properties["name"][v], "photo_filename": graph.vertex_properties["photo_filename"][v]} for v in vertex_list]
    return ret

api.add_resource(ShortestPath, '/shortest_path')
# api.add_resource(CutVertices, '/cut_vertices')

if __name__ == '__main__':
  app.run(debug=True)