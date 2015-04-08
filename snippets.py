import psycopg2
import logging
import argparse
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")


def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection, connection.cursor() as cursor:
      try:  
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))          
      except psycopg2.IntegrityError as e:
        connection.rollback()
        command = "update snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet, name))    
    logging.debug("Snippet stored successfully.")
    return snippet
        
def get(name):
    """Retrieve the snippet with a given name."""
    logging.info("Retrieving snippet {!r}.".format(name))
    command = "select message from snippets where keyword=%s"
    with connection, connection.cursor() as cursor:
      cursor.execute("select message from snippets where keyword=%s", (name,))
      row = cursor.fetchone()
    logging.debug("Snippet retrieved successfully.")
    if not row:
      print "Snippet does not exist."
    else:
      return row[0]
  
def catalogue():
  """Provide a list of all snippets with names."""
  logging.info("Retrieving snippet catalogue.")
  command = "select * from table"
  with connection, connection.cursor() as cursor:
    cursor.execute("select * from snippets")
    row = cursor.fetchall()
  logging.debug("Catalogue retrieved successfully.")
  if not row:
      print "Catalogue is empty."
  else:
      return row
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    # Subparser for the get command
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    get_parser.add_argument("snippet", help="The snippet text")
    
    
    
    # Subparser for the catalogue command
    get_parser = subparsers.add_parser("catalogue", help="Retrieve snippet catalogue")    

    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
      name = put(**arguments)
      print("Stored {!r}.".format(name))
    elif command == "get":
      snippet = get(**arguments)
      print("Retrieved snippet: {}.".format(snippet))
    elif command == "catalogue":
      row = catalogue(**arguments)
      print "Catalogue returned: "
      for pairs in row:
        print pairs
      
      
      
      
        
if __name__ == "__main__":
    main()