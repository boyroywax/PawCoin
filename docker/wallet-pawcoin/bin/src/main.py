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

async def publish_work(message):
    """Read events from pub-sub channel."""

    try:
        connection = await asyncio_redis.Connection.create(host=redis_url, port=redis_port)
        # Create subscriber.
        logger.info('connection created {}'.format(connection))
        logger.info('connection opened to redis from publish')
        # Create transaction
        message = str(message)
        await connection.publish('Work', message)
        connection.close()
        return True
    except:
        return False
    logger.info('{}, message has been published to redis'.format(message))

async def start_pubsub():
    try: 
        connection = await asyncio_redis.Connection.create(host=redis_url, port=redis_port)
        logger.info('Redis Connection Succeeded')

        subscriber = await connection.start_subscribe()
        await subscriber.subscribe([ 'Messages' ])
        logger.info('subscribed to channel')

        # inPubSub = await connection.in_pubsub()
        # logging.info('In the Pubsub? - {}'.format(inPubSub))

        while True:
            reply = await subscriber.next_published()
            publish_work(reply)
            logger.info('Message received {}'.format(reply))
        # When finished, close the connection.
        connection.close()
        # start_pubsub_work(reply)
    except:
        logger.info('Did Not Join Message Pubsub')
    return

asyncio.run(start_pubsub())