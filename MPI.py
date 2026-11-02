
import csv
import os
from multiprocessing import Pool, cpu_count


# Worker function: calculates one row of result matrix
def multiply_row(task):

    row_id, row, matrix_b = task

    print(f"[WORKER] Processing row {row_id}")

    result_row = []

    # Multiply one row of A with every column of B
    for col in range(len(matrix_b[0])):

        dot_product = 0

        for k in range(len(row)):
            dot_product += row[k] * matrix_b[k][col]

        result_row.append(dot_product)

    print(f"[WORKER] Row {row_id} result: {result_row}")

    return row_id, result_row


def main():

    filename = "matrix_22.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    matrix_a = []

    # Read matrix A from CSV
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            values = [
                int(row["col_0"]),
                int(row["col_1"]),
                int(row["col_2"]),
                int(row["col_3"])
            ]

            matrix_a.append(values)

    # Define matrix B
    matrix_b = [
        [1, 2, 0, 1],
        [0, 1, 2, 0],
        [2, 0, 1, 2],
        [1, 1, 0, 1]
    ]

    print("\n========== MPI MATRIX MULTIPLICATION ==========")

    print("\n[MASTER] Matrix A:")
    for row in matrix_a:
        print(row)

    print("\n[MASTER] Matrix B:")
    for row in matrix_b:
        print(row)

    # Scatter: distribute rows to worker tasks
    tasks = [
        (i, matrix_a[i], matrix_b)
        for i in range(len(matrix_a))
    ]

    print("\n[MASTER] Scattering matrix rows to workers...")

    for task in tasks:
        print(f"[SCATTER] Row {task[0]} assigned to worker")

    # Parallel execution
    with Pool(processes=min(len(tasks), cpu_count())) as pool:
        partial_results = pool.map(multiply_row, tasks)

    # Gather: collect worker results
    print("\n[MASTER] Gathering partial results...")

    partial_results.sort(key=lambda x: x[0])

    result_matrix = [
        result for row_id, result in partial_results
    ]

    print("\n[MASTER] Final Matrix Product (A x B):")

    for row in result_matrix:
        print(row)

    print("\n[SUCCESS] Parallel Matrix Multiplication Completed.")
    print("===============================================")


if __name__ == "__main__":
    main()
