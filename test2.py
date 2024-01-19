# coding=gbk
import csv
import itertools


def find_record(doi):
    with open('/Users/moqi/Desktop/test_data_01.csv',
              'r',
              encoding='utf-8-sig',
              newline='') as f:
        reader = csv.reader(f)
        # Note:不读标题栏
        next(reader)
        for row in reader:
            temp_doi = row[0]
            if temp_doi == doi:
                return [
                    int(row[1]),
                    int(row[2]),
                    int(row[3]),
                    int(row[4]),
                    int(row[5]),
                    int(row[6]),
                    int(row[7]),
                    int(row[8]),
                    int(row[9]),
                    int(row[10]),
                    int(row[11]),
                    int(row[12]),
                    int(row[13]),
                    int(row[14]),
                    int(row[15]),
                    int(row[17]),
                    int(row[18])
                ]
        return None


def is_match_record(tw_doi, non_tw_doi):
    tw_record = find_record(tw_doi)
    ntw_record = find_record(non_tw_doi)
    return tw_record[:15] == ntw_record[:15]


def get_journals():
    journals = set()
    with open('/Users/moqi/Desktop/test_data_01.csv',
              'r',
              encoding='utf-8-sig',
              newline='') as f:
        reader = csv.reader(f)
        # Note:不读标题栏
        next(reader)
        for row in reader:
            journals.add(row[16])
        return list(journals)


def get_doi():
    dois = set()
    with open('/Users/moqi/Desktop/test_data_01.csv',
              'r',
              encoding='utf-8-sig',
              newline='') as f:
        reader = csv.reader(f)
        # Note:不读标题栏
        next(reader)
        for row in reader:
            dois.add(row[0])
        return list(dois)


def write_items():
    tw_dois = []
    non_tw_dois = []
    with open('/Users/moqi/Desktop/test_data_01.csv',
              'r',
              encoding='utf-8-sig',
              newline='') as f:
        reader = csv.reader(f)
        # Note:不读标题栏
        next(reader)
        for row in reader:
            doi = row[0]
            if int(row[16]) == 1:
                tw_dois.append(doi)
            else:
                non_tw_dois.append(doi)
        match_id = 0
        for [tw_doi, non_tw_doi] in itertools.product(tw_dois, non_tw_dois):
            print('number:', match_id)
            match_id += 1
            if not is_match_record(tw_doi, non_tw_doi):
                print('not matched..................')
                continue
            print('matched: ', match_id, [tw_doi, non_tw_doi])
            # 1.1创建文件对象
            with open('data.csv', 'a') as f:
                # 1.2基于文件对象构建csv写入对象
                writer = csv.writer(f)
                # 1.3构建列表头
                # writer.writerow([
                #     'Tw_doi', 'Non_tw_doi', 'No.tw', 'No.ntw', 'No.ctw',
                #     'No.cntw'
                # ])
                row = []
                row.append(tw_doi)
                row.append(non_tw_doi)
                tw_record = find_record(tw_doi)
                ntw_record = find_record(non_tw_doi)
                row.append(tw_record[15])
                row.append(ntw_record[15])
                row.append(tw_record[16])
                row.append(ntw_record[16])
                for i in range(0, 15):
                    row.append(tw_record[i])
                    row.append(ntw_record[i])
                writer.writerow(row)


# def write_items():
#     journals = get_journals()
#     for journal in journals:
#         tw_dois = []
#         non_tw_dois = []
#         with open('/Users/moqi/Desktop/test_data_01.csv',
#                   'r',
#                   encoding='utf-8-sig',
#                   newline='') as f:
#             reader = csv.reader(f)
#             # Note:不读标题栏
#             next(reader)
#             for row in reader:
#                 if row[16] != journal:
#                     continue
#                 doi = row[0]
#                 if int(row[22]) == 1:
#                     tw_dois.append(doi)
#                 else:
#                     non_tw_dois.append(doi)
#         for [tw_doi, non_tw_doi] in itertools.product(tw_dois, non_tw_dois):
#             print('begin....', journal)
#             if not is_match_record(tw_doi, non_tw_doi):
#                 continue
#             print('test: ', journal, [tw_doi, non_tw_doi])
#             # 1.1创建文件对象
#             with open('data.csv', 'a') as f:
#                 # 1.2基于文件对象构建csv写入对象
#                 writer = csv.writer(f)
#                 # 1.3构建列表头
#                 # writer.writerow([
#                 #     'Tw_doi', 'Non_tw_doi', 'No.tw', 'No.ntw', 'No.ctw',
#                 #     'No.cntw'
#                 # ])
#                 row = []
#                 row.append(tw_doi)
#                 row.append(non_tw_doi)
#                 tw_record = find_record(tw_doi)
#                 ntw_record = find_record(non_tw_doi)
#                 row.append(tw_record[18])
#                 row.append(ntw_record[18])
#                 row.append(tw_record[19])
#                 row.append(ntw_record[19])
#                 writer.writerow(row)

if __name__ == '__main__':
    write_items()
