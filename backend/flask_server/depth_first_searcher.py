from graph_tool import Graph
import numpy as np

used = []
visited_list = []

def dfs(g, v, limit, d):
  global used
  used[g.vertex_index[v]] = 1
  global visited_list
  visited_list.append(v)
  for to in v.all_neighbors():
    if used[g.vertex_index[to]] == 0:
      if d + 1 <= limit:
        dfs(g, to, limit, d + 1)

def dfs_search_with_limit(g, source, limit):
  global used
  used = np.zeros(16000, dtype='int')
  global depth
  global visited_list
  visited_list = []
  dfs(g, source, limit, 0)
  return visited_list