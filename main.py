#!/usr/bin/env python

import os
import random
from datetime import datetime, timedelta
import dotenv
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import requests
import ssl
import mysql.connector


load_dotenv(dotenv.find_dotenv())


TOKEN = os.environ['DISCORD_TOKEN']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']


def dbConnect():
    return mysql.connector.connect(
        auth_plugin='auth_socket',
        host='localhost',
        user=DB_USER,
        password=DB_PASS,
        database="bnb")


# Sheets table db operations

def sheetCreate(id: str,):
    conx = dbConnect()
    cursor = conx.cursor()
    sql = "INSERT INTO sheets (id) VALUES (%s)"
    val = (id)
    cursor.execute(sql, val)
    conx.commit()

def sheetFind(id: str) -> list:
    conx = dbConnect()
    cursor = conx.cursor()
    sql = "SELECT * FROM sheets WHERE id = %s"
    val = (id)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result

def sheetDelete(id: str):
    conx = dbConnect()
    cursor = conx.cursor()
    sql = "DELETE FROM sheets WHERE id = %s"
    val = (id)
    cursor.execute(sql, val)
    conx.commit()


def sheetUpdate(id: str):
    conx = dbConnect()
    cursor = conx.cursor()
    sql = "UPDATE sheets SET id = %s, " # put the columns in lazy.
    val = (id)
    cursor.exesute(sql, val)
    conx.commit()


# Users table db operations

def usersSetRecord(t_id: str, d_id: str, points: int, hours: int, messages: int, activities: int):
    """
    Takes the variables and sets them as a record in the users table if the
    email isn't in the verified table
    """
    conx = dbConnect()
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
    conx = dbConnect()
    cursor = conx.cursor()
    sql = "SELECT * FROM users WHERE t_id = %s"
    val = (t_id)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result

def usersDeleteRecord(t_id: str):
    "Deletes the selected table from the table"
    # Check for symbols to qualify index type: d_id -> email
    conx = dbConnect()
    cursor = conx.cursor()
    sql = "DELETE FROM users WHERE t_id = %s"
    val = (t_id)
    cursor.execute(sql, val)
    conx.commit()


bot = commands.Bot(command_prefix = '$', intents = discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)


@bot.tree.command(name='erm')
async def erm(interaction: discord.Interaction):
    erm = os.environ['ERM']
    await interaction.response.send_message(f"Tigerfae has said 'erm' {erm} times!")
    dotenv.set_key(dotenv.find_dotenv(), "ERM", str(int(erm) + 1))


@bot.tree.command(name='link')
@app_commands.describe(t_id = 'Your Twitch account name')
async def link(interaction: discord.Interaction, t_id: str):
        usersSetRecord(t_id, str(interaction.user.id), 0, 0, 0, 0)
        await interaction.response.send_message(f"You've successfully tied the user `{t_id}` to your account, {interaction.user.name}!")


#@client.command()

bot.run(TOKEN)
