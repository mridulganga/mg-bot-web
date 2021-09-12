from collections import UserList
from random import randint
import re
from app import db
from app.utils import choose_random,load_replies,random
import datetime

mono_list = ["balance","beg","search","steal","gamble","inventory","buy","sell","use","shop","market","store","deposit","withdraw","loan","share","send","rich"]

def get_ref_user(message):
    for part in message:
        if "@" in part:
            return part.replace("@")
    return None

def get_money_value(message,all_amount,money_index=1):
    money = 0
    if len(message) == money_index or message[money_index] == "all":
        money = int(all_amount)
    else:
        try: money = int(message[1])
        except: return None
    if money > all_amount:
        return None
    return money    


def mono_hander(user, message):
    print(user, message)
    sub = db.get_or_create_user(user)
    ref_user = None
    if get_ref_user(message):
        ref_user = db.get_or_create_user(get_ref_user(message))

    if message[0] == "balance":
        u = sub
        if ref_user:
            u = ref_user
        return "<br>".join([f"**Balance for {u['username']}**",f"Wallet: {u['wallet']}",f"Bank: {u['bank']}"])
    
    if message[0] == "beg":
        if "last_beg" in sub:
            if (datetime.datetime.today() - sub["last_beg"]).seconds < 10:
                return f"**{user}** you're begging too much. Stop it!! (wait {10-int((datetime.datetime.today() - sub['last_beg']).seconds)} seconds)"

        beg_from = choose_random(load_replies("donators"))
        beg_line = choose_random(load_replies("beg_lines"))
        
        beg_amount = random.randint(10,100)
        sub["last_beg"] = datetime.datetime.today()
        sub["wallet"] += beg_amount
        db.update_user(sub)
        return f"**{beg_from}** donated **{beg_amount}** to **{user}**. {beg_line}"

    if message[0] == "search":
        if "last_search" in sub:
            if (datetime.datetime.today() - sub["last_search"]).seconds < 10:
                return f"**{user}** you need to wait {10-int((datetime.datetime.today() - sub['last_search']).seconds)} seconds before searching again."

        search_line = choose_random(load_replies("search_lines"))
        
        search_amount = random.randint(100,300)
        sub["last_search"] = datetime.datetime.today()
        sub["wallet"] += search_amount
        db.update_user(sub)
        return f"Congrats **{user}** you found **{search_amount}** {search_line}"

    if message[0] == "withdraw":
        money = 0
        if len(message) == 1 or message[1] == "all":
            money = int(sub['bank'])
        else:
            try: money = int(message[1])
            except: return "Please Enter a numeric value or all."
        # deduct from bank and add to wallet
        if money > sub["bank"]:
            return "You dont have that kind of money in your bank."
        sub["wallet"] += money
        sub["bank"] -= money
        db.update_user(sub)
        return f"{money} has been withdrawn."

    if message[0] == "deposit":
        money = 0
        if len(message) == 1 or message[1] == "all":
            money = int(sub['wallet'])
        else:
            try: money = int(message[1])
            except: return "Please Enter a numeric value or all."
        # deduct from wallet and add to bank
        if money > sub["wallet"]:
            return "You dont have that kind of money in your wallet."
        sub["wallet"] -= money
        sub["bank"] += money
        db.update_user(sub)
        return f"{money} has been deposited."

    if message[0] == "steal":
        if not ref_user:
            return "Whom do you want to steal from?"
        
        money = ref_user['wallet']
        if money < 200 or sub['wallet'] < 200:
            return "Both you and victim should have atleast 200 in your wallet"

        stealSuccess = random.randint(1,2) == 2
        
        reply_text = ""
        if stealSuccess:
            steal_money = random.randint(10,int(money/2))
            ref_user['wallet'] -= steal_money
            sub['wallet'] += steal_money
            reply_text = f"{user} stole {steal_money} from {ref_user['username']}"
        else:
            caught_money = random.randint(10,int(sub['wallet']/2))
            ref_user['wallet'] += caught_money
            sub['wallet'] -= caught_money
            reply_text = f"{user} caught while stealing from {ref_user['username']} and paid them {caught_money}"
        db.update_user(ref_user)
        db.update_user(sub)
        return reply_text


    if message[0] == "gamble":
        money = get_money_value(message,sub['wallet'])
        if not money:
            return "Please Enter a valid numeric value or all."

        gambleSuccess = random.choice([True, True, True, False, False])
        winnings =  int(money*random.randint(60,100)/100)
        reply_text = ""
        if gambleSuccess:
            sub['wallet'] += winnings
            reply_text = f"Congrats!!<br>{user} won in Gamble. They got {winnings}"
        else:
            sub['wallet'] -= money
            reply_text = f"{user} lost {money} in Gamble."
        db.update_user(sub)
        return reply_text
        

    if message[0] in ["share","send"]:
        if not ref_user:
            return "Whom do you want to send money to?"
        money = get_money_value(message,sub['wallet'],2)
        if not money:
            return "Please specify valid amount (numeric)"

        sub['wallet'] -= money
        ref_user['wallet'] += money
        db.update_user(sub)
        db.update_user(ref_user)
        return f"{user} sent {money} to {ref_user['username']}"

    if message[0] == "inventory":
        u = ref_user if ref_user else sub
        if 'inventory' not in u:
            return f"{u['username']} there are no items in your inventory"
        reply_text = f"**{u['username']}'s Inventory**"
        for item,value in u['inventory'].items():
            shop_item = db.get_shop_item(item)
            reply_text += f"<br>{item} ({value}) = {shop_item['price']}"
        return reply_text

    if message[0] == "buy":
        if len(message) < 2:
            return "Please enter a valid item"
        item = message[1]
        shop_item = db.get_shop_item(item)
        if not shop_item:
            return "Please enter a valid item"

        if shop_item['price'] > sub['wallet']:
            return f"You don't have enough money to buy {item}"

        if 'inventory' in sub:
            if item in sub['inventory']:
                maxv = shop_item['max'] if 'max' in shop_item else 5000
                if sub['inventory'][item] <= maxv:
                    sub['inventory'][item] += 1
                    sub['wallet'] -= shop_item['price']
                else:
                    return f"You cannot buy more of {item}"
            else:
                sub['inventory'][item] = 1
                sub['wallet'] -= shop_item['price']
        else:
            sub['inventory'] = {item:1}
            sub['wallet'] -= shop_item['price']
        db.update_user(sub)
        return f"{user} bought {item}"

    if message[0] == "sell":
        if len(message) < 2:
            return "Please enter a valid item"
        item = message[1]
        shop_item = db.get_shop_item(item)
        if not shop_item:
            return "Please enter a valid item"
        if 'inventory' not in sub:
            return "No items in your inventory"
        if item not in sub['inventory']:
            return f"You don't have {item} in your inventory"
        sub['wallet'] += shop_item['price']
        if sub['inventory'][item] > 1:
            sub['inventory'][item] -= 1
        else:
            sub['inventory'].pop(item)
        db.update_user(sub)
        return f"Sold {item}"

    if message[0] == "use":
        if len(message) < 2:
            return "Please enter a valid item"
        item = message[1]
        shop_item = db.get_shop_item(item)
        if not shop_item:
            return "Please enter a valid item"
        if 'inventory' not in sub:
            return "No items in your inventory"
        if sub['inventory'][item] > 1:
            sub['inventory'][item] -= 1
        else:
            sub['inventory'].pop(item)
        db.update_user(sub)
        return f"Used {item}"

    if message[0] in ["shop","market","store"]:
        reply_text = "**Shop Items**"
        for item in db.get_shop_items():
            reply_text += f"<br>{item['name']} = {item['price']}"
        return reply_text

    if message[0] == "rich":
        reply_text = "**Rich People**"
        for u in db.get_users():
            reply_text += f"<br>{u['username']} = {u['wallet']}"
        return reply_text
