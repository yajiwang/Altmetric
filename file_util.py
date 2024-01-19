import csv
import os


# 1.获取当前目录下的CSV文件名--------------------------------
def get_csv_name(path):
    file_names = []
    #将当前目录下的所有文件名称读取进来
    a = os.listdir(path)
    for j in a:
        #判断是否为CSV文件, 如果是则存储到列表中
        if os.path.splitext(j)[1] == '.csv':
            # 存储是1.csv等
            file_names.append(j)
            # 存储是移除扩展名后的文件名
            # file_name.append(int(os.path.splitext(j)[0]))
    return file_names


# 2.统计每个CSV文件中的行数--------------------------------
def get_csv_rows(path, file_names):
    csv_file = open(path, 'w', encoding='utf-8-sig', newline='')
    csv_writer = csv.writer(csv_file)
    for i in range(1, 284):
        if i in file_names:
            to_csv_file = path + '/{}.csv'.format(i)
            with open(to_csv_file, 'r', encoding='utf-8-sig', newline='') as f:
                reader = csv.reader(f)
                # Note:跳过标题栏
                next(reader)
                # 将reader转为list
                count = len(list(reader))
                csv_writer.writerow([count])
        else:
            csv_writer.writerow([0])
    csv_file.close()
