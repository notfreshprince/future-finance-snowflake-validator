import boto3
import logging


logging.basicConfig(level=logging.INFO)
pushgateway_logger = logging.getLogger("task_monitor")

ECS_CLUSTER_ARN = "arn:aws:ecs:eu-west-1:414834577805:cluster/grada-sales-dev-ecs-cluster"
SCHEDULED_TASKS = ["grada-etl-apps-competitor-benchmarking-weighting-event-rule",
                   "grada-etl-apps-sftp-nectar-event-rule",
                   "grada-sales-sql-scheduler-Data-Science-RDV-dev",
                   "grada-sales-sql-scheduler-checkouts-appevent-dev",
                   "grada-sales-sql-scheduler-checkouts-customer-order-dev",
                   "grada-sales-sql-scheduler-checkouts-retail-dev",
                   "grada-sales-sql-scheduler-checkouts-signoff-dev",
                   "grada-sales-sql-scheduler-checkouts-signon-dev",
                   "grada-sales-sql-scheduler-fee-dev",
                   "grada-sales-sql-scheduler-nectar-lk-dev",
                   "grada-sales-sql-scheduler-osts-ppsv-store-day-prd-dev",
                   "grada-sales-sql-scheduler-osts-raw-dev",
                   "grada-sales-sql-scheduler-pharmacy-items-dev",
                   "grada-sales-sql-scheduler-update-price-amt-returns",
                   "grada-sales-sql-scheduler-update-store-nk-cust-order",
                   "pii-sales-smg-lettuceknow-sftp-lettuce-know-feedback",
                   "pii-sales-smg-lettuceknow-sftp-lettuce-know-instore",
                   "pii-sales-smg-lettuceknow-sftp-lettuce-know-ofs",
                   "pii-sales-smg-lettuceknow-sftp-lettuce-know-popup",
                   "pii-sales-smg-lettuceknow-sftp-lk-comp-benchmarking"]


if __name__ == '__main__':
    # try:
    #     while True:
    #         # DO THINGS
    #         pass
    # except Exception:
    #     raise

    client = boto3.client("ecs", region_name="eu-west-1")

    running_tasks = client.list_tasks(
        cluster=ECS_CLUSTER_ARN,
        # desired_status='RUNNING'
    )

    logging.info("RUNNING TASKS:")
    for task in running_tasks:
        logging.info(task)

    for task in SCHEDULED_TASKS:
        if task in running_tasks:
            logging.info(f"Hot diggity dog, we got a live one: [{task}]")
        else:
            logging.info("No scheduled tasks were found to be running, will try again shortly...")
