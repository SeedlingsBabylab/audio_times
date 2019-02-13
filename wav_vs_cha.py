import pyclan as pc
import pandas as pd
import os


wav_times = pd.read_csv("wav_times.csv")
cha_dir = "data/both_all_ob1fixed"
cha_files = [os.path.join(cha_dir, x)
                for x in os.listdir(cha_dir)
                    if "lena.cha" not in x and not x.startswith(".")]

cha_times = []

for f in cha_files:
    key = os.path.basename(f)[:5]
    print os.path.basename(f)
    cf = pc.ClanFile(f)
    for x in reversed(cf.line_map):
        if x.is_tier_line:
            ts = int(x.timestamp().split("_")[1])
            cha_times.append((key, ts))
            break

cha_times = pd.DataFrame(cha_times, columns=["file", "sparse_code_time"])

cha_times.to_csv("cha_times.csv", index=False)

joined = cha_times.merge(wav_times, on="file")

joined["diff"] = (joined["sparse_code_time"]-joined["wav_time"]).abs()

joined.to_csv("time_diffs.csv", index=False)

print