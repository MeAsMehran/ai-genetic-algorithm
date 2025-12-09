# utils.py
import random
import os
import matplotlib.pyplot as plt
from config import NUM_GENES, SUM_CONSTRAINT


def repair_chromosome(chrom):
    s = sum(chrom)
    if s == 0:
        return [SUM_CONSTRAINT/NUM_GENES]*NUM_GENES
    factor = SUM_CONSTRAINT / s
    return [max(0, x*factor) for x in chrom]


def random_chromosome():
    vals = [random.random() for _ in range(NUM_GENES)]
    s = sum(vals)
    return [v/s * SUM_CONSTRAINT for v in vals]


def save_plot(data, title, xlabel, ylabel, filename):
    os.makedirs("plots", exist_ok=True)
    plt.figure()
    plt.plot(data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(f"plots/{filename}")
    plt.close()


def save_bar_chart(values, title, filename):
    os.makedirs("plots", exist_ok=True)
    plt.figure()
    plt.bar(range(1, len(values)+1), values)
    plt.title(title)
    plt.xlabel("Run")
    plt.ylabel("Final Fitness")
    plt.savefig(f"plots/{filename}")
    plt.close()
