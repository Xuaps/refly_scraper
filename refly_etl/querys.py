def UpsertQuery( connection, insert_buffer, update_buffer ):
    connection.execute("begin")    
    connection.execute(
        """
        CREATE TABLE temp_refs
        (
          docset text NOT NULL,
          reference text NOT NULL,
          type text NOT NULL,
          content text,
          parent_uri text,
          uri text NOT NULL
        )
        """
    )

    for item in insert_buffer:
        connection.execute(
            """
            SET CONSTRAINTS ALL DEFERRED;
            INSERT INTO temp_refs ( reference, type, docset, content, uri, parent_uri)\
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            item['reference'], item['type'], item['docset'], item['content'], item['uri'], item['parent']
        )
    #connection.execute(
    #    """
    #    DELETE FROM refs WHERE docset=%s;
    #    """,
    #    insert_buffer[0]['docset']
    #)
    connection.execute("end")
    print 'insert: ' + str(len(insert_buffer))
    print 'update: ' + str(len(update_buffer))
