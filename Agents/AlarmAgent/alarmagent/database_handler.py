import time
from crate import client


def insert_data(table: str, data: list, HOST="localhost", PORT=4200):
    try:
        # connect to CrateDB database
        crate_cursor = client.connect(f"http://{HOST}:{PORT}")
        # construct query string
        insert_data_str = f"""INSERT INTO {table} (timestamp, device_id, datapoint, value) VALUES (?, ?, ?, ?)"""
        # execute query to insert data
        crate_cursor.execute(insert_data_str, data)
    except Exception as e:
        pass
    
def insert_data(table: str, data: list, HOST="localhost", PORT=4200):
    try:
        # connect to CrateDB database
        crate_client = client.connect(f"http://{HOST}:{PORT}")
        cursor = crate_client.cursor()
        # construct query string
        insert_data_str = f"""INSERT INTO {table} (timestamp, device_id, datapoint, value) VALUES (?, ?, ?, ?)"""
        # execute query to insert data
        cursor.execute(insert_data_str, data)
    except Exception as e:
        pass


if __name__ == "__main__":
    data = [
        time.time(),
        "device_1",
        "temperature",
        "25.0"
    ]
    insert_data(
        table="raw_data",
        data=data,
        HOST="localhost",
        PORT=4200
    )
