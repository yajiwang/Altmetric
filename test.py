# import math
# import os

# def chunks(arr, m):
#     n = int(math.ceil(len(arr) / float(m)))
#     return [arr[i:i + n] for i in range(0, len(arr), n)]

# list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# print(chunks(list, 4))

# file_name = []

# #获取当前目录下的CSV文件名
# def get_csv_name(path):
#     #将当前目录下的所有文件名称读取进来
#     a = os.listdir(path)
#     for j in a:
#         #判断是否为CSV文件, 如果是则存储到列表中
#         if os.path.splitext(j)[1] == '.csv':
#             file_name.append(int(os.path.splitext(j)[0]))

# path = '/Users/moqi/Altmetric/journal/wos/sci/url'
# get_csv_name(path)
# print(file_name)

# csv_file = open('sci.csv', 'w', encoding='utf-8-sig', newline='')
# csv_writer = csv.writer(csv_file)
# for i in range(1, 284):
#     if i in file_name:
#         csv_path = path + '/{}.csv'.format(i)
#         with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
#             reader = csv.reader(f)
#             # Note:标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
#             next(reader)
#             count = 0
#             for row in reader:
#                 count += 1
#             csv_writer.writerow([count])
#     else:
#         csv_writer.writerow([0])
# csv_file.close()

# with open('wos-cited-url-1.csv', 'r', encoding='utf-8-sig', newline='') as f:
#     reader = csv.reader(f)
#     # Note:标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
#     next(reader)
#     count = len(list(reader))
#     print(count)

# 1.测试推文活动是否强相关引用数
# import csv
# import numpy as np
# import statsmodels.api as sm

# X1 = []  # 有推文活动
# X2 = []
# yTest = []
# nSample = 0
# with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
#     reader = csv.reader(f)
#     # Note:不读标题栏
#     next(reader)
#     for row in reader:
#         X1.append(int(row[3]))
#         X2.append(int(row[4]))
#         # if int(row[2]) > 0:
#         #     X1.append(1)
#         # else:
#         #     X1.append(0)
#         yTest.append(int(row[5]))

# nSample = len(yTest)
# print('nSample: ', nSample)

# # 转换为列矩阵
# X1 = np.transpose(X1)
# X2 = np.transpose(X2)
# Y = np.transpose(yTest)

# # 将矩阵按列合并, 即[x1, x2, X3]
# X = np.column_stack((X1, X2))
# # print(X)

# model = sm.NegativeBinomial(endog=Y, exog=X)  # 建立模型
# results = model.fit()  # 返回模型拟合结果
# yFit = results.fittedvalues  # 模型拟合的值
# print(results.summary())  # 输出回归分析的摘要
# print("\nNBR model: ln(Y) = b1*X1 + ... + bm*Xm + alpha")
# print('Parameters: ', results.params)  # 输出：拟合模型的系数

# # 2.测试推文活动(>n)是否强相关引用数
# import csv
# import numpy as np
# import statsmodels.api as sm

# # 1.产生哑变量列表-----------------------------------------------
# def gen_dum_list(m):
#     list = []
#     for i in range(0, m):
#         a = []
#         list.append(a)
#     return list

# # 2.获取m-分位数-----------------------------------------------
# def get_perce(column, m):
#     xTest = []
#     with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
#         reader = csv.reader(f)
#         # Note:不读标题栏
#         next(reader)
#         for row in reader:
#             a = int(row[column])
#             # 不添加重复元素
#             if a > 0 and a not in xTest:
#                 xTest.append(a)
#     xTest.sort()
#     print(xTest)

#     q = []
#     # # m不能超过xTest的元素个数
#     if m > len(xTest):
#         m = len(xTest)
#     start = round(100 / m)
#     print('start:', start)
#     for i in range(1, m):
#         q.append(start * i)
#     perce = np.percentile(xTest, tuple(q), interpolation="midpoint")
#     print('perce:', perce)
#     return perce

# # 获取等距序列(card为基数,如10等)
# def get_equidist(card, m):
#     q = []
#     for i in range(1, m):
#         q.append(card * i)
#     return q

# # 3.获取xTest------------------------------------------------
# def get_xTest(column, m):

#     dum_list = gen_dum_list(m)
#     perce = get_perce(column, m)

#     with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
#         reader = csv.reader(f)
#         # Note:不读标题栏
#         next(reader)
#         for row in reader:
#             a = int(row[column])
#             if a == 0:
#                 for i in range(len(dum_list)):
#                     dum_list[i].append(0)
#             else:
#                 inter = get_interval(a, perce)
#                 for i in range(0, len(dum_list)):
#                     if i == inter:
#                         dum_list[i].append(1)
#                     else:
#                         dum_list[i].append(0)

#     return dum_list

# # 获取a所在的分位数区间
# def get_interval(a, perce):
#     if a <= perce[0]:
#         return 0
#     if a > perce[len(perce) - 1]:
#         return len(perce)
#     for i in range(len(perce)):
#         if a > perce[i - 1] and a <= perce[i]:
#             return i

# # 4.获取负二项回归结果------------------------------------------
# def get_nbr_results(m, *args):

#     dum_list = []
#     for i in range(len(args)):
#         dum_list.extend(get_xTest(args[i], m))
#         print(len(dum_list))

