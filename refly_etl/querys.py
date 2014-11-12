def UpsertQuery( connection, insert_buffer, update_buffer ):
    connection.execute(
        """
        DELETE FROM refs WHERE docset=%s;
        """,
        insert_buffer[0]['docset']
    )
    for item in insert_buffer:
        connection.execute(
            """
            INSERT INTO refs ( reference, type, docset, content, uri, parent_uri)\
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            item['reference'], item['type'], item['docset'], item['content'], item['uri'], item['parent']
        )
