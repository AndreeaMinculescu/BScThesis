# listen model 1: always attend, no access meaning
# listen model 2: always attend, access meaning
# listen model 3: attend while wandering, access meaning while wandering
# listen model 4: always attend, access meaning while wandering

import matplotlib.pyplot as plt
import statistics
from math import sqrt
from statistics import mean
import os

# compute the number of mind-wandering occurences
def get_count_mw(folder):
    mw_occurences = []
    DIR = "final_data/" + folder
    length = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    for i in range(1, int(length/2+1), 1):
        try:
            name = "final_data/" + folder + "/_trace_00" + str(i) + ".txt"
            f = open(name, "r")
        except FileNotFoundError:
            name = "final_data/" + folder + "/_trace_0" + str(i) + ".txt"
            f = open(name, "r")

        count_mw = 0
        for line in f:
            if "MIND-WANDER" in line:
                count_mw += 1
        mw_occurences.append(count_mw)
    return mw_occurences

# compute the duration of mind-wandering episodes
def get_mean_dur(folder):
    total_dur = []
    DIR = "final_data/" + folder
    length = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    for i in range(1, int(length/2+1), 1):
        try:
            name = "final_data/" + folder + "/_trace_00" + str(i) + ".txt"
            f = open(name, "r")
        except FileNotFoundError:
            name = "final_data/" + folder + "/_trace_0" + str(i) + ".txt"
            f = open(name, "r")
        text_by_line = [line for line in f if "*" in line]

        mw_len = []
        idx = -1
        while idx < len(text_by_line):
            idx += 1
            len_occur_temp = 0
            if idx < len(text_by_line) and "MIND-WANDER" in text_by_line[idx]:
                while idx < len(text_by_line) and "MIND-WANDER" in text_by_line[idx]:
                    len_occur_temp += 1
                    idx += 1
                mw_len.append(float(len_occur_temp))
        try:
            total_dur.append(mean(mw_len))
        except statistics.StatisticsError:
            total_dur.append(0.0)

    return total_dur

# compute confidence interval
def plot_confidence_interval(name, x, values, z=1.96, color='black', horizontal_line_width=0.25):
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    confidence_interval = z * stdev / sqrt(len(values))
    # print(name, values)

    left = x - horizontal_line_width / 2
    top = mean - confidence_interval
    right = x + horizontal_line_width / 2
    bottom = mean + confidence_interval
    plt.plot([top, bottom], [x, x], color=color)
    plt.plot([top, top], [left, right], color=color)
    plt.plot([bottom, bottom], [left, right], color=color)
    plt.plot(mean, x, 'o', color='black')

    return mean, confidence_interval

# main plotting function
def plot(dur=True):
    count_dr = get_count_mw(folder_dr)
    count_mw = get_count_mw(folder_mw)
    count_l1 = get_count_mw(folder_listen_m1)
    count_l2 = get_count_mw(folder_listen_m2)
    count_l3 = get_count_mw(folder_listen_m3)
    count_l4 = get_count_mw(folder_listen_m4)

    mean_dur_dr = get_mean_dur(folder_dr)
    mean_dur_mw = get_mean_dur(folder_mw)
    mean_dur_l1 = get_mean_dur(folder_listen_m1)
    mean_dur_l2 = get_mean_dur(folder_listen_m2)
    mean_dur_l3 = get_mean_dur(folder_listen_m3)
    mean_dur_l4 = get_mean_dur(folder_listen_m4)

    if dur:
        data = [mean_dur_l4, mean_dur_l3, mean_dur_l2, mean_dur_l1, mean_dur_mw, mean_dur_dr]
    else:
        data = [count_l4, count_l3, count_l2, count_l1, count_mw, count_dr]

    fig, ax = plt.subplots()

    ax.axhline(y=1, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=2, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=3, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=4, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=5, color='black', linestyle='--', alpha=0.25)
    ax.axhline(y=6, color='black', linestyle='--', alpha=0.25)

    r = ax.violinplot(data, vert=False, showmeans=False, showextrema=False)
    for pc in r['bodies']:
        pc.set_facecolor('#D3D3D3')
        pc.set_alpha(1)
    if dur:
        ax.set_title("Mean duration of mind-wandering episodes", fontsize=15)
    else:
        ax.set_title("Number of mind-wandering occurences", fontsize=15)

    ax.set_xlabel("Count", fontsize=12)
    plt.xticks(fontsize=11)
    ax.set_yticks([6, 5, 4, 3, 2, 1])
    ax.set_yticklabels(["Baseline\nSalvucci", "Single\n(MW)", "MW+\nListen1", "MW+\nListen2", "MW+\nListen3", "MW+\nListen4"], fontsize=12)

    plot_confidence_interval("Drive", 6, data[5])
    plot_confidence_interval("MW", 5, data[4])
    plot_confidence_interval("Listen_m1", 4, data[3])
    plot_confidence_interval("Listen_m2", 3, data[2])
    plot_confidence_interval("Listen_m3", 2, data[1])
    plot_confidence_interval("Listen_m4", 1, data[0])

    plt.savefig(f"final_data/IMAGES/AllGraphs/Count_mw.png")
    plt.show()

if __name__ == '__main__':
    # folder paths
    folder_dr = "driving"
    folder_mw = "mind_wandering"
    folder_listen_m1 = "listen_m1"
    folder_listen_m2 = "listen_m2"
    folder_listen_m3 = "listen_m3"
    folder_listen_m4 = "listen_m4"

    plot(False)


