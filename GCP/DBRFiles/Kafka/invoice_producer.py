# Databricks notebook source
from confluent_kafka import Producer
import json
import time

# COMMAND ----------

# dbutils.library.restartPython()

# COMMAND ----------

class invoiceproducer:
    def __init__(self):
        self.topic="invoices"
        self.conf={
            'bootstrap.servers':'pkc-n3603.us-central1.gcp.confluent.cloud:9092',
            'security.protocol':'SASL_SSL',
            'sasl.mechanism':'PLAIN',
            'sasl.username':'ZKP5URHC7O4FOIQK',
            'sasl.password':'yMjcbjJvepEfTHVouAUlwFcjapvPtbjQxY+5fXto9hNpLwLOhvJTUjokNwROV5gN',
            'client.id':'sanjeevmachine'
        }
    
    def delivery_callback(self,err,msg):
        if err:
            print("Error")
        else:
            key=msg.key().decode('utf-8')
            invoice_id=json.loads(msg.value().decode('utf-8'))["InvoiceNumber"]
            print("Produced event to key")

    def produce_invoices(self,producer,counts):
        counter=0
        with open("gs://rawdbrdata/datasets/invoices/invoices.json") as lines:
            for line in lines:
                invoice=json.loads(line)
                store_id=invoice['StoreID']
                producer.produce(self.topic,key=store_id,value=line,callback=self.delivery_callback)
                time.sleep(0.5)
                producer.poll(1)
                counter+=1
                if counter==counts:
                    break
    def start(self):
        kafka_producer=Producer(self.conf)
        self.produce_invoices(kafka_producer,10)
        kafka_producer.flush(10)

# COMMAND ----------

invoice_producer=invoiceproducer()

# COMMAND ----------

invoice_producer.start()

# COMMAND ----------

pwd

# COMMAND ----------



# COMMAND ----------


