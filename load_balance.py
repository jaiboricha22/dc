
import csv
import os

def least_connections(jobs):

    # Worker nodes and their current loads
    workers = {
        "Worker_1": 0,
        "Worker_2": 0,
        "Worker_3": 0
    }

    print("\n========== TRUSTMESH LOAD BALANCER ==========")
    print("[LOAD BALANCER] Initializing worker nodes...")
    print("Initial Worker Loads:", workers)

    print("\n[LOAD BALANCER] Distributing incoming jobs...")

    for job in jobs:

        # Select worker having minimum number of jobs
        selected_worker = min(
            workers,
            key=workers.get
        )

        # Assign job to selected worker
        job["assigned_worker"] = selected_worker
        job["status"] = "ASSIGNED"

        # Update worker load
        workers[selected_worker] += 1

        print(
            f"\n[ALLOCATION] Job {job['job_id']} "
            f"({job['compute_units']} units) "
            f"-> {selected_worker}"
        )

        print("[CURRENT LOAD]", workers)

    # Display final assignments
    print("\n========== FINAL JOB ALLOCATIONS ==========")

    for job in jobs:
        print(
            f"Job {job['job_id']} -> "
            f"{job['assigned_worker']} | "
            f"Status: {job['status']}"
        )

    # Display balanced workload summary
    print("\n========== WORKER LOAD SUMMARY ==========")

    for worker, load in workers.items():
        print(f"{worker}: {load} jobs")

    print("\nTotal Jobs:", len(jobs))
    print("==========================================")


def main():

    filename = "workload_5.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    jobs = []

    # Read jobs from CSV
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["status"].strip().upper() == "PENDING":
                jobs.append({
                    "job_id": row["job_id"],
                    "compute_units": int(row["compute_units"]),
                    "assigned_worker": row["assigned_worker"],
                    "status": row["status"]
                })

    least_connections(jobs)


if __name__ == "__main__":
    main()
