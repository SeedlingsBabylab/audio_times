from ffprobe import *
import csv

path = "/Volumes/pn-opus/Seedlings/Subject_Files"

# months = ["06", "07"]
months = "all"


times = []


def correct_month(root):
    split_root_begin = root.split("Home_Visit")[0][:-1]
    root_base = os.path.basename(split_root_begin)
    if root_base[3:5] in months or months == "all":
        return True, root_base[:5]
    return False, root_base[:5]



def walk_tree(path):
    for root, dirs, files in os.walk(path):
        correct, prefix = correct_month(root)
        if "Audio_Files" in root and correct:
            for file in files:
                if file == "{}.wav".format(prefix):
                    pathname = os.path.join(root, file)
                    metadata = FFProbe(pathname)
                    try:
                        length = metadata.streams[0].durationSeconds()
                    except (IndexError):
                        print os.path.join(root, file) + " was a problem file. skipped."
                        continue
                    print "{}: {}".format(file, length)
                    times.append((file, length * 1000))


walk_tree(path)


with open("wav_times.csv", "wb") as out:
    writer = csv.writer(out)
    writer.writerow(["file", "wav_time"])
    writer.writerows(times)
