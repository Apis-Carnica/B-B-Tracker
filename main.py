#!/usr/bin/env python

import os
import random
from datetime import datetime, timedelta
import discord
import requests
import ssl
import mysql.connector


t_id = ''
d_id = ''
points = 0
hours = 0
messages = 0
activities = 0


TOKEN = os.getenv('DISCORD_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')


def usersConnect():
    return mysql.connector.connect(
        auth_plugin='auth_socket',
        host='localhost',
        user=DB_USER,
        password=DB_PASS,
        database="bnb")

def usersSetRecord(t_id: str, d_id: str, points: int, hours: int, messages: int, activities: int):
    """
    Takes the variables and sets them as a record in the users table if the
    email isn't in the verified table
    """
    conx = usersConnect()
    cursor = conx.cursor()
    sql = "INSERT INTO users (t_id, d_id, points, hours, messages, activities) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (t_id, d_id, points, hours, messages, activities)
    cursor.execute(sql, val)
    conx.commit()

def usersCheckRecord(t_id: str) -> list:
    """
    Sends a SELECT query from the users server and verifies the variables.
    Returns True if the code supplied matches the one populating the record.
    """
    conx = usersConnect()
    cursor = conx.cursor()
    sql = "SELECT * FROM users WHERE t_id = %s"
    val = (t_id)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result

def usersDeleteRecord(t_id: str):
    "Deletes the selected table from the table"
    # Check for symbols to qualify index type: d_id -> email
    conx = usersConnect()
    cursor = conx.cursor()
    sql = "DELETE FROM users WHERE t_id = %s"
    val = (t_id)
    cursor.execute(sql, val)
    conx.commit()


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Logged on as {}".format(client.user))


@client.event
async def on_message(message):
    print(message.content)
#    if message.content.startswith('$link'):
        #t_id = message.content.split(' ')[-1]
        #usersSetRecord(t_id, str(message.author.id), 0, 0, 0, 0)
        #await message.channel.send("User has been added.")


@client.event
async def on_message(message):
    if message.channel.id == 1253253393913479199:
        if message.content == '$erm':
            erm = os.getenv('ERM')
            os.environ['ERM'] = str(int(erm) + 1)
            await message.channel.send("Tigerfart has said 'erm' {} times!".format(os.getenv('ERM')))

client.run(TOKEN)
