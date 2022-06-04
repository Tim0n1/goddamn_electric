history_file = 'musicbot/commands/history.txt'
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.ticker import MaxNLocator


current_month = datetime.now().month
previous_month = current_month - 1
if previous_month < 10:
    previous_month = f'0{previous_month}'
if current_month < 10:
    current_month = f'0{current_month}'


def get_month_activity(month):
    l_months = list()
    f = open(history_file, 'r')
    for line in f:

        for i in range(0, len(line)):
            if line[i] == '-':
                if line[i+1:i+3] == month:
                    l_months.append(line)
                    break
    return l_months

def count_daily_activity(month):
    daily_dict = dict()
    for line in month:
        if line[0:2] not in daily_dict.keys():
            daily_dict[line[0:2]] = 1
        else:
            daily_dict[line[0:2]] += 1
    return daily_dict


def make_graph_monthly():
    y1 = [0 for i in range(1, 32)]
    x1 = [i for i in range(1, 32)]
    for k, v in count_daily_activity(get_month_activity(previous_month)).items():
        y1[int(k)] = v
    plt.figure(figsize=(10, 10), facecolor='lightgrey')
    plt.subplot(2, 1, 1)
    plt.title('През миналия месец')
    plt.plot(x1, y1, color='black')
    ax = plt.gca()
    ax.set_facecolor('#BA5E5E')
    plt.ylabel('Общо използвания за деня')
    plt.xlabel('Дата')
    plt.xticks([i for i in range(1, 32) if i%2 == 0])

    plt.subplot(2, 1, 2)
    plt.title('През настоящия месец')
    y2 = [0 for i in range(1, 32)]
    x2 = [i for i in range(1, 32)]
    for k, v in count_daily_activity(get_month_activity(current_month)).items():
        y2[int(k)] = v
    plt.plot(x2, y2, color='black')
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_facecolor('#BA5E5E')
    plt.ylabel('Общо използвания за деня')
    plt.xlabel('Дата')
    plt.xticks([i for i in range(1, 32) if i % 2 == 0])
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.savefig('monthly_statistic.png',dpi=300)



