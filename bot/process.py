import time
from app import animals, monopoly
import help

def get_text_msg(message):
    return {
            "name": "bot",
            "message": message,
            "timestamp": round(time.time() * 1000)
        }

def get_img_msg(link, message):
    return {
            "name": "bot",
            "message": message,
            "image": link,
            "hasImage": True,
            "timestamp": round(time.time() * 1000)
        }

def help_processor(item):
    if item in help.items:
        return help.items[item]
    return f"No help found for {item}"

def prepare_response(user,message,reply):
    return f"<small>{user}: {message}</small><br>{reply}"

def process_message(user, message):
    parts = message.split(" ")[1:]
    reply_text = ""
    if parts[0] in animals.animal_list:
        return get_img_msg(animals.get_animal_image(parts[0]),f"{user} your {parts[0]} is here.")
    elif parts[0] in monopoly.mono_list:
        reply_text = monopoly.mono_hander(user,parts)
    elif parts[0] == "help":
        help_item = parts[1] if len(parts) > 1 else ""
        reply_text = help_processor(help_item)
    else:
        reply_text = f"sorry {user} didn't recognise {message}. <br>Try `pls help`"
    return get_text_msg(prepare_response(user,message,reply_text))