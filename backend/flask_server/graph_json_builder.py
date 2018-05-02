def create_json_graph(g):
  ret = {}
  for v in g.vertices():
    ret[g.vertex_index[v]] = {"name": g.vertex_properties["name"][v], "photo_filename": g.vertex_properties["photo_filename"][v], "friends": []}
  for e in g.edges():
    ret[g.vertex_index[e.source()]]["friends"].append(g.vertex_index[e.target()])
    ret[g.vertex_index[e.target()]]["friends"].append(g.vertex_index[e.source()])
  return ret
