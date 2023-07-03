import numpy as np
import pandas as pd
Tilt = 0

def change_ang(x):
    if x >180 :
        return x-360
    else:
        return x 

            
df = pd.read_excel(r'.\Results\June30_2023_ADN03_AxisC.xlsx')
df2 =pd.DataFrame()
while (Tilt <= 360):
    if Tilt==0:
        try:
            df2=df2._append((df.loc[(df['Tilt (deg.)']<=0.05)]).iloc[0])
        except IndexError:
            pass
 
    elif Tilt <= 90:
        try:
            df2=df2._append((df.loc[((df['Tilt (deg.)']-Tilt)>= -0.05) & ((df['Tilt (deg.)']-Tilt)<= 0.05)]).iloc[0])           
        except IndexError:
            pass
            
    elif (Tilt>90 and Tilt<270):
        Tilt =270
        try:
            df2=df2._append((df.loc[((df['Tilt (deg.)']-Tilt)>= -0.05) & ((df['Tilt (deg.)']-Tilt)<= 0.05)]).iloc[0])           
        except IndexError:
            pass

    elif Tilt>270:
        try:
            df2=df2._append((df.loc[((df['Tilt (deg.)']-Tilt)>= -0.05) & ((df['Tilt (deg.)']-Tilt)<= 0.05)]).iloc[0])           
        except IndexError:
            pass
        
    Tilt=Tilt+0.5
    print(Tilt)

df2['Tilt (deg.)']=df2['Tilt (deg.)'].apply(change_ang)
df2.to_excel(".\Results\Final_June30_2023_ADN03_AxisC.xlsx", index=False)
plt=df2.plot(x='Tilt (deg.)',y=['Short Circuit Current Primary (mA)', 'Short Circuit Current Redundant (mA)','Current Expected (mA)'],title="Short Circuit Current(mA) v/s Incident Angle(deg)", xlabel="Incident Angle (deg)", ylabel="Short Circuit Current (mA)", legend=(['Short Circuit Current Primary (mA)', 'Short Circuit Current Redundant (mA)','Current Expected (mA)']))
fig = plt.get_figure()
fig.savefig('.\Results\Graph_June30_2023_ADN03_AxisC.jpg')
#plt.savefig(".\Results\Graph_June30_2023_ADN03_AxisC.jpg")    