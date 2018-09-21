import scipy.spatial.distance as distance
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import pandas as pd

#datacsvによって作られた距離行列からデンドログラムを作る

#csvファイル
csv='data_git.csv'


data=pd.read_csv(csv,index_col=0)

# 距離ベクトル生成
dArray = distance.squareform(data)

# クラスタリング
result = linkage(dArray, method='average')

# 図示
dendrogram(result,labels=data.index,orientation='right')
plt.show()