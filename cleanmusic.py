import pandas as pd
df=pd.read_csv("E:\dv_project\Global_Music_Streaming_Listener_Preferences.csv")
print(df.isnull().sum())