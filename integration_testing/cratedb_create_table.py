# First install the Python crateDB library before implement this code!!
# use `pip install crate`

from crate import client

HOST = "localhost"
PORT = 4200


def create_table(crate_cursor: client, table_name: str):
  """
  This function create table in crateDB with arguments:
  
  crate_cursor: cursor pointing from to CrateDB
  type: crate.client
  table_name: name of table to be create in CrateDB
  type: str
  """
  
  create_table_str = f"""
  CREATE TABLE {table_name} (
  timestamp TIMESTAMP,
  device_id VARCHAR(32),
  datapoint VARCHAR(32),
  value TEXT
  )
  """
  crate_cursor.execute(create_table_str)


def main():
  crate_client = client.connect(f"http://{HOST}:{PORT}")
  cursor = crate_client.cursor()
  create_table(cursor, "raw_data")


if __name__ == "__main__":
  main()