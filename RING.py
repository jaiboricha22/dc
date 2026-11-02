
import csv
import os

# -----------------------------------
# RING LEADER ELECTION ALGORITHM
# -----------------------------------

def ring_election(nodes):

    node_map = {node["node_id"]: node for node in nodes}

    active_nodes = [
        node for node in nodes if node["is_active"]
    ]

    if not active_nodes:
        print("[ERROR] No active nodes available!")
        return

    current_coordinator = next(
        (node["node_id"] for node in nodes
         if not node["is_active"]),
        None
    )

    print("\n========== RING LEADER ELECTION ==========")

    print("[FAILURE DETECTED] Coordinator has failed.")
    print("Failed Coordinator:", current_coordinator)

    # Select the first active node as initiator
    initiator = min(node["node_id"] for node in active_nodes)

    print(f"\n[INITIATOR] Node {initiator} starts election.")

    # -----------------------------------
    # TOKEN CIRCULATION
    # -----------------------------------

    print("\n[ELECTION] Circulating election token...")

    election_list = []
    current = initiator
    visited = set()

    while current not in visited:

        visited.add(current)

        node = node_map[current]

        if node["is_active"]:

            election_list.append(current)

            print(
                f"[TOKEN] Node {current} passes election token "
                f"to Node {node['next_node_id']}"
            )

        current = node["next_node_id"]

    # -----------------------------------
    # SELECT NEW COORDINATOR
    # -----------------------------------

    new_coordinator = max(election_list)

    print("\n[ELECTION] Active nodes in election:", election_list)

    print(f"[RESULT] Highest ID node: {new_coordinator}")

    # -----------------------------------
    # COORDINATOR ANNOUNCEMENT
    # -----------------------------------

    print("\n[BROADCAST] Circulating COORDINATOR message...")

    current = initiator
    visited.clear()

    while current not in visited:

        visited.add(current)

        if node_map[current]["is_active"]:

            print(
                f"[COORDINATOR] Node {new_coordinator} "
                f"announces leadership to Node {current}"
            )

        current = node_map[current]["next_node_id"]

    print("\n==========================================")
    print(f"[SUCCESS] Node {new_coordinator} elected as LEADER.")
    print("==========================================")


# -----------------------------------
# READ CSV DATASET
# -----------------------------------

def main():

    filename = "ring_nodes_15.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    nodes = []

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            node = {
                "node_id": int(row["node_id"]),
                "next_node_id": int(row["next_node_id"]),
                "is_active": row["is_active"].strip().upper() == "TRUE",
                "priority_rank": int(row["priority_rank"])
            }

            nodes.append(node)

    ring_election(nodes)


# -----------------------------------
# MAIN PROGRAM
# -----------------------------------

if __name__ == "__main__":
    main()
