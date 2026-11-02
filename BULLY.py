
import csv
import os

# -----------------------------------
# BULLY LEADER ELECTION ALGORITHM
# -----------------------------------

def bully_election(nodes):

    alive_nodes = [
        node["node_id"]
        for node in nodes
        if node["is_alive"]
    ]

    current_coordinator = next(
        (node["node_id"] for node in nodes
         if node["is_current_coordinator"]),
        None
    )

    print("\n========== TRUSTMESH BULLY ELECTION ==========")

    print("Alive Nodes:", alive_nodes)
    print("Current Coordinator:", current_coordinator)

    if not alive_nodes:
        print("[ERROR] No active nodes available!")
        return

    # Select an alive node to initiate election
    initiator = min(alive_nodes)

    print(f"\n[FAILURE DETECTED] Coordinator Node {current_coordinator} failed.")

    print(f"\n[INITIATOR] Node {initiator} starts election.")

    # Send ELECTION messages to higher ID nodes
    higher_nodes = [
        node_id for node_id in alive_nodes
        if node_id > initiator
    ]

    if not higher_nodes:
        print("[COORDINATOR] No higher active nodes.")
        print(f"[BROADCAST] Node {initiator} is the new COORDINATOR.")
        return

    print("\n[ELECTION] Sending ELECTION messages to higher nodes...")

    responses = []

    for node_id in higher_nodes:
        print(f"[ELECTION] Node {initiator} -> Node {node_id}: ELECTION")
        print(f"[OK] Node {node_id} responds OK")
        responses.append(node_id)

    # Highest alive node becomes coordinator
    new_coordinator = max(alive_nodes)

    print("\n[COORDINATOR] Higher nodes responded OK.")
    print(f"[ELECTION] Highest active node: {new_coordinator}")

    print("\n[BROADCAST] Broadcasting COORDINATOR message...")

    for node_id in alive_nodes:
        if node_id != new_coordinator:
            print(
                f"[COORDINATOR] Node {new_coordinator} "
                f"-> Node {node_id}: COORDINATOR"
            )

    print("\n==============================================")
    print(f"[SUCCESS] Node {new_coordinator} elected as LEADER.")
    print("==============================================")


# -----------------------------------
# READ CSV DATASET
# -----------------------------------

def main():

    filename = "bully_cluster_2.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    nodes = []

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            node = {
                "node_id": int(row["node_id"]),
                "is_alive": row["is_alive"].strip().upper() == "TRUE",
                "is_current_coordinator":
                    row["is_current_coordinator"].strip().upper() == "TRUE"
            }

            nodes.append(node)

    bully_election(nodes)


# -----------------------------------
# MAIN PROGRAM
# -----------------------------------

if __name__ == "__main__":
    main()
