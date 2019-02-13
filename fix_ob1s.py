import pyclan as pc
import os
import sys

from proportions import *

total_fixed = 0

def process_file(f):
    global total_fixed

    cf = pc.ClanFile(f.file)
    found = False
    for line in cf.line_map:
        if line._has_timestamp:
            ts = line.timestamp().split("_")
            if ts[0][-1] == "9" or ts[1][-1] == "9":
                old_ts = "_".join(ts)
                if ts[0][-1] == "9":
                    ts[0] = str(int(ts[0])+1)
                if ts[1][-1] == "9":
                    ts[1] = str(int(ts[1])+1)
                new_ts = "_".join(ts)
                if new_ts in f.times:
                    if not found:
                        print "**{}**".format(os.path.basename(f.file))
                    found = True
                    line.line = line.line.replace(old_ts, new_ts)
                    total_fixed += 1
                    # print "\t{}".format(ts)
    if found:
        cf.write_to_cha(os.path.join(out_dir, cf.filename))
        print "\t\t\t\ttotal fixed so far: {}".format(total_fixed)


class Group:
    def __init__(self, filepath, timestamps):
        self.file = filepath
        self.times = timestamps


if __name__ == "__main__":
    df1 = sys.argv[1]
    df2 = sys.argv[2]
    cha_dir = [os.path.join(sys.argv[3], x)
                for x in os.listdir(sys.argv[3])
                    if (".lena.cha" not in x and x.endswith(".cha"))]
    out_dir = sys.argv[4]

    stamps1 = process_df(df1)
    stamps2 = process_df(df2)

    chas = {}
    for x in cha_dir:
        key = os.path.basename(x)[:5]
        chas[key] = Group(x, stamps1[key])


    for key, value in chas.items():
        print key
        process_file(value)

    print "\n\n"

    print "total timestamps fixed = {}".format(total_fixed)
    print