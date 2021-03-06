import pyclan as pc
import csv
import os

# start_dir = "data/6_7_lenacha"
start_dir = "data/idslabel_files"


def end_time(filepath):
    clan_file = pc.ClanFile(filepath)
    for line in reversed(clan_file.line_map):
        if not line.is_tier_line:
            continue
        else:
            return line.offset
    print

def sum_time(filepath):
    clan_file = pc.ClanFile(filepath)
    total = 0
    for line in clan_file.line_map:
        if line.is_tier_line:
            total += line.offset - line.onset

    return total


def walk():
    times = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            print file
            path = os.path.join(root, file)
            end = end_time(path)
            # sumd = sum_time(path)
            # print (file[:5], end, sumd)
            # times.append((file[:5], end, sumd))
            times.append((file[:5], end))
    return times




with open("idslabel_bergelson_times.csv", "wb") as out:
    times = walk()
    writer = csv.writer(out)
    # writer.writerow(["file", "end_stamp_lenacha", "sum_stamp_lenacha"])
    writer.writerow(["file", "time"])
    writer.writerows(times)



# clan_file = pc.ClanFile("data/6_7_sparsecode/03_07_sparse_code.cha")

print
