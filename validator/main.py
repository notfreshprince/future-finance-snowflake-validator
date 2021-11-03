import logging
import requests
import argparse
from connector import get_connection, run_query

PUSHGATEWAY_URL = "http://pushgateway.grada-pii-sales-nonprd.js-devops.co.uk/metrics/job/grada_sales_airflow"
REQUEST_TIMEOUT = 20

logging.basicConfig(level=logging.INFO)
pushgateway_logger = logging.getLogger("pushgateway")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", action="store", dest="query", help="Query filename")
    parser.add_argument("-m", "--metric-name", action="store", dest="metric_name", help="Metric name")
    parser.add_argument("-n", "--nargs", nargs="+", dest="nargs", help="Nargs")

    return parser.parse_args()


def _push_metric(metric_name, metric_value, labels=None):
    pushgateway_logger.info(f"sending metric [{metric_name}] values to Pushgateway")
    label_suffix = ""
    if labels and isinstance(labels, dict):
        label_suffix = "/".join([f"{name}/{value}" for name, value in labels.items()])

    logging.info(f"Pushing to [{PUSHGATEWAY_URL}]...")

    resp = requests.post(
        f"{PUSHGATEWAY_URL}/{label_suffix}",
        data=f"{metric_name} {metric_value}\n",
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    logging.info("FINISHED")


def validate_and_push(query, metric_name):
    logging.info(f"Running validation query [{query}]...")

    with get_connection() as snowflake_connection:
        results = run_query(snowflake_connection, query)

    for row in results:
        _push_metric(metric_name, row[0])


if __name__ == '__main__':
    args = parse_args()
    validate_and_push(args.query, args.metric_name)
