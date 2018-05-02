from graph_tool import Graph
import numpy as np

used = []
depth = []
visited_list = []

def dfs(g, v, limit):
  used[g.vertex_index[v]] = 1
  visited_list.append(v)
  for to in v.all_neighbors():
    if used[g.vertex_index[to]] == 0:
      depth[g.vertex_index[to]] = depth[g.vertex_index[v]] + 1
      if depth[g.vertex_index[to]] <= limit:
        dfs(g, to, limit)

def dfs_search_with_limit(g, source, limit):
  global used
  used = np.zeros(16000, dtype='int')
  global depth
  depth = np.zeros(16000, dtype='int')
  global visited_list
  visited_list = []
  dfs(g, source, limit)
  return visited_list