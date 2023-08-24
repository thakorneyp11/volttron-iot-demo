# First install the Python crateDB library before implement this code!!
# use `pip install crate`

from crate import client
import time

HOST = "localhost"
PORT = 4200


def insert_data(crate_cursor: client, table: str, data: list):
  """
  This function insert data into crateDB with arguments:
  
  crate_cursor: cursor pointing from to CrateDB
  type: crate.client
  table: name of table to be insert data in CrateDB
  type: str
  data: data to insert into database
  type: list
  """
  
  insert_data_str = f"""INSERT INTO {table} (timestamp, device_id, datapoint, value) VALUES (?, ?, ?, ?)"""
  crate_cursor.execute(insert_data_str, data)


def main():
  crate_client = client.connect(f"http://{HOST}:{PORT}")
  cursor = crate_client.cursor()
  data = [
    time.time(),
    "abc1234",
    "temperature",
    "25.0"
  ]
  insert_data(cursor, "raw_data", data)


if __name__ == "__main__":
  main()