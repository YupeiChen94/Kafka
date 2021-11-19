from kafka import KafkaProducer
from kafka.errors import KafkaError
import msgpack
import json
import logging as log

# Basic producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Asynchronous send by default
future = producer.send('my-topic', b'raw_bytes')

# Block until all async messages are sent
producer.flush()

# Close producer
producer.close()

# Producer with msgpack encoded objects
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key', 'value'})
producer.close()

# Producer with json messages and retries
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'), retries=5)
producer.send('json-topic', {'key', 'value'})
producer.close()


# Functions
def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)
    print(record_metadata.timestamp)


def on_send_error(exception):
    log.error('I am an errback', exc_info=exception)
    # Handle exception
    pass


# Produce async with callbacks
producer.send('json-topic', {'key', 'value'}).add_callback(on_send_success).add_callback(on_send_error)
producer.flush()
producer.close()



