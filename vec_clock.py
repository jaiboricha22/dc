
import csv
import os

PROCESSES = ["P1", "P2", "P3"]

# Initialize vector clocks
clocks = {
    "P1": [0, 0, 0],
    "P2": [0, 0, 0],
    "P3": [0, 0, 0]
}

# Store messages and event timestamps
messages = {}
event_vectors = {}


def vector_clock(events):

    print("\n========== VECTOR CLOCKS ==========")

    for event in events:

        event_id = event["event_id"]
        process = event["process_id"]
        action = event["event_action"]
        target = event["target_process"]

        if process not in clocks:
            print("[ERROR] Invalid process:", process)
            continue

        index = PROCESSES.index(process)

        print(f"\n[EVENT] {event_id}")
        print(f"[PROCESS] {process}")
        print(f"[ACTION] {action}")

        # Receive event
        if action == "RECEIVE":

            key = (target, process)

            if key not in messages or not messages[key]:
                print("[ERROR] No matching SEND message!")
                continue

            received_vector = messages[key].pop(0)

            # Merge local and received vector
            clocks[process] = [
                max(a, b)
                for a, b in zip(clocks[process], received_vector)
            ]

        elif action not in ["SEND", "INTERNAL"]:
            print("[ERROR] Invalid event action!")
            continue

        # Increment own clock
        clocks[process][index] += 1

        # Store event timestamp
        event_vectors[event_id] = clocks[process].copy()

        # Send event
        if action == "SEND":

            if target not in clocks:
                print("[ERROR] Invalid target:", target)
                del event_vectors[event_id]
                continue

            key = (process, target)

            if key not in messages:
                messages[key] = []

            messages[key].append(clocks[process].copy())

            print(f"[SEND] Message sent from {process} to {target}")
            print("[MESSAGE VECTOR]", clocks[process])

        elif action == "RECEIVE":
            print(f"[RECEIVE] Message received from {target}")
            print("[MERGE] Vector clocks merged")

        print("[UPDATED VECTOR]", clocks[process])

    # Compare event vectors
    print("\n========== CAUSALITY ANALYSIS ==========")

    event_ids = list(event_vectors.keys())

    for i in range(len(event_ids)):
        for j in range(i + 1, len(event_ids)):

            e1 = event_ids[i]
            e2 = event_ids[j]

            v1 = event_vectors[e1]
            v2 = event_vectors[e2]

            if all(a <= b for a, b in zip(v1, v2)) and v1 != v2:
                print(f"{e1} -> {e2} : CAUSALLY PRECEDING")

            elif all(a >= b for a, b in zip(v1, v2)) and v1 != v2:
                print(f"{e2} -> {e1} : CAUSALLY PRECEDING")

            else:
                print(f"{e1} || {e2} : CONCURRENT")

    print("\n====================================")
    print("[SUCCESS] Vector Clock Completed.")
    print("====================================")


def main():

    filename = "vector_events_36.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    events = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            events.append({
                "event_id": row["event_id"],
                "process_id": row["process_id"],
                "event_action": row["event_action"].strip().upper(),
                "target_process": row["target_process"].strip()
            })

    vector_clock(events)


if __name__ == "__main__":
    main()
