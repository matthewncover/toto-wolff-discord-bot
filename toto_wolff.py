import discord
from discord.ext import tasks, commands

import os, json, numpy as np, pandas as pd, datetime as dt

os.chdir("./discord_bots/toto-wolff-discord-bot")

base_date = "Jan 8 2023 07:00:00"
id_dict = json.load(open("ids_debug.json"))
# id_dict = json.load(open("ids_aof.json"))

def read_wolff_quotes():
    df_wolff = pd.read_csv("wolff_quotes.csv")
    df_wolff.datetime_posted = pd.to_datetime(df_wolff.datetime_posted)

    return df_wolff

def select_quote(df_wolff):
    selected_quote = np.random.choice(
        df_wolff
        .sort_values(by="datetime_posted")
        .head(10)
        .quotes
        .tolist()
    )
    
    return selected_quote

def update_save_data(df_wolff, selected_quote):
    df_wolff.loc[df_wolff.quotes == selected_quote, "datetime_posted"] = dt.datetime.now()

    df_wolff.to_csv("wolff_quotes.csv", index=False)

def is_time_to_post_quote():

    def get_timestamp(date_str):

        return dt.datetime.strptime(date_str, "%b %d %Y %H:%M:%S").timestamp()

    base_timestamp = get_timestamp(base_date)

    current_timestamp = dt.datetime.now().timestamp()

    seconds_diff_from_week = abs(base_timestamp - current_timestamp) % 604800
    if seconds_diff_from_week <= 150:
        return True
    elif 604800 - seconds_diff_from_week < 150:
        return True

    return False

client = commands.Bot(command_prefix="$toto")

@tasks.loop(minutes=5)
async def send_message():

    if is_time_to_post_quote():
        channel = client.get_channel(id_dict["channel-id"])

        df_wolff = read_wolff_quotes()
        quote = select_quote(df_wolff)
        update_save_data(df_wolff, quote)

        await channel.send(quote)

@client.event
async def on_ready():

    send_message.start()

client.run(id_dict['bot-token'])