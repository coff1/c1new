import sqlite3


class mydb:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('source/fristsqlite3.db')
        self.cursor = self.conn.cursor()

    def execute_sqlite(self,sql_statement)->None:        
        # Execute the SQL statement
        self.cursor.execute(sql_statement)        
        # Fetch the result of the query
        self.conn.commit()

    def query_sqlite(self,sql_statement):        
        # Execute the SQL statement
        self.cursor.execute(sql_statement)        
        # Fetch the result of the query
        result = self.cursor.fetchall()
        # Get the field names of the result set
        field_names = [i[0] for i in self.cursor.description]
        # Return the result and field names
        return {"result":result, "field_names":field_names}


    def query_sqlite_with_order(self,sql_statement, order_by_field_name=None,is_DESC = False):        
        # extrea the SQL statement
        if order_by_field_name != None:
            sql_statement = sql_statement + f" ORDER BY {order_by_field_name}"
        if is_DESC:
            sql_statement = sql_statement + " DESC"

        # Execute the SQL statement
        self.cursor.execute(sql_statement)        
        # Get the query result and the table field names
        result = self.cursor.fetchall()
        field_names = [field_info[0] for field_info in self.cursor.description]
        return {"result":result, "field_names":field_names}



    def insert_into_table(self,table_name, fields):
        # Construct the SQL statement for inserting the fields into the table
        sql_statement = f"INSERT INTO {table_name} VALUES ({','.join(['?' for field in fields])})"        
        # Execute the SQL statement
        self.cursor.execute(sql_statement, fields)        
        # Commit the changes to the database
        self.conn.commit()


    def insert_into_table(self,table_name, data):        
        # Construct the SQL statement for inserting the values into the table
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for value in data.values()])
        sql_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        # Execute the SQL statement
        self.cursor.execute(sql_statement, tuple(data.values()))        
        # Commit the changes to the database
        self.conn.commit()


    def insert_or_update_table(self,table_name, data):
        # Construct the SQL statement for inserting the values into the table
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for value in data.values()])
        sql_insert = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        columns +=', is_new'
        placeholders += ',False' 
        sql_update = f"REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            # Try to insert the values into the table
            self.cursor.execute(sql_insert, tuple(data.values()))
        except sqlite3.IntegrityError as e:
            # If a unique constraint violation error occurs, update the existing record in the table
            self.cursor.execute(sql_update, tuple(data.values()))
        # Commit the changes to the database
        self.conn.commit()


    def query_sqlite_with_parameter(self,sql_statement,**kwargs):        
        args={
            "order_by":None,
            "is_desc":None,
            "limit":None,
            "fuzz_filter":None,
            "the_filter":None
            }
        for i in kwargs:
            args[i] = kwargs [i]


        # extrea the SQL statement
        if args["fuzz_filter"]:
            sql_statement = sql_statement + " WHERE "+' AND '.join([f"{key} LIKE '%{args['fuzz_filter'][key]}%'" for key in args["fuzz_filter"]])
        if args["the_filter"]:
            sql_statement = sql_statement + " WHERE "+' AND '.join([f"{key} = {args['the_filter'][key]}" for key in args["the_filter"]])
        if args["order_by"]:
            sql_statement = sql_statement + " ORDER BY {}".format(args["order_by"])
        if args["is_desc"]:
            sql_statement = sql_statement + " DESC"
        if args["limit"]:
            sql_statement = sql_statement + " limit {}".format(args["limit"])

        # print(sql_statement)
        # Execute the SQL statement
        self.cursor.execute(sql_statement)        
        # Get the query result and the table field names
        result = self.cursor.fetchall()
        field_names = [field_info[0] for field_info in self.cursor.description]
        return {"result":result, "field_names":field_names}





