# main.py

from algorithm import run_multiple

if __name__ == "__main__":
    results = run_multiple()

    print("\n============================")
    print("      Final Results")
    print("============================")

    for i, r in enumerate(results, 1):
        print(f"\n--- Run {i} ---")
        print("Best Chromosome:", [round(x,3) for x in r["best_solution"]])
        print("Fitness:", round(r["best_fitness"], 6))
        print("Q:", round(r["best_q"], 6))
        print("Cost:", round(r["best_cost"], 6))

    print("\n All the graphs are saved in the 'plots' directory. BINGOO!\n")
