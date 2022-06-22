#!/usr/bin/env python
import time
import os
import pika
from laserembeddings import Laser
from math import sqrt
import functools
import logging
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)



def squared_sum(x):
    
    return round(sqrt(sum([a*a for a in x])),3)

def cos_similarity(x,y):

    numerator = sum(a*b for a,b in zip(x,y))
    denominator  = squared_sum(x)*squared_sum(y)
    return round(numerator/float(denominator),3)

def filterdecision(score):
    
    print(score)
    if score<=0.75:
        print("Misaligned sentence pair")
        return True
    else:
        print("Aligned sentence pair")
        return False

def on_request(ch, method, props, body):

    body = body.decode("utf-8")
    l = body.split("$")
    sentence1=l[0]
    sentence2=l[1]

    laser = Laser()

    embeddings = laser.embed_sentences([sentence1,sentence2],lang=['de','fr'])

    score = cos_similarity(embeddings[0],embeddings[1])

    if(filterdecision(score)):
        response = "Misaligned sentence pair"
    else:
        file1.write(sentence1)
        file2.write(sentence2)
        file3.write(str(score)+"\n")
        response = "Aligned sentence pair"

    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


lang1 = "de"
lang2 = "fr"

file1 = open("output/filtereddata."+lang1,"w")
file2 = open("output/filtereddata."+lang2,"w")
file3 = open("output/similarityscores.de-fr","w")

print(" [x] Awaiting Language Pairs, To exit press CTR+C")


#start  

# establishing the connection 

credentials = pika.PlainCredentials('guest', 'guest')
# Note: sending a short heartbeat to prove that heartbeats are still
# sent even though the worker simulates long-running work
parameters = pika.ConnectionParameters('localhost', credentials=credentials, blocked_connection_timeout=60)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

#declaring the queue

channel.queue_declare(queue='langaugepairs')


channel.basic_qos(prefetch_count=1)

#declaring a callback on_request and it is executed when the request from the client is recived. 
#It does the work specified in the on_request function and sends the response back 


channel.basic_consume(queue='langaugepairs', on_message_callback=on_request)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

channel.stop_consuming()

file1.close()
file2.close()

print(os.path.abspath("output/filtereddata.de"))
print(os.path.abspath("output/filtereddata.fr"))
print(os.path.abspath("output/similarityscores.de-fr"))


#connection.close()