import numpy as np
import pandas as pd
Tilt = 270
df = pd.read_excel(r'.\Results\May30_2023_ADN01_AxisB_1.xlsx')
df2 =pd.DataFrame()
while (Tilt <= 360):
    if Tilt==0:
        try:
            df2=df2._append((df.loc[(df['Tilt (deg.)']<=0.05)]).iloc[0])
        except IndexError:
            pass
 
    else:
        try:
            df2=df2._append((df.loc[((df['Tilt (deg.)']-Tilt)>= -0.05) & ((df['Tilt (deg.)']-Tilt)<= 0.05)]).iloc[0])
            #print(((df.loc[((df['Tilt (deg.)']-Tilt)>= -0.05) & ((df['Tilt (deg.)']-Tilt)<= 0.05)]).iloc[0]))
        except IndexError:
            pass
    Tilt=Tilt+0.5
    print(Tilt)

df2.to_excel(".\Results\Final_May30_2023_ADN01_AxisB_1.xlsx", index=False)