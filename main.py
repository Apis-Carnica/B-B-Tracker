#!/usr/bin/env python

import os
import random
from datetime import datetime, timedelta
import discord
from dotenv import load_dotenv
import requests
import ssl
import mysql.connector


t_id = ''
d_id = ''
points = 0
hours = 0
messages = 0
activities = 0

url = requests.get("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=<your client id goes here>&redirect_uri=http://localhost:3000&scope=channel%3Amanage%3Apolls+channel%3Aread%3Apolls&state=c3ab8aa609ea11e793ae92361f002671")


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASSWD')


def usersConnect():
    return mysql.connector.connect(
        host='localhost',
        user=DB_USER,
        password=DB_PASS,
        database="bnb")

def usersSetRecord(t_id, d_id, points, hours, messages, activities):
    """
    Takes the variables and sets them as a record in the users table if the
    email isn't in the verified table
    """
    conx = usersConnect()
    cursor = conx.cursor()
    sql = "INSERT INTO users (t_id, d_id, points, hours, messages, activities) VALUES (%s, %s, %s, %s)"
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

client = discord.Client()


@client.event
async def on_ready():
    print("Logged on as {}".format(client.user))


@client.event
async def on_message(message):
    if message.channel.id == "1253253393913479199":
        if message.content.startswith('$link'):
            t_id = message.content.split(' ')[-1]
            if t_id not null:
                usersSetRecord(t_id, message.author.id, 0, 0, 0, 0)
            elif t_id == '':
                await message.channel.send("Make sure to give us your Twitch username with the link command!")
    

"""
@client.event
async def on_message(message):
    if message.channel.recipient == message.users:
        if message.content.startswith('!email'):
            d_id = message.content.split(' ')[-1]
            code = []
            for _ in range(6):
                code.append(str(random.randint(0,9)))
            code = ''.join(code)
            expiry = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            d_id = str(message.channel.recipient)

            if bool(check_verified(t_id)):
                set_record(t_id, d_id, code, expiry)
                send_email(code, t_id)
                await message.channel.send("An email was sent to the address you provided. If you have trouble finding it, try refreshing your browser, wait a few minutes or check your spam folder. Feel free to reach out to **Ursa#1337** with any questions you have.")

            else:
                await message.channel.send("That email has already been verified. If you think message in error, please make a post in tech-support so our moderators can assist you.")

        elif message.content.startswith('!verify'):
            code = message.content.split(' ')[-1]
            d_id = str(message.channel.recipient)

            if bool(check_record(code, d_id)):
                set_verified(d_id)
                delete_record(d_id)

                guild = client.get_guild(int(GUILD_ID))
                print(guild.id)
                role = discord.utils.get(guild.roles, name='valid')
                print(role.name)
                member = discord.utils.find(lambda m : m.id == message.channel.recipient.id, guild.members)
                print(member.id)
                if role is not None:
                    if member is not None:
                        await member.add_roles(role)
                        await message.channel.send("You're all set! We look forward to learning with you!")
                    else:
                        print("Member doesn't exist.")
                else:
                    print("Role doesn't exist or is misconfigured in '.env'.")
            else:
                await message.channel.send("It looks like your code is wrong, please try again.")

        elif message.content.startswith('!delete'):
            field = message.content.split(' ')[-1]

            delete_record(field)
            message.channel.send("We'll get that taken care of for you!")

        else:
            pass
"""

client.run(TOKEN)
