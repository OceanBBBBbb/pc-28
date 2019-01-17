import pandas as pd
import numpy
from fbprophet import Prophet

df = pd.read_csv('file/lucky_num.csv')
print(df.head())
m = Prophet()
m.fit(df)