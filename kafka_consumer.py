from elasticsearch import Elasticsearch

from kafka import KafkaConsumer
from kafka import TopicPartition

import json

var = 1
while var == 1 :
    # Initialize Kafka consumer
    consumer = KafkaConsumer(bootstrap_servers='ec2-18-188-248-171.us-east-2.compute.amazonaws.com:9092',group_id='p3consumer',auto_offset_reset='latest')
    consumer.subscribe(['instagram'])
    
    # Initialize Elasticsearch client
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    # Read incoming messages
    for message in consumer:
        if "Username" in message.value:
            
            # Parse message text
            content = message.value
            json_string = content.split('(data-HEAP): ')[1]

            stalker_report_json = json.loads(json_string)
            
            # Push the data to Elasticsearch index
            es.index(index='instagram_report', doc_type='report', id=stalker_report_json['ImageAnalysis']['Id'], body=stalker_report_json)
