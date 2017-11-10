from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

values = pd.read_csv('results.csv')

websites = values.Website.unique()
delays = np.array(values.Delay.unique())
delays.sort()
fig, ax = plt.subplots(nrows = websites.shape[0], figsize=(30, 15))
x = 0
width = 0.35

ip1 = values[values.tcp =='vanilla']
ip2 = values[values.tcp =='tcp fast_open']
y_pos = np.arange(ip1.shape[0])

rects1 = ax.bar(y_pos, ip1['Time for transfer'],width, color='g')

rects2 = ax.bar(y_pos + width, ip2['Time for transfer'],width, color='b')

ax.set_ylabel("Time for transfer")
ax.set_xlabel("Delay")
ax.set_title(" Bandwidth: " + str(5))
ax.set_xticks(y_pos)
ax.set_xticklabels(delays)
ax.legend((rects1[0], rects2[0]), ('TCP Vanilla', 'TCP Fast Open'))

plt.tight_layout()
fig.savefig("plots.png")