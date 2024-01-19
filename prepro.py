import csv


# 1.移除Altmetric导出数据中推特为0且发表在非WoS核心期刊的记录
def clear_csv(alt_csv, clc_csv, jou_list):
    # Note:'utf-8-sig'去除'/u'
    with open(alt_csv, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        # Note:标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
        title_row = next(reader)
        clc_file = open(clc_csv, 'a', encoding='utf-8-sig', newline='')
        clc_writer = csv.writer(clc_file)
        clc_writer.writerow(title_row)
        index = 0
        for row in reader:
            print('index: ', index, '------------------------------')
            index += 1
            if row[2].lower() not in jou_list:
                continue
            # Note:从csv读出的数字是字符串
            if int(row[29]) == 0:
                continue
            clc_writer.writerow(row)
        clc_file.close()


# 2.获取WoS核心期刊(SCI-E,SSCI,AH)列表
def get_jou_list(jou_csv):
    jou_list = []
    # Note:'utf-8-sig'去除'/u'
    with open(jou_csv, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        # Note:去掉标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
        next(reader)
        for row in reader:
            jou_list.append(row[0].lower())
    return jou_list


# 3.移除Altmetric导出期刊数据中推特为0或引用为0的记录
def rov_jou_items(jou_csv, rov_csv):
    # Note:'utf-8-sig'去除'/u'
    with open(jou_csv, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        # Note:标题栏~~~~~~~~~~~~~~~~~~~~~~~~~~
        title_row = next(reader)
        rov_file = open(rov_csv, 'a', encoding='utf-8-sig', newline='')
        rov_writer = csv.writer(rov_file)
        rov_writer.writerow(title_row)
        index = 0
        for row in reader:
            print('index: ', index, '------------------------------')
            index += 1
            # Note:从csv读出的数字是字符串
            if int(row[30]) == 0 or int(row[44]) == 0:
                continue
            rov_writer.writerow(row)
        rov_file.close()


if __name__ == '__main__':
    rov_jou_items('/Users/moqi/Altmetric/journal/Scientometrics.csv',
                  '/Users/moqi/Altmetric/journal/Sci.csv')
