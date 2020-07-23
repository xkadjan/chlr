
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


def plot_pearsoncorr(pearsoncorr,label):
    fig, ax = plt.subplots(figsize=[10, 5], dpi=100, facecolor='w', edgecolor='r')
    sb.heatmap(pearsoncorr,
        xticklabels=pearsoncorr.columns,
        yticklabels=pearsoncorr.columns,
        cmap='RdBu_r',
        annot=True,
        linewidth=0.5,
        square=False)
    ax.set_title(label + ' - pearsons correlations', size=10, loc='left')
    fig.tight_layout()

T19 = pd.read_csv(r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - Smartphone\MERENI\200618_psenice\200618_psenice.csv",',')
SPAD = pd.read_csv(r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - Smartphone\MERENI\200618_psenice\SPAD_Psenica.csv",',')

T19.insert(len(T19.columns),'spad',SPAD.spad)
chlr = T19.drop(['variant','leaf','measurement'],axis=1)

pearsoncorr_chlr = chlr.corr(method='pearson')
plot_pearsoncorr(pearsoncorr_chlr,'Chlorophyll')

plants = pd.DataFrame()
for plant in range(90):
    plant = chlr.iloc[(plant*10):(plant*10)+10].mean()
    plants = plants.append(plant,ignore_index=True)
pearsoncorr_plants = plants.corr(method='pearson')
plot_pearsoncorr(pearsoncorr_plants,'Chlorophyll')

plants_selection = plants[['ExG_n','spad']]

plt.plot(chlr.ExG_n)
plt.plot(chlr.spad/50)

plt.plot(chlr.r)
plt.plot(chlr.spad/150)