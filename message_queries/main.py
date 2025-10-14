import pika
import json


# Понимание асинхронности, очередей, надёжности.
# Интеграция с RabbitMQ, Kafka, Redis Streams и т.д.
# Обработка ошибок, retry, dead letter queues.

# Простая асинхронная обработка.
# Подходит для систем с высокой нагрузкой.
# Можно масштабировать и распределять нагрузку.


# Producer
def send_message(queue_name: str, message: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()


# Consumer
def consume_messages(queue_name: str, callback_func):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        msg = json.loads(body)
        try:
            callback_func(msg)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("Waiting for messages...")
    channel.start_consuming()


# Пример обработки
def process_order(msg):
    print(f"Processing order: {msg}")

send_message("order_queue", {"order_id": 123, "status": "created"})
consume_messages("order_queue", process_order)
