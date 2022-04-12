import numpy as np
import pandas as pd
import math
import os 
import csv
topology = input("Input the topology type (ex:square_four):")
if os.path.exists(topology) is not True:
  # 自動/手動建立拓樸
  while 1 :
    mode = input("Choose mode (Auto:A ,Manual:M):")
    if mode.lower() in ['a','m']:
      break
  # 拓樸大小
  t_size = int(input("Input the topology size :"))
  with open(topology + '.csv', 'w', newline='') as csvfile:
    # 定義欄位
    fieldnames = ['id', 'x', 'y', 'Color']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    # 自動
    if mode.lower() in ['a']:
      # 正方形中十字的部分是黑色節點
      if topology == 'square_four':
        for i in range(t_size):
          for j in range(t_size):
            if i == t_size//2 or j == t_size//2:
              writer.writerow({'id':int(i*t_size + j + 1), 'x':j, 'y':i, 'Color':1})
            else:
              writer.writerow({'id':int(i*t_size + j + 1), 'x':j, 'y':i, 'Color':0})
      # 正方形中米字的部分是黑色節點
      elif topology == 'square_eight':
        for i in range(t_size):
          for j in range(t_size):
            if i == t_size//2 or j == t_size//2 or j == i or (t_size-j-1) == i:
              writer.writerow({'id':int(i*t_size + j + 1), 'x':j, 'y':i, 'Color':1})
            else:
              writer.writerow({'id':int(i*t_size + j + 1), 'x':j, 'y':i, 'Color':0})
      elif topology == 'triangle':
        # 三頂點位置
        x_ = [0, t_size/2, t_size]
        y_ = [0, t_size * math.sin(math.radians(60)), 0]
        # 重心位置
        G_x = (x_[0] + x_[1] + x_[2])/3 
        G_y = (y_[0] + y_[1] + y_[2])/3
        print(f"G x:{G_x} ,y:{G_y}")
        slope_list = [(y_[0]-G_y)/(x_[0]-G_x), (y_[2]-G_y)/(x_[2]-G_x)]
        # 從三角形底部往上做
        nodes = t_size + 1
        x = 0
        y = 0
        id_count = 1
        while nodes:
          for i in range(nodes):
            slope = (y-G_y)/(x+i-G_x) if x+i-G_x != 0 else 0
            if slope in slope_list or x+i == G_x:
              writer.writerow({'id':id_count, 'x':x+i, 'y':y, 'Color':1})
            else:
              writer.writerow({'id':id_count, 'x':x+i, 'y':y, 'Color':0})
            id_count += 1
          x += 1/2
          y += math.sin(math.radians(60))
          nodes -= 1
    # 手動
    elif mode.lower() in ['m']:
      while 1:
        try:
          id, x, y, color = input("Input ID, x, y and Color :").split(' ')
          id = int(id)
          writer.writerow({'ID':id , 'x':x, 'y':y, 'Color':color})
        # id輸入"end"則結束
        except ValueError as err:
          if 'end' in str(err):
            print("End manual input...")
            break
          else:
            print("That was no valid number. Try again...")