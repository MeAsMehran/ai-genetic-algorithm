# algorithm.py

import random
from config import (
    POP_SIZE, NUM_GENERATIONS, TOURNAMENT_SIZE,
    CROSSOVER_RATE, MUTATION_RATE, NUM_GENES
)
from model import fitness_of, Q_final, C_norm
from utils import random_chromosome, repair_chromosome, save_plot, save_bar_chart


# --------------------------
# انتخاب تورنومنت
# --------------------------
def tournament_selection(pop, fitnesses):
    cand = random.sample(range(len(pop)), TOURNAMENT_SIZE)
    best = max(cand, key=lambda i: fitnesses[i])
    return pop[best][:]


# --------------------------
# BLX-alpha crossover (بهترین برای بردارهای حقیقی)
# --------------------------
def blx_alpha_crossover(p1, p2, alpha=0.4):
    if random.random() > CROSSOVER_RATE:
        return p1[:], p2[:]

    c1 = []
    c2 = []

    for a, b in zip(p1, p2):
        low = min(a, b)
        high = max(a, b)
        d = high - low
        min_range = low - alpha*d
        max_range = high + alpha*d

        c1.append(random.uniform(min_range, max_range))
        c2.append(random.uniform(min_range, max_range))

    return repair_chromosome(c1), repair_chromosome(c2)


# --------------------------
# جهش قوی Gaussian
# --------------------------
def mutate(chrom, sigma=12):
    for i in range(NUM_GENES):
        if random.random() < MUTATION_RATE:
            chrom[i] += random.gauss(0, sigma)
    return repair_chromosome(chrom)


# --------------------------
# اجرای یک Run
# --------------------------
def run_ga(run_id=1):
    pop = [random_chromosome() for _ in range(POP_SIZE)]

    history_best = []
    history_mean = []

    best_solution = None
    best_fit = -999999

    for g in range(NUM_GENERATIONS):

        fitnesses = [fitness_of(ind) for ind in pop]

        # ثبت وضعیت
        best_idx = max(range(POP_SIZE), key=lambda i: fitnesses[i])
        bsol = pop[best_idx]
        bfit = fitnesses[best_idx]

        history_best.append(bfit)
        history_mean.append(sum(fitnesses)/POP_SIZE)

        if bfit > best_fit:
            best_fit = bfit
            best_solution = bsol[:]

        # نسل جدید
        new_pop = []
        while len(new_pop) < POP_SIZE:
            p1 = tournament_selection(pop, fitnesses)
            p2 = tournament_selection(pop, fitnesses)
            c1, c2 = blx_alpha_crossover(p1, p2)
            new_pop.append(mutate(c1))
            if len(new_pop) < POP_SIZE:
                new_pop.append(mutate(c2))

        pop = new_pop

    save_plot(history_best, f"Run {run_id} Best Fitness",
              "Generation", "Fitness", f"run_{run_id}_best.png")

    save_plot(history_mean, f"Run {run_id} Mean Fitness",
              "Generation", "Fitness", f"run_{run_id}_avg.png")

    return {
        "best_solution": best_solution,
        "best_fitness": best_fit,
        "best_q": Q_final(best_solution),
        "best_cost": C_norm(best_solution)
    }


# --------------------------
# اجرای 5 بار مستقل
# --------------------------
def run_multiple():
    results = []
    for i in range(1, 6):
        print(f"\nRunning GA (Run {i}) ...")
        results.append(run_ga(i))

    final_fitnesses = [r["best_fitness"] for r in results]
    save_bar_chart(final_fitnesses, "Final Fitness Comparison", "comparison.png")

    return results
