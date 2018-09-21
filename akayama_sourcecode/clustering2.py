import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

#getfeatureによって作られたcsvファイルからk-means法によりクラスタリングする
#csvファイル
csv='team000-answer_log2.csv'
#出力ファイル（入力ファイルの最後にクラスターナンバーがある）
out='output.csv'



data=pd.read_csv(csv,index_col=0)

sc = StandardScaler()
data_sc=sc.fit_transform(data)

mms=MinMaxScaler()
data_mms=mms.fit_transform(data_sc)

pred=KMeans(n_clusters=8).fit_predict(data_mms)

data['cluster']=np.array(pred)

data.to_csv(out)

print(pred)
