import backoff
from clickhouse_driver import Client
from kafka import KafkaConsumer, OffsetAndMetadata, TopicPartition
from settings import logger, settings


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def create_table(client: Client) -> None:
    """
    Creating table in Clickhouse
    :param client: Clickhouse connection
    """
    client.execute("""CREATE DATABASE IF NOT EXISTS content ON CLUSTER company_cluster""")
    client.execute(
        """CREATE TABLE IF NOT EXISTS content.views  ON CLUSTER company_cluster (
            user_id UUID,
            movie_id UUID,
            viewed_frame UInt64,
            event_time DateTime
            )  Engine=MergeTree()  ORDER BY event_time
     """)


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def insert_in_clickhouse(client: Client, batch: list) -> None:
    """
    Inserting data in clickhouse
    :param client: Clickhouse connection
    :param data: Data for load
    """
    try:
        client.execute(
            "INSERT INTO content.views VALUES",
            batch,
            types_check=True,
        )
        return None
    except KeyError as ch_err:
        logger.error(
            "Error while loading data into Clickhouse: {0}".format(ch_err)
        )


def etl_process(extractor: KafkaConsumer, loader: Client, batch_size: int) -> None:
    while True:
        data_list = []
        for message in extractor:
            try:
                msg = (*str(message.key.decode('utf-8')).split('+'), int(message.value), message.timestamp)
                data_list.append(str(msg))
                if len(data_list) == batch_size:
                    insert_in_clickhouse(loader, data_list)
                    data_list.clear()
                    tp = TopicPartition(settings.kafka.topics, message.partition)
                    options = {tp: OffsetAndMetadata(message.offset + 1, None)}
                    consumer.commit(options)
                    logger.debug(f'Loader success {len(data_list)} rows')
            except Exception as e:
                logger.error(f'Loader error: {e}')


if __name__ == "__main__":
    consumer = KafkaConsumer(
        settings.kafka.topics,
        bootstrap_servers=settings.kafka.uri,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        group_id=settings.kafka.group_id,
    )
    clickhouse_client = Client(host=settings.ch.host, port=settings.ch.port)
    create_table(clickhouse_client)

    etl_process(consumer, clickhouse_client, batch_size=settings.app.batch_size)
