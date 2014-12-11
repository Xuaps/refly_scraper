#!/usr/bin/python
import psycopg2

def main():
  connection_string = "host='localhost' dbname='slashdb' user='postgres'"
 
  connection = psycopg2.connect(connection_string)
  pgcursor = connection.cursor()
  query = """
        INSERT INTO refs (reference, content,uri,parent_uri,type,docset)
        SELECT reference,content,uri,parent,type, docset FROM temp_refs
        """
  pgcursor.execute(query)
  print "Transfer completed!\n"
  connection.commit()
 
if __name__ == "__main__":
	main()

