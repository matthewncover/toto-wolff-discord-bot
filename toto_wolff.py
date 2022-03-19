import discord
from discord.ext import tasks, commands

import json, requests, numpy as np, pandas as pd
from bs4 import BeautifulSoup

# id_dict = json.load(open("ids_debug.json"))
id_dict = json.load(open("ids_aof.json"))

def get_wolff_quotes():

    wolff_quotes = []

    url = "https://www.brainyquote.com/authors/toto-wolff-quotes"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    wolff_quotes += [
        result.get_text().replace("\n", "")
        for result in soup.find_all("a", {"class": "b-qt"})
    ]

    url = "https://www.whatshouldireadnext.com/quotes/authors/toto-wolff"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    wolff_quotes += [
        result.get_text().replace("\n", "") 
        for result in soup.find_all("a", {"class": "quote-card__text"})
    ]

    url = "https://www.quotes.net/authors/Toto+Wolff"
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    wolff_quotes += [
        result.get_text() 
        for result in soup.find_all("blockquote")
    ]

    # from F1 drive to survive
    wolff_quotes += [
        "Do you drink? Do you drink during the day? You do."
    ]

    super_legit_wolff_quotes = [
        "Contrary to public opinion, the liberal media, and words I may have quite explicitly said, I was actually stoked Valtteri Bottas won the Austrian Grand Prix.",
    ]

    wolff_quotes = pd.Series(wolff_quotes).unique().tolist()

    return wolff_quotes, super_legit_wolff_quotes

def choose_wolff_quote():

    # if np.random.random() > 0.95:
    #     return np.random.choice(super_legit_wolff_quotes, 1)[0]
    # else:
    return np.random.choice(wolff_quotes, 1)[0]

wolff_quotes, super_legit_wolff_quotes = get_wolff_quotes()

client = commands.Bot(command_prefix="$420")

@tasks.loop(minutes=5)
async def send_message():

    channel = client.get_channel(id_dict["channel-id"])

    quote = choose_wolff_quote()

    await channel.send(quote)

@client.event
async def on_ready():

    send_message.start()

client.run(id_dict['bot-token'])