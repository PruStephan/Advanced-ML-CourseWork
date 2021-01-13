import csv
import xlrd
import pandas
import math

def main():
    paths = ['DataExtracted/kazan_Dataset.xlsx', 'DataExtracted/omsk_Dataset.xlsx', 'DataExtracted/tomsk_Dataset.xlsx']
    field_names = ['post', 'emotion']
    with open('../Train.csv', 'w') as csv_train:
        with open('../Test.csv', 'w') as csv_test:
            writer_train = csv.DictWriter(csv_train, fieldnames=field_names)
            writer_test = csv.DictWriter(csv_test, fieldnames=['post'])
            writer_train.writeheader()
            writer_test.writeheader()
            for path in paths:
                cur_book = pandas.read_excel(path, header=None)
                cur_dict = cur_book.to_dict()
                for i in range(len(cur_dict[0])):
                    post = cur_dict[0][i]
                    emotion = cur_dict[1][i]
                    if not isinstance(emotion, str):
                        writer_test.writerow({'post': post})
                    else:
                        writer_train.writerow({'post': post, 'emotion': emotion})

if __name__ == '__main__':
    main()