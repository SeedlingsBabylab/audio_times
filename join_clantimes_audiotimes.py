import pandas as pd


audio_times = pd.read_csv("audiotimes.csv")
clan_times = pd.read_csv("06_07_clantime_11-10-17_with_cex_files.csv")

# joined = audio_times.join(clan_times, on='file')

joined = pd.merge(clan_times, audio_times, left_on="file", right_on='file', how='left')

joined.to_csv("audiotimes_11-10-17_with_cex_files.csv", index=False)