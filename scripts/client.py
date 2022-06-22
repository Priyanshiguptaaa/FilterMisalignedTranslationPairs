#!/usr/bin/env python
import pika
import uuid
import asyncio
import time
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

#initializing the client class

class FilterPairRpcClient(object):

    def __init__(self):

        #establishing a connection
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        #establishing the channel
        self.channel = self.connection.channel()

        #client sends a request message and expects a response message from the server

        result = self.channel.queue_declare(queue='', exclusive=True)

        #callback queue is where the asynchronous code gets pushed and waits for its execution so that we can receive responses
        self.callback_queue = result.method.queue

        #starting a non-local, non-exclusiove consumer, with explicit acknowledgements and a server generated consumer tag

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    #on_response callback function gets executed on every response, checks the correlation_id, saves the response and breaks the consuming loop 

    def on_response(self, ch, method, props, body):

        #correlation is used to set a unique value for every request
        if self.corr_id == props.correlation_id:
            self.response = body

    #call fucntion to send the client request and blocking until the answer is received

    async def call(self, text):
        self.response = None

        #generate a correlation id number that the on_response callback function uses to catch the appropriate response
        self.corr_id = str(uuid.uuid4())

        #publishing the request message to the server with two properties; reply_to and correlation_id
        self.channel.basic_publish(
            exchange='',
            routing_key='langaugepairs',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=text)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

#reading the files as arguments  

file1 = sys.argv[1]
file2 = sys.argv[2]

f1 = open(file1)
f2 = open(file2)


lines1 = f1.readlines()
lines2 = f2.readlines()

print("lines read")

n = len(lines1)

#defining the asynchronous funtion to read line by line data and send it to the broker as a task queue
async def main():

    tasks = []

    for i in range(0,n):

        filterpair_rpc = FilterPairRpcClient()

        print(" [x] Requesting decision for pair")

        s = lines1[i]+'$'+lines2[i]

        print(lines1[i]+','+lines2[i])


        tasks.append(asyncio.ensure_future(filterpair_rpc.call(s)))

    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(" [.] Got %r" % response)

asyncio.run(main())
#print("--- %s seconds ---" % (time.time() - start_time))