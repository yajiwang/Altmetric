# import numpy as np

# a = [3, 6, 8, 9, 1, 2, 4, 23, 45, 12]
# a.sort()
# print(a)
# print(np.percentile(a, (20, 40, 60, 80), interpolation="midpoint"))

import csv
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

xData = []

index = 0
index_list = []
with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    # Note:不读标题栏
    next(reader)
    for row in reader:
        if int(row[2]) == 0:
            continue
        index_list.append(index)
        index += 1
        xData.append(int(row[2]))

X = np.array(xData).reshape(-1, 1)
km = KMeans(n_clusters=3, max_iter=1000).fit(X)
print(index_list)
print(km.cluster_centers_)
#会得出每个sample属于哪一类
y = KMeans(n_clusters=3, max_iter=1000).fit_predict(X)
print(y)
print(len(y))

sci_score = []
for k in range(2, 9):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(X)
    sci_score.append(silhouette_score(X, kmeans.labels_))
print('sci_score: ', sci_score)
plt.plot(range(2, 9), sci_score, 'o-')
plt.xlabel('k')
plt.show()

label_pred = km.labels_  #获取聚类标签
#绘制k-means结果
x0 = X[label_pred == 0]
x1 = X[label_pred == 1]
x2 = X[label_pred == 2]
plt.figure(figsize=(4, 2.3), layout='constrained')
plt.scatter(np.linspace(1, len(x0), len(x0)),
            x0[:, 0],
            c="red",
            marker='o',
            label='label0')
plt.scatter(np.linspace(1, len(x1), len(x1)),
            x1[:, 0],
            c="green",
            marker='*',
            label='label1')
plt.scatter(np.linspace(1, len(x2), len(x2)),
            x2[:, 0],
            c="blue",
            marker='+',
            label='label2')
plt.xlabel('petal length')
plt.ylabel('petal width')
plt.legend(loc=2)
plt.show()

xTest = []
yTest = []
ind = 0
with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    # Note:不读标题栏
    next(reader)
    for row in reader:
        if int(row[2]) == 0:
            xTest.append(0)
        else:
            # 添加类别
            xTest.append(y[ind + 1])
            ind += 1
        yTest.append(int(row[5]))
