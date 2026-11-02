
import csv
import json
import os

# ------------------------------------------
# TRUSTMESH SERVER FUNCTIONS
# ------------------------------------------

def processData(value):
    print(f"[SERVER EXECUTION] Processing parameter: {value}")
    result = value * 2
    return result


def calculateRisk(value):
    print(f"[SERVER EXECUTION] Calculating risk for: {value}")

    if value > 500:
        return "HIGH RISK"
    else:
        return "LOW RISK"


# ------------------------------------------
# RPC DISPATCHER
# ------------------------------------------

def dispatcher(request):

    method_name = request["method_name"]
    param_value = request["param_value"]

    # Identify and execute requested method
    if method_name == "processData":
        return processData(param_value)

    elif method_name == "calculateRisk":
        return calculateRisk(param_value)

    else:
        raise ValueError(f"Unknown method: {method_name}")


# ------------------------------------------
# RPC CLIENT
# ------------------------------------------

def rpc_client():

    filename = "rpc_calls_1.csv"

    print("\n==========================================")
    print("       TRUSTMESH RPC SIMULATION")
    print("==========================================")

    if not os.path.exists(filename):
        print("[ERROR] CSV file not found!")
        return

    with open(filename, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            print("\n------------------------------------------")

            # Read request from CSV
            call_id = row["call_id"]
            client_name = row["client_name"]
            method_name = row["method_name"]
            param_value = int(row["param_value"])
            timestamp = row["timestamp"]

            print("[DISPATCH] Client invoking method")
            print(f"Call ID: {call_id}")
            print(f"Client: {client_name}")
            print(f"Method: {method_name}")
            print(f"Parameter: {param_value}")
            print(f"Timestamp: {timestamp}")

            # ----------------------------------
            # MARSHALLING
            # ----------------------------------

            request = {
                "call_id": call_id,
                "client_name": client_name,
                "method_name": method_name,
                "param_value": param_value
            }

            marshalled_data = json.dumps(request)

            print("[MARSHALLING] Request packaged successfully")

            # ----------------------------------
            # SERVER RECEIVES REQUEST
            # ----------------------------------

            received_request = json.loads(marshalled_data)

            print("[SERVER] Request received")

            # ----------------------------------
            # SERVER DISPATCHES REQUEST
            # ----------------------------------

            try:
                result = dispatcher(received_request)

                # ----------------------------------
                # RETURN RESULT
                # ----------------------------------

                response = {
                    "call_id": call_id,
                    "result": result
                }

                # Unmarshalling response
                returned_data = json.dumps(response)
                final_response = json.loads(returned_data)

                print(f"[RETURN] Result: {final_response['result']}")
                print("[CLIENT] Response received successfully")

            except ValueError as error:
                print(f"[SERVER ERROR] {error}")


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------

if __name__ == "__main__":
    rpc_client()
