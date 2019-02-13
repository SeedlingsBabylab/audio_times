import pyclan as pc
import os
import csv
import filegrouper as fg
import re


grouper = fg.FileGrouper(
    "data/both_all_ob1fixed", types=[fg.lena_cha, fg.clan_sparsecode,
                            fg.clan_final, fg.clan_chi_checked,
                            fg.newclan_merged, fg.newclan_merged_final])

# grouper = fg.FileGrouper("test_data", types = [fg.lena_cha, fg.clan_sparsecode])


silstart_rgx = re.compile(
    "starts at ([+-]?\\d*\\.\\d+)(?![-+0-9\\.]) -- previous timestamp adjusted: was (\\d+)")
silstart_rgx2 = re.compile(
    "starts at (\\d+) -- previous timestamp adjusted: was (\\d+)")
silend_rgx = re.compile(
    "ends at ([+-]?\\d*\\.\\d+)(?![-+0-9\\.]) -- previous timestamp adjusted: was (\\d+)")
silend_rgx2 = re.compile(
    "ends at (\\d+) -- previous timestamp adjusted: was (\\d+)")

comment_ts = []
sil_comms = []
subr_comms = []
discreps = []


def process_comments(comms):
    for com in comms:
        if "silence" in com.line:
            m = silstart_rgx.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in sil_comms:
                    sil_comms.append(entry)
                continue
            m = silstart_rgx2.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in sil_comms:
                    sil_comms.append(entry)
                continue

            m = silend_rgx.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in sil_comms:
                    sil_comms.append(entry)
                continue
            m = silend_rgx2.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in sil_comms:
                    sil_comms.append(entry)
                continue

        if "subregion" in com.line:
            m = silstart_rgx.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in subr_comms:
                    subr_comms.append(entry)
                continue
            m = silstart_rgx2.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in subr_comms:
                    subr_comms.append(entry)
                continue

            m = silend_rgx.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in subr_comms:
                    subr_comms.append(entry)
                continue
            m = silend_rgx2.search(com.line)
            if m:
                entry = (int(float(m.group(1))), int(m.group(2)))
                if entry not in subr_comms:
                    subr_comms.append(entry)
                continue


for prefix, group in grouper.groups():
    print prefix
    if group.clan_sparsecode:
        sparsecode = pc.ClanFile(group.clan_sparsecode)
    elif group.clan_final:
        sparsecode = pc.ClanFile(group.clan_final)
    elif group.clan_chi_checked:
        sparsecode = pc.ClanFile(group.clan_chi_checked)
    elif group.newclan_merged:
        sparsecode = pc.ClanFile(group.newclan_merged)
    elif group.newclan_merged_final:
        sparsecode = pc.ClanFile(group.newclan_merged_final)
    else:
        raise Exception()

    sparsecode.flatten()
    # sparsecode.write_to_cha("test.cha")
    lenacha = pc.ClanFile(group.lena_cha)

    sc_comments = sparsecode.get_user_comments()
    lena_comments = lenacha.get_user_comments()

    process_comments(sc_comments)

    sparsecode_lines = set(["{}_{}".format(x.onset, x.offset)
                            for x in sparsecode.line_map if x.is_tier_line])
    lenacha_lines = set(["{}_{}".format(x.onset, x.offset)
                         for x in lenacha.line_map if x.is_tier_line])

    sc_onsets = [int(x.split("_")[0]) for x in sparsecode_lines]
    lena_onsets = [int(x.split("_")[0]) for x in sparsecode_lines]

    sil_comms_new = [x[0] for x in sil_comms]
    sil_comms_old = [x[1] for x in sil_comms]

    subr_comms_new = [x[0] for x in subr_comms]
    subr_comms_old = [x[1] for x in subr_comms]

    discrep_lena_temp = lenacha_lines - sparsecode_lines
    onsets = [x.split("_")[0] for x in discrep_lena_temp]

    discrep_lena = []
    for x in discrep_lena_temp:
        offset = int(x.split("_")[1])
        if  offset not in sil_comms_old and offset not in subr_comms_old:
            discrep_lena.append(x)

    discrep_sparse = []
    discrep_sparse_temp = sparsecode_lines - lenacha_lines
    for x in discrep_sparse_temp:
        offset = int(x.split("_")[1])
        if offset not in sil_comms_new and offset not in subr_comms_new:
            discrep_sparse.append(x)

    result = (prefix, discrep_lena, discrep_sparse)
    print result
    discreps.append(result)


with open("all_discrep_in_lena_notin_sparse_ob1fixed.csv", "wb") as out:
    writer = csv.writer(out)
    writer.writerow(["file", "problem_timestamps"])
    for x in discreps:
        writer.writerow([x[0], " -- ".join(x[1])])

with open("all_discrep_in_sparse_notin_lena_ob1fixed.csv", "wb") as out:
    writer = csv.writer(out)
    writer.writerow(["file", "problem_timestamps"])
    for x in discreps:
        writer.writerow([x[0], " -- ".join(x[2])])
