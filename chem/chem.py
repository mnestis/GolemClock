#!/usr/bin/python

import alarmlogic
import pika
import threading
import time

alarmlist=[]
running =True

# performs time based actions
def timethread():

        alarmactive=0
	while running:
		alarm_set = alarmlogic.evaluatealarms(alarmlist)

		if alarm_set == 1 and alarmactive==0:
			channel.basic_publish(exchange='clock_output',
	                routing_key='',
	                body='ALARM_START')
		        alarmactive=1
 		elif alarm_set == 0 and alarmactive==1:
 			channel.basic_publish(exchange='clock_output',
        	        routing_key='',
        	        body='ALARM_STOP')
        	        alarmactive=0
	
		time.sleep(1)




if __name__ == "__main__":

        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()

#        channel.queue_declare(queue='output')

	# input channels
	channel.queue_declare(queue='input')

	# output channels
	channel.exchange_declare(exchange='clock_output',type='fanout')

        alarmlist = alarmlogic.getalarms()

	t1 = threading.Thread(target=timethread)
	t1.start()

	try:
        	while(1):
			time.sleep(1)
			pass
	except KeyboardInterrupt:
		running=False

