from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
plt.switch_backend('agg')

values = pd.read_csv('results.csv')

websites = values.Website.unique()
delays = np.array(values.Delay.unique())
delays.sort()
bandwidth = np.array(values.Bandwidth.unique())
bandwidth.sort()
fig, ax = plt.subplots(ncols = bandwidth.shape[0],nrows = websites.shape[0], figsize=(30, 15))
x = 0
y = 0
width = 0.35
for website in websites:
    for bw in bandwidth:
        ip = values[values.Website == website]
        ip1 = ip[ip.tcp =='vanilla']
        ip1 = ip1[ip1.Bandwidth == bw]
        ip2 = ip[ip.tcp =='tcp fast_open']
        y_pos = np.arange(ip1.shape[0])
        ip2 = ip2[ip2.Bandwidth == bw]

        rects1 = ax[x][y].bar(y_pos, ip1['Time for transfer'],width, color='g')

        rects2 = ax[x][y].bar(y_pos + width, ip2['Time for transfer'],width, color='b')

        ax[x][y].set_ylabel("Time for transfer")
        ax[x][y].set_xlabel("Delay")
        ax[x][y].set_title(website + " Bandwidth: " + str(bw))
        ax[x][y].set_xticks(y_pos)
        ax[x][y].set_xticklabels(delays)
        ax[x][y].legend((rects1[0], rects2[0]), ('TCP Vanilla', 'TCP Fast Open'))
        y = y + 1
    x = x + 1
    y = 0
plt.tight_layout()
fig.savefig("plots.png")