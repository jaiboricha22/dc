
import csv
import os
from collections import defaultdict

clocks = defaultdict(int)
messages = {}
events = []


def lamport_clock(events):

    print("\n========== LAMPORT'S LOGICAL CLOCK ==========")

    for event in events:

        event_id = event["event_id"]
        process = event["process_id"]
        event_type = event["event_type"]
        message_to = event["message_to"]

        if process not in clocks:
            clocks[process] = int(event["initial_clock"])

        print(f"\n[EVENT] {event_id}")
        print(f"[PROCESS] {process}")
        print(f"[TYPE] {event_type}")

        # Internal event
        if event_type == "INTERNAL":

            clocks[process] += 1

            print("[INTERNAL] Clock incremented")

        # Send event
        elif event_type == "SEND":

            clocks[process] += 1

            timestamp = clocks[process]

            messages[(process, message_to)] = timestamp

            print(f"[SEND] Message sent to {message_to}")
            print(f"[MESSAGE TIMESTAMP] {timestamp}")

        # Receive event
        elif event_type == "RECEIVE":

            sender = message_to
            key = (sender, process)

            if key not in messages:
                print("[ERROR] No matching SEND event found!")
                continue

            msg_timestamp = messages[key]
            old_clock = clocks[process]

            clocks[process] = max(
                old_clock, msg_timestamp
            ) + 1

            print(f"[RECEIVE] Message received from {sender}")
            print(f"[CURRENT CLOCK] {old_clock}")
            print(f"[MESSAGE TIMESTAMP] {msg_timestamp}")

        else:
            print("[ERROR] Invalid event type!")
            continue

        event["logical_timestamp"] = clocks[process]

        print(f"[LOGICAL CLOCK] {clocks[process]}")

    # Sort events by logical timestamp
    events.sort(
        key=lambda e: (
            e["logical_timestamp"],
            e["process_id"],
            e["event_id"]
        )
    )

    print("\n========== FINAL CAUSAL ORDER ==========")

    for event in events:
        print(
            f"{event['event_id']} | "
            f"Process: {event['process_id']} | "
            f"Type: {event['event_type']} | "
            f"Timestamp: {event['logical_timestamp']}"
        )

    print("\n========== FINAL PROCESS CLOCKS ==========")

    for process, clock in sorted(clocks.items()):
        print(f"{process}: {clock}")

    print("\n[SUCCESS] Lamport Clock Execution Completed.")
    print("============================================")


def main():

    filename = "events_29.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            events.append(row)

    lamport_clock(events)


if __name__ == "__main__":
    main()
