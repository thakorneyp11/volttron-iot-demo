# First install the Python crateDB library before implement this code!!
# use `pip install crate`

from crate import client

HOST = "localhost"
PORT = 4200


def query_data(crate_cursor: client, query_string: str) -> list:
  """
  This function query data from crateDB with arguments:
  
  crate_cursor: cursor pointing from to CrateDB
  type: crate.client
  query_string: SQL query string
  type: str
  """
  
  crate_cursor.execute(query_string)
  return crate_cursor.fetchall()


def main():
  crate_client = client.connect(f"http://{HOST}:{PORT}")
  cursor = crate_client.cursor()
  table_name = "raw_data"
  query_string = f"""
  SELECT * FROM {table_name} WHERE device_id='abc123' AND datapoint='temperature' ORDER BY timestamp DESC LIMIT 100
  """
  data = query_data(cursor, query_string)
  print(f"Got data: {data}")


if __name__ == "__main__":
  main()