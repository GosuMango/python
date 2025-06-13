#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgi
import cgitb
import random
import json
import os

cgitb.enable()

STATE_FILE = "/home/students/odd/2027/myu70/public_html/final/memory"

titles = {
    (-float('inf'), -1000000): "Beyond Homeless 🥀❤️‍🩹",
    (-1000000, -10000): "Big Bum 🥀",
    (-10000, 2500): "Lvl 1 Crook",
    (2500, 10000): "Lvl 25 Mafia Member",
    (10000, 1000000): "Lvl 100 Mafia Boss",
    (1000000, float('inf')): "Supreme Gambling Entity"
}

def get_title(money):
    for (low, high), title in titles.items():
        if low < money <= high:
            return title
    return "Gambler"

def load_state():
    global money, odds
    default_state = {
        "money": 1000.0,
        "odds": {
            "full loss": 0.45,
            "small loss": 0.25,
            "small win": 0.25,
            "big win": 0.04,
            "jackpot": 0.01
        }
    }

    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                money = data.get("money", 1000.0)
                odds = data.get("odds", default_state["odds"])
        except json.JSONDecodeError:
            money = default_state["money"]
            odds = default_state["odds"]
    else:
        money = default_state["money"]
        odds = default_state["odds"]

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump({"money": money, "odds": odds}, f)

def normalize(odds):
    total = sum(odds.values())
    return {k: v / total for k, v in odds.items()}

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

def multigamble(bet, times):
    results = []
    for _ in range(times):
        if bet > 0:
            result = gamble(bet)
            results.append(result)
    return results

def boost_wins(cost=100):
    global money, odds
    if money < cost:
        return "Not enough money to boost."
    money -= cost
    reduce_full = min(0.01, odds["full loss"])
    reduce_small = min(0.01, odds["small loss"])
    gain = reduce_full + reduce_small
    odds["full loss"] -= reduce_full
    odds["small loss"] -= reduce_small
    odds["small win"] += gain * 0.5
    odds["big win"] += gain * 0.3
    odds["jackpot"] += gain * 0.2
    odds = normalize(odds)
    return "Win odds boosted!"

def boost_jackpot(cost=150):
    global money, odds
    if money < cost:
        return "Not enough money to boost jackpot."
    money -= cost
    reduce_small_win = min(0.01, odds["small win"])
    reduce_big_win = min(0.01, odds["big win"])
    total_gain = reduce_small_win + reduce_big_win
    odds["small win"] -= reduce_small_win
    odds["big win"] -= reduce_big_win
    odds["jackpot"] += total_gain
    odds = normalize(odds)
    return "Jackpot chance boosted!"

def brokey():
    global money
    if money <= 250:
        money += 500
        return "You were given $500."
    return "Stop being a greedy bum."

load_state()

data = cgi.FieldStorage()
message = ""

if "action" in data:
    action = data["action"].value
    bet = float(data.getfirst("bet", "0"))
    max_bet = abs(money) * 1.5 if money < 0 else money * 1.5

    if action == "Gamble":
        if bet > 0 and bet <= max_bet:
            result = gamble(bet)
            message = f"Gambling Result: {result}. Money: ${money:.2f}"
        else:
            message = "<p class = 'bigsize'> Invalid bet. Must be a positive number up to 1.5x your balance. </p>"
    elif action in ["3x Gamble", "5x Gamble", "10x Gamble"]:
        multiplier = int(action.split("x")[0])
        if bet > 0 and bet * multiplier <= max_bet:
            results = multigamble(bet, multiplier)
            message = f"{action} Results: {', '.join(results)}. Money: ${money:.2f}"
        else:
            message = "<p class = 'bigsize'> Invalid bet. Must be a positive number up to 1.5x your balance. </p>"
    elif action == "Boost Odds":
        message = boost_wins()
    elif action == "Boost Jackpot":
        message = boost_jackpot()
    elif action == "broke?":
        message = brokey()
    elif action == "Restart?":
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        load_state()
        message = "Game has been reset."

player_title = get_title(money)

print(f"""
<html>
<head>
    <meta charset="utf-8">
    <link href="final.css" rel="stylesheet">
    <title>{player_title}</title>
</head>
<body>
    <p class = "bigsize"> {player_title} </p>
    <p class = "bigsize"> <strong>Money:</strong> ${money:.2f}</p>
    <form method="get" class = "bigsize">
        Bet Amount: <input type="text" class = "bigsize" name="bet">
        <input type="submit" name="action" class = "bigsize" value="Gamble">
        <input type="submit" name="action" class = "bigsize" value="3x Gamble">
        <input type="submit" name="action" class = "bigsize" value="5x Gamble">
        <input type="submit" name="action" class = "bigsize" value="10x Gamble">
        <br><br>
        <input type="submit" name="action" class = "bigsize" value="Boost Odds">
        <input type="submit" name="action" class = "bigsize" value="Boost Jackpot">
        <input type="submit" name="action" class = "bigsize" value="broke?">
        <input type="submit" name="action" class = "bigsize" value="Restart?">       
    </form>
    <p>{message}</p>
    <p class = "bigsize">Current Odds:</p>
    <ul>
""")

for outcome in odds:
    print(f"<li class = 'bigsize'>{outcome}: {odds[outcome]*100:.2f}%</li>")

print("""
    </ul>
</body>
</html>
""")

save_state()
