import asyncio
import logging
import time
import sys
import aiohttp
import json
import os
import traceback
import re
import datetime
import asyncio_redis
import subprocess

redis_url = 'pwc-redis'
redis_port = 6379

# Boiler Plate code which creates a log file instead of printing to console 
# https://discordpy.readthedocs.io/en/latest/logging.html
###
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
# formatter = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
logger = root

async def split_input(value_from_pubsub):
    value = str(value_from_pubsub)
    v = value.split()
    return v

async def call_wallet(command):
        check_info = subprocess.getoutput('pawcoin-cli {}'.format(command))
        logger.info('pawcoin-cli output {}'.format(check_info))
        return check_info

async def setHash(my_key, my_field, my_value) -> int:
    # Create Redis connection
    connection = await asyncio_redis.Connection.create(
        host=redis_url,
        port=redis_port)
    logger.info('Connection Made to redis for hset')
    # Set a hash field
    hashResponse = await connection.hsetnx(my_key, my_field, my_value)
    # When finished, close the connection.
    connection.close()
    return hashResponse

async def publish(channel, message):
    """Read events from pub-sub channel."""
    try:
        connection = await asyncio_redis.Connection.create(host='pwc-redis', port=6379)
        # Create subscriber.
        logger.info('connection created to redis from publish {}'.format(connection))
        # Create publish on the feed
        message = str(message)
        await connection.publish(channel, message)
        connection.close()
        return True
    except:
        return False
    logger.info('{}, message has been published to redis'.format(message))

async def start_pubsub(sub_channel): 
    connection = await asyncio_redis.Connection.create(host=redis_url, port=redis_port)
    logger.info('Redis Connection Succeeded')

    subscriber = await connection.start_subscribe()
    await subscriber.subscribe([ sub_channel ])
    logger.info('subscribed to channel')

    # inPubSub = await connection.in_pubsub()
    # logging.info('In the Pubsub? - {}'.format(inPubSub))

    while True:
        reply = await subscriber.next_published()
        # await publish_work('Work', reply)
        logger.info('Message received {}'.format(reply))
        
        # work queue pending
        logger.info(reply.value)
        value = reply.value
        v = str(value)
        await setHash(value, 'message_status', 'Active')

        logger.info('Value from Pubsub - {}'.format(value))
        message_id = await split_input(v)
        logger.info('message id from pubsub - {}'.format(message_id[0]))
        command = message_id[2]
        # command = re.sub(r'^\W*\w+^\W*\w+\W*', '', value)
        logger.info('Command going to the wallet - {}'.format(str(command)))
        try:
            command_output = await call_wallet(command) 
            logger.info('SUCCESS! Command output - {}'.format(command_output))
            output_message = str(command_output)
            publish_output = await setHash(message_id[0], 'command_output', output_message)
            logger.info('Success publishing the message to complete - {}'.format(publish_output))
        except:
            logger.info('FAILURE! Command output  - {}'.format(command_output))
        ## work queue complete
    # When finished, close the connection.
    connection.close()
    # start_pubsub_work(reply)

asyncio.run(start_pubsub('Wallet'))