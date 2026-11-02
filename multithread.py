
import csv
import os
import threading
import time

# Mutex lock to protect shared resources
task_lock = threading.Lock()

# Shared list of completed tasks
completed_tasks = []


def worker(task):

    task_id = task["task_id"]
    thread_name = task["thread_name"]
    burst_ms = task["burst_ms"]
    priority = task["priority"]

    print(
        f"\n[{thread_name}] Started processing "
        f"Task {task_id} | Priority: {priority}"
    )

    # Simulate task execution
    time.sleep(burst_ms / 1000)

    # Acquire mutex lock before modifying shared list
    print(f"[{thread_name}] Waiting to acquire lock...")

    with task_lock:
        print(f"[{thread_name}] Lock ACQUIRED")

        completed_tasks.append(task_id)

        print(f"[{thread_name}] Task {task_id} added to completed list")

        print(f"[{thread_name}] Lock RELEASED")


def main():

    filename = "tasks_4.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    tasks = []

    # Read tasks from CSV
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["status"].strip().upper() == "PENDING":
                task = {
                    "task_id": row["task_id"],
                    "thread_name": row["thread_name"],
                    "burst_ms": int(row["burst_ms"]),
                    "priority": row["priority"]
                }
                tasks.append(task)

    print("\n========== TRUSTMESH MULTITHREADING ==========")
    print("[MAIN] Creating worker threads...")

    threads = []

    # Create and start worker threads
    for task in tasks:
        thread = threading.Thread(
            target=worker,
            args=(task,)
        )

        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("\n========== FINAL TASK STATUS ==========")
    print("[MAIN] All worker threads completed.")

    for task_id in completed_tasks:
        print(f"[COMPLETED] Task {task_id}")

    print("\nTotal Completed Tasks:", len(completed_tasks))
    print("=======================================")


if __name__ == "__main__":
    main()
