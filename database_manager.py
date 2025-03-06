import pyodbc
import pandas as pd

class DatabaseManager:
    def __init__(self, connection_string:str):
        self.connection_string = connection_string
    
    def get_schema_info(self) -> dict:
        """Fetch the database schma details"""
        schema = {
            "tables":{},
            "relationships":[]
        }

        try:
            with pyodbc.connect(self.connection_string) as conn:
                print(" connection string ", self.connection_string)
                cursor = conn.cursor()

                # Retrieve database tables
                tables = cursor.execute(
                    """
                        SELECT 
                            t.name AS table_name,
                            c.name AS column_name, 
                            ty.name AS data_type
                        FROM 
                            sys.tables t
                        INNER JOIN 
                            sys.columns c 
                            ON t.object_id = c.object_id
                        INNER JOIN 
                            sys.types ty 
                            ON c.user_type_id = ty.user_type_id
                        ORDER BY 
                            t.name, 
                            c.column_id
                    """).fetchall()
                           
                for table, column, data_type in tables:
                    if table not in schema["tables"]:
                        schema["tables"][table]={"columns":{}}
                    schema["tables"][table]["columns"][column] = data_type
                
                # Retrieve all the foreign key relationships
                relationships = cursor.execute(
                    """
                        SELECT 
                            OBJECT_NAME(f.parent_object_id) AS TableName,
                            COL_NAME(fc.parent_object_id, fc.parent_column_id) AS ColumnName,
                            OBJECT_NAME(f.referenced_object_id) AS ReferenceTableName,
                            COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS ReferenceColumnName
                        FROM 
                            sys.foreign_keys AS f
                        INNER JOIN 
                            sys.foreign_key_columns AS fc
                            ON f.OBJECT_ID = fc.constraint_object_id

                    """).fetchall()
                
                for table, column, referenced_table, referenced_column in relationships:
                    relationship = {
                        "table": table,
                        "column": column,
                        "referenced_table" : referenced_table,
                        "referenced_column" : referenced_column
                    }

                    if relationship not in schema["relationships"]:
                        schema["relationships"].append(relationship)
                
                return schema

                # # Convert the schema dictionary to a valid JSON string
                # schema_json = json.dumps(schema, indent=2)  # pretty-printing with 4 spaces indentation
                # return schema_json
        except Exception as ex:
            print(f"Unable to retrieve the database schema: {str(ex)}")
            return None

    def execute_query(self, query: str) -> pd.DataFrame:
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute(query)                

                # Fetch results
                results = cursor.fetchall()

                # print("Fetched Results:")
                for row in results[:1]:  # Show the first 1 rows for debugging
                    print(row)

                # Fetch column names
                columns = [column[0] for column in cursor.description]                

                # Check if the result set is empty
                if len(results) == 0:
                    print("No results found.")
                    return pd.DataFrame()  # Return an empty DataFrame if no results        
                
                # Check if the number of columns matches the number of columns in the first row
                if len(columns) == len(results[0]):
                    # Create a pandas DataFrame from the fetched data
                    data = [list(row) for row in results]
                    df = pd.DataFrame(data, columns=columns)
                    print(f"DataFrame created with shape: {df.shape}")
                    return df
                else:
                    print(f"Error: Column count {len(columns)} does not match row shape {len(results[0])}")
                    return pd.DataFrame()  # Return empty DataFrame in case of mismatch
            
        except Exception as e:
            print(f"Error Query execution failed: {str(e)}")
            return None
        
    def save_row_data(self, table_name, row_data):

        print(row_data)
        # Create a connection to the database
        conn = pyodbc.connect(self.connection_string)
        cursor = conn.cursor()

        # Prepare the columns and values for the SQL INSERT statement
        columns = ', '.join(row_data.keys())  # Column names as a comma-separated string
        values = ', '.join(f"'{v}'" for v in row_data.values())  # Values as a comma-separated string

        # Construct the SQL query
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
 
        print("_____ Query _____")
        print(query)
        try:
            # Execute the query
            cursor.execute(query)
            conn.commit()  # Commit the transaction to the database
            print("Data inserted successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection
            cursor.close()
            conn.close()
            
