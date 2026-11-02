import csv
import json
import os

def process_data(value):
    print(f"[SERVER EXECUTION] Processing parameter : {value}")
    result = value *2;
    return result