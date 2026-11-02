
import csv
import os

def cristian_algorithm(records):

    print("\n======= DISTRIBUTED SMART TRAFFIC MANAGEMENT =======")
    print("       CRISTIAN'S CLOCK SYNCHRONIZATION")
    
    for record in records:

        client_id = record["client_id"]
        t0 = record["t0_send_ms"]
        t_server = record["t_server_ms"]
        t1 = record["t1_recv_ms"]

        print("\n----------------------------------------------")
        print(f"[CLIENT] {client_id} sends time request")
        
        # Calculate Round Trip Time
        rtt = t1 - t0
        print(f"[RTT] T1 - T0 = {t1} - {t0} = {rtt} ms")

        # Estimate server time when response reaches client
        estimated_server_time = t_server + (rtt / 2)

        print(
            f"[SERVER TIME] T_server + (RTT / 2) "
            f"= {t_server} + ({rtt} / 2)"
        )
        print(
            f"[ESTIMATED TIME] {estimated_server_time:.2f} ms"
        )

        # Calculate local clock offset
        local_clock_offset = estimated_server_time - t1

        print(
            f"[OFFSET] Estimated Server Time - Client Receive Time "
            f"= {estimated_server_time:.2f} - {t1}"
        )
        print(f"[OFFSET] {local_clock_offset:+.2f} ms")

        # Adjust client clock
        adjusted_client_time = t1 + local_clock_offset

        print(
            f"[ADJUSTED CLOCK] {adjusted_client_time:.2f} ms"
        )

    print("\n==============================================")
    print("[SUCCESS] Clock Synchronization Completed.")
    print("==============================================")


def main():

    filename = "cristian_clocks_8.csv"

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    records = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            record = {
                "client_id": row["client_id"],
                "t0_send_ms": float(row["t0_send_ms"]),
                "t_server_ms": float(row["t_server_ms"]),
                "t1_recv_ms": float(row["t1_recv_ms"])
            }

            records.append(record)

    cristian_algorithm(records)


if __name__ == "__main__":
    main()
