#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgi
import cgitb
import random

cgitb.enable()

# Game state (in practice, store/load from file)
money = 1000
odds = {
    "full loss": 0.45,
    "small loss": 0.25,
    "small win": 0.25,
    "big win": 0.04,
    "jackpot": 0.01
}

def normalize(odds):
    total = sum(odds.values())
    return {k: v / total for k, v in odds.items()}

# Perform a spin
def gamble(bet):
    global money, odds
    r = random.random()
    total = 0
    for outcome, prob in odds.items():
        total += prob
        if r < total:
            if outcome == "full loss":
                money -= bet
            elif outcome == "small loss":
                money -= bet * 0.4
            elif outcome == "small win":
                money += bet * 0.5
            elif outcome == "big win":
                money += bet * 1.2
            elif outcome == "jackpot":
                money += bet * 5
            return outcome
    return "no outcome"

def maxgamble(bet):
    global money
    times = money / bet
    while times != 0:
        gamble(bet)
        times -= 1

# Boost overall win chance
def boost_wins(cost=100):
    global money, odds
    if money < cost:
        return "Not enough money to boost."
    money -= cost
    reduce_full = min(0.005, odds["full loss"])
    reduce_small = min(0.005, odds["small loss"])
    gain = reduce_full + reduce_small
    odds["full loss"] -= reduce_full
    odds["small loss"] -= reduce_small
    odds["small win"] += gain * 0.5
    odds["big win"] += gain * 0.3
    odds["jackpot"] += gain * 0.2
    odds = normalize(odds)
    return "Win odds boosted!"

# Boost jackpot by taking from small/big win
def boost_jackpot(cost=150):
    global money, odds
    if money < cost:
        return "Not enough money to boost jackpot."
    money -= cost
    reduce_small_win = min(0.005, odds["small win"])
    reduce_big_win = min(0.005, odds["big win"])
    total_gain = reduce_small_win + reduce_big_win
    odds["small win"] -= reduce_small_win
    odds["big win"] -= reduce_big_win
    odds["jackpot"] += total_gain
    odds = normalize(odds)
    return "Jackpot chance boosted!"

# Handle form input
data = cgi.FieldStorage()
message = ""
bet = 0
if "action" in data:
    action = data["action"].value
    if action == "Gamble" and "bet" in data:
        try:
            bet = int(data["bet"].value)
            if bet > 0 and bet <= money:
                result = gamble(bet)
                message = f"Gambling Results: {result}. Money: ${money:.2f}"
            else:
                message = ("Invalid bet amount.")
        except:
            message = ("Bet must be a number.")
    elif action == "Max Gamble" and "bet" in data:
        try:
            bet = int(data["bet"].value)
            if bet > 0 and bet <= money:
                result = maxgamble(bet)
                message = f"Gambling Results: {result}. Money: ${money:.2f}"
            else:
                message = ("Invalid bet amount.")
        except:
            message = ("Bet must be a number.")
    elif action == "Boost Odds":
        message = boost_wins()
    elif action == "Boost Jackpot":
        message = boost_jackpot()

# HTML Output
print("""
<html>
<head>
    <title>Gambling</title>
</head>
<body>
    <h1>Gambling</h1>
    <p>Money: ${:.2f}</p>
    <form method="get">
        Bet Amount: <input type="text" name="bet">
        <input type="submit" name="action" value="Gamble">
        <input type="submit" name="action" value="Max Gamble">
        <input type="submit" name="action" value="Boost Odds">
        <input type="submit" name="action" value="Boost Jackpot">
    </form>
    <p>{}</p>
    <h2>Current Odds:</h2>
    <ul>
""".format(money, message))

for outcome in odds:
    print(f"<li>{outcome}: {odds[outcome]*100:.2f}%</li>")

print("""
    </ul>
</body>
</html>
""")
