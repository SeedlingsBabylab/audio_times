import pandas as pd
import csv
import sys


def process_df(path):
    stamps = {}
    with open(path, "rU") as input:
        reader = csv.reader(input)
        reader.next()
        for row in reader:
            if row[1]:
                temp_stamps = [x.strip() for x in row[1].split("--")]
                temp_stamps.sort(key = lambda x: int(x.split("_")[0]))
                stamps[row[0]] = temp_stamps
            else:
                stamps[row[0]] = []
    return stamps


if __name__ == "__main__":

    df1 = sys.argv[1]
    df2 = sys.argv[2]

    stamps1 = process_df(df1)
    stamps2 = process_df(df2)

    stamps1_count = sum([len(x) for k, x in stamps1.items()])
    stamps2_count = sum([len(x) for k, x in stamps2.items()])

    end9_count1 = 0
    for k, v in stamps2.items():
        for x in v:
            if x[-1] == "9" or x.split("_")[0][-1] == "9":
                end9_count1 += 1

    end_not09_count = 0
    for k, v in stamps2.items():
        for x in v:
            if x[-1] not in ["9", "0"] or x.split("_")[0][-1] not in ["9", "0"]:
                end_not09_count += 1

    end_0_count = 0
    for k, v in stamps2.items():
        for x in v:
            if x[-1] == "0" and x.split("_")[0][-1] == "0":
                end_0_count += 1

    end_9_and_other_count = 0
    for k, v in stamps2.items():
        for x in v:
            if (x[-1] == "9" and x.split("_")[0][-1] not in  ["9", "0"]) or \
                    (x[-1] not in ["9", "0"] and x.split("_")[0][-1] == "9"):
                end_9_and_other_count += 1
    print
