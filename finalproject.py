#!/usr/bin/env python3
print("Content-type: text/html\n")

import cgi
import cgitb
import random
import json
import os

cgitb.enable()

# State file path
STATE_FILE = "/home/students/odd/2027/myu70/public_html/py/data/finalproject_state"

# Load game state
def load_state():
    global money, odds
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            money = data.get("money", 1000.0)
            odds = data.get("odds", {
                "full loss": 0.45,
                "small loss": 0.25,
                "small win": 0.25,
                "big win": 0.04,
                "jackpot": 0.01
            })
    else:
        money = 1000.0
        odds = {
            "full loss": 0.45,
            "small loss": 0.25,
            "small win": 0.25,
            "big win": 0.04,
            "jackpot": 0.01
        }

# Save game state
def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump({"money": money, "odds": odds}, f)

# Normalize odds
def normalize(odds):
    total = sum(odds.values())
    return {k: v / total for k, v in odds.items()}

# Gambling function
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

# Multiple gamble function
def multigamble(bet, times):
    results = []
    for _ in range(times):
        if bet > 0:
            result = gamble(bet)
            results.append(result)
    return results

# Boost win odds
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

# Boost jackpot odds
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

# Emergency cash
def brokey():
    global money
    if money <= 250:
        money += 500
        return "You were given $500."
    return "Stop being a greedy bum."

# Load state
load_state()

# Handle form data
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
            message = "Invalid bet. Must be a positive number up to 1.5x your balance."
    elif action in ["3x Gamble", "5x Gamble", "10x Gamble"]:
        multiplier = int(action.split("x")[0])
        if bet > 0 and bet <= max_bet:
            results = multigamble(bet, multiplier)
            message = f"{action} Results: {', '.join(results)}. Money: ${money:.2f}"
        else:
            message = "Invalid bet. Must be a positive number up to 1.5x your balance."
    elif action == "Boost Odds":
        message = boost_wins()
    elif action == "Boost Jackpot":
        message = boost_jackpot()
    elif action == "broke?":
        message = brokey()

# Save state
save_state()

# Output HTML
print(f"""
<html>
<head>
    <title>Gambling</title>
</head>
<body>
    <h1>Gambling Game</h1>
    <p><strong>Money:</strong> ${money:.2f}</p>
    <form method="get">
        Bet Amount: <input type="text" name="bet">
        <input type="submit" name="action" value="Gamble">
        <input type="submit" name="action" value="3x Gamble">
        <input type="submit" name="action" value="5x Gamble">
        <input type="submit" name="action" value="10x Gamble">
        <br><br>
        <input type="submit" name="action" value="Boost Odds">
        <input type="submit" name="action" value="Boost Jackpot">
        <input type="submit" name="action" value="broke?">
    </form>
    <p>{message}</p>
    <h2>Current Odds:</h2>
    <ul>
""")

for outcome in odds:
    print(f"<li>{outcome}: {odds[outcome]*100:.2f}%</li>")

print("""
    </ul>
</body>
</html>
""")
