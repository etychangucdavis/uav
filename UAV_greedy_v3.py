import numpy as np
import pandas as pd
import math
from DefineNode import Node_greedy as Node

class Topology:
  '''
  mode : 拓樸類別
  radius : 黑色節點廣播範圍
  '''
  def __init__(self, mode='square_four', radius=2):
    self.mode = mode
    self.radius = radius
    self.nodes = []
    self.S = []
    self.R = [] # remain
    # 讀取csv
    nodes = pd.read_csv(mode +'.csv')
    nodes = nodes.values.tolist()
    # 紀錄所有節點資訊的list
    for node in nodes:
        id, x, y, color = node
        self.nodes.append(Node(int(id), x, y, int(color)))

  # 初始化每個點的白鄰居表與鄰居表
  def UpdateNeighbor(self):
    self.B_ = [] # black nodes
    for i, node in enumerate(self.nodes):
        for other_node in self.nodes[i+1:]:
            if ComputeDistance(node.x-other_node.x, node.y-other_node.y) <= self.radius:
                # 加入此鄰居至鄰居表中
                node.SetNeighborList(other_node)
                # 鄰居為白色節點，也加入至白鄰居表中
                if not other_node.color :
                    node.SetWhiteNeighborList(other_node)
                # 同時更新該鄰居節點的鄰居表
                other_node.SetNeighborList(node)
                if not node.color :
                    other_node.SetWhiteNeighborList(node)
        # 此節點為黑色節點且有白鄰居則加進B'中
        if node.color and len(node.neighbor_w_list):
            #node.PrintContent()
            self.B_.append(node)    

  # 判斷當前黑色節點是否存在任一白色鄰居
  def CheckWhiteNeighbor(self):
    for node in self.B_:
      if len(node.GetWhiteNeighborList()):
        return True
    return False

  # 執行演算法
  def RunGreedy(self):
    # start from line 5 
    iters = 1
    while(self.CheckWhiteNeighbor()):
      B = self.B_
      self.B_ = []
      every_round = []
      for node in B:
        w_list = node.GetWhiteNeighborList()
        self.R += [w_x for w_x in w_list if w_x not in self.R]
      while self.R :
        max_neighbor = -1
        # argmax|w(x)|
        for node in B:
          #if node.neighbor_w_num > max_neighbor:
          if len(node.GetWhiteNeighborList()) > max_neighbor:
            max_neighbor = len(node.GetWhiteNeighborList())
            x = node
        # S = S Union {x}
        self.S.append(x)
        every_round.append(x)
        # B = B - {x}
        B = [node for node in B if node is not x]
        # color nodes in w(x) as black
        w_x = x.GetWhiteNeighborList()
        for node in w_x:
          node.ToBlack()
        # R = R - w(x)
        self.R = [ _ for _ in self.R if _ not in w_x]
        # B' = B' Union w(x)
        self.B_ += [ _ for _ in w_x if _ not in self.B_]
      print(f' -----{iters}th-----')  
      for node in every_round:
        node.PrintContent()
      iters += 1
    return self.S

# 計算兩點之間的距離
def ComputeDistance(x, y):
    return math.hypot(x, y)

test = Topology(mode='square_four', radius= math.sqrt(2))
test.UpdateNeighbor()
s = test.RunGreedy()

# for node in s:
#    node.PrintContent()