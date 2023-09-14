import multiprocessing
import time
import matplotlib.pyplot as plt
import numpy as np


def compare_dna(healthy_dna, unhealthy_dna, results):
    indices = []
    for x in range(0, len(healthy_dna)):
        if healthy_dna[x] != unhealthy_dna[x]:
            indices.append(x)
    results.put(indices)


if __name__ == '__main__':
    healthy_dna = list(input("Enter the healthy DNA sample: "))
    unhealthy_dna = list(input("Enter the unhealthy DNA sample: "))

    start = time.time()

    blocks = 40
    processes = []
    results = multiprocessing.Queue()

    for x in range(0, len(healthy_dna), blocks):
        h = healthy_dna[x:x + blocks]
        uh = unhealthy_dna[x:x + blocks]
        p = multiprocessing.Process(target=compare_dna, args=(h, uh, results))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end = time.time()
    print("\nProgram executed in", end - start, "second(s)")

    # Collect results from the processes
    diff_indices = []
    while not results.empty():
        diff_indices.extend(results.get())

    # Visualize the differences using Matplotlib
    positions = np.arange(len(healthy_dna))
    healthy = np.array(healthy_dna)
    unhealthy = np.array(unhealthy_dna)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(positions, healthy == unhealthy, color='green', label='Match')
    ax.bar(diff_indices, healthy[diff_indices] != unhealthy[diff_indices], color='red', label='Mismatch')

    ax.set_xlabel('Position in DNA Sequence')
    ax.set_ylabel('Match/Mismatch')
    ax.set_title('DNA Sequence Comparison')
    ax.legend()

    plt.show()
