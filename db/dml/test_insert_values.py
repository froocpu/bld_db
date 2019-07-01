import psycopg2

if __name__ == "__main__":
    try:
        connection = psycopg2.connect(user = "you",
                                      password = "hunter2",
                                      host = "host",
                                      port = "5432",
                                      database = "postgres")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        #closing database connection.
        connection.close()
    except Exception as error :
        print ("Error while connecting to PostgreSQL", error)
