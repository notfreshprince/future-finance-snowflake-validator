import logging
from os.path import join, exists
from snowflake import connector


logging.basicConfig(level=logging.INFO)
snowflake_connector_logger = logging.getLogger("pushgateway")


def get_connection():
    connection = connector.connect(
        user='EPOS_ETL_DEV_USER',
        password='h33ln1#ZtVFt7&mk',
        account="sainsburys.eu-west-1",
        host="sainsburys.eu-west-1.privatelink.snowflakecomputing.com",
        warehouse="KIWI_WH_L",
        database="ADW_DEV",
        role="KIWI_DEV_DEVELOPER"
    )
    return connection


def run_query(connection, query_name):
    sql_path = join("sql", query_name + ".sql")

    if exists(sql_path):
        logging.info(f"Running query [{sql_path}]...")
        with open(f"{sql_path}", "r") as query:
            cursor = connection.execute_string(query.read())[0]
            results = cursor.fetchall()
            return results
