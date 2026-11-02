
import csv
import os

def berkeley_algorithm(nodes):

    print("\n========== TRUSTMESH: BERKELEY CLOCK SYNCHRONIZATION ==========")

    healthy_nodes = []
    faulty_nodes = []

    # Poll all node clocks
    print("\n[MASTER] Polling node clock times...")

    for node in nodes:
        print(
            f"[POLL] Node {node['node_id']} "
            f"Clock Time: {node['clock_time_sec']} seconds"
        )

        if node["is_faulty"]:
            faulty_nodes.append(node)
        else:
            healthy_nodes.append(node)

    # Display faulty nodes
    print("\n[FAULT DETECTION] Checking faulty nodes...")

    for node in faulty_nodes:
        print(
            f"[DISCARDED] Node {node['node_id']} "
            f"with time {node['clock_time_sec']} seconds"
        )

    if not healthy_nodes:
        print("[ERROR] No healthy nodes available!")
        return

    # Calculate average time of healthy nodes
    total_time = sum(
        node["clock_time_sec"] for node in healthy_nodes
    )

    average_time = total_time / len(healthy_nodes)

    print("\n[MASTER] Calculating average clock time...")
    print(f"[RESULT] Average Time: {average_time:.2f} seconds")

    # Calculate relative adjustment for each healthy node
    print("\n[SYNCHRONIZATION] Calculating clock adjustments...")

    for node in healthy_nodes:
        adjustment = average_time - node["clock_time_sec"]

        if adjustment > 0:
            action = "FORWARD"
        elif adjustment < 0:
            action = "BACKWARD"
        else:
            action = "NO CHANGE"

        print(
            f"[ADJUSTMENT] Node {node['node_id']}: "
            f"{adjustment:+.2f} seconds ({action})"
        )

    print("\n===============================================================")
    print("[SUCCESS] Berkeley Clock Synchronization Completed.")
    print("===============================================================")


def main():

    filename = "node_clocks_3.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    nodes = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            node = {
                "node_id": row["node_id"],
                "clock_time_sec": float(row["clock_time_sec"]),
                "is_faulty": row["is_faulty"].strip().upper() == "TRUE"
            }

            nodes.append(node)

    berkeley_algorithm(nodes)


if __name__ == "__main__":
    main()
