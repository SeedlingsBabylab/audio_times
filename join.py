import pandas as pd



lenacha = pd.read_csv("lenacha.csv")
sparsecode = pd.read_csv("sparsecode.csv")
wav = pd.read_csv("wav_times.csv")

df = pd.merge(pd.merge(lenacha, sparsecode, on='file'), wav, on="file")

df.to_csv("audiotimes.csv", index=False)
print