#     dum_tran_list = []
#     for i in range(len(dum_list)):
#         dum_tran_list.append(np.transpose(dum_list[i]))

#     yTest = []
#     with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
#         reader = csv.reader(f)
#         # Note:不读标题栏
#         next(reader)
#         for row in reader:
#             yTest.append(int(row[5]))

#     # 将矩阵按列合并, 即[x1, x2, X3]
#     X = np.column_stack(tuple(dum_tran_list))
#     Y = np.transpose(yTest)

#     model = sm.NegativeBinomial(endog=Y, exog=X)  # 建立模型
#     results = model.fit()  # 返回模型拟合结果
#     print(results.summary())  # 输出回归分析的摘要
#     print("\nNBR model: ln(Y) = b1*X1 + ... + bm*Xm + alpha")
#     print('Parameters: ', results.params)  # 输出:拟合模型的系数

# get_nbr_results(4, 2)

# X1 = []
# X2 = []
# X3 = []
# X4 = []
# X5 = []
# X6 = []
# X7 = []
# X8 = []
# X9 = []
# X10 = []
# xTest = []
# yTest = []

# with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
#     reader = csv.reader(f)
#     # Note:不读标题栏
#     next(reader)
#     for row in reader:
#         a = int(row[2])
#         # 移除重复元素
#         if a > 0 and a not in xTest:
#             xTest.append(a)

# print(xTest)
# # 获取5分位数
# perce = np.percentile(xTest, (10, 20, 30, 40, 50, 60, 70, 80, 90),
#                       interpolation="midpoint")
# print('perce:', perce)

# with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
#     reader = csv.reader(f)
#     # Note:不读标题栏
#     next(reader)
#     for row in reader:
#         a = int(row[2])
#         if a > 0 and a <= perce[0]:
#             X1.append(1)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[0] and a <= perce[1]:
#             X1.append(0)
#             X2.append(1)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[1] and a <= perce[2]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(1)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[2] and a <= perce[3]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(1)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[3] and a <= perce[4]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(1)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[4] and a <= perce[5]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(1)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[5] and a <= perce[6]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(1)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[6] and a <= perce[7]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(1)
#             X9.append(0)
#             X10.append(0)
#         elif a > perce[7] and a <= perce[8]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(1)
#             X10.append(0)
#         elif a > perce[8]:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(1)
#         else:
#             X1.append(0)
#             X2.append(0)
#             X3.append(0)
#             X4.append(0)
#             X5.append(0)
#             X6.append(0)
#             X7.append(0)
#             X8.append(0)
#             X9.append(0)
#             X10.append(0)
#         yTest.append(int(row[5]))

# # 转换为列矩阵
# X1 = np.transpose(X1)
# X2 = np.transpose(X2)
# X3 = np.transpose(X3)
# X4 = np.transpose(X4)
# X5 = np.transpose(X5)
# X6 = np.transpose(X6)
# X7 = np.transpose(X7)
# X8 = np.transpose(X8)
# X9 = np.transpose(X9)
# X10 = np.transpose(X10)
# Y = np.transpose(yTest)

# # 将矩阵按列合并, 即[x1, x2, X3]
# X = np.column_stack((X1, X2, X3, X4, X5, X6, X7, X8, X9, X10))
# # print(X)

# model = sm.NegativeBinomial(endog=Y, exog=X)  # 建立模型
# results = model.fit()  # 返回模型拟合结果
# yFit = results.fittedvalues  # 模型拟合的值
# print(results.summary())  # 输出回归分析的摘要
# print("\nNBR model: ln(Y) = b1*X1 + ... + bm*Xm + alpha")
# print('Parameters: ', results.params)  # 输出:拟合模型的系数
# # print('Parameters: ', round(results.params[0], 4))  # 输出:拟合模型的系数

import csv
import numpy as np
import statsmodels.api as sm

X1 = []
X2 = []
X3 = []
X4 = []
yTest = []
nSample = 0
with open('total.csv', 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    # Note:不读标题栏
    next(reader)
    for row in reader:

        if int(row[2]) > 100:
            X1.append(1)
            X2.append(0)
            X3.append(0)
        elif int(row[2]) <= 100 and int(row[2]) >= 42:
            X1.append(0)
            X2.append(1)
            X3.append(0)
        elif int(row[2]) <= 41 and int(row[2]) >= 1:
            X1.append(0)
            X2.append(0)
            X3.append(1)
        else:
            X1.append(0)
            X2.append(0)
            X3.append(0)

        yTest.append(int(row[5]))

print('X1:', X1)
nSample = len(yTest)
print('nSample: ', nSample)

# 转换为列矩阵
X1 = np.transpose(X1)
X2 = np.transpose(X2)
X3 = np.transpose(X3)
# X4 = np.transpose(X4)
Y = np.transpose(yTest)

# 将矩阵按列合并, 即[x1, x2, X3]
X = np.column_stack((X1, X2, X3))
# print(X)

model = sm.NegativeBinomial(endog=Y, exog=X)  # 建立模型
results = model.fit()  # 返回模型拟合结果
yFit = results.fittedvalues  # 模型拟合的值
print(results.summary())  # 输出回归分析的摘要
print("\nNBR model: ln(Y) = b1*X1 + ... + bm*Xm + alpha")
print('Parameters: ', results.params)  # 输出:拟合模型的系数
