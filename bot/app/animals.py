import requests

animal_list = ["dog","bark","bork","cat","meow","pussy","movingcat"]

def get_animal_image(animal):
    if animal in ["dog","bark","bork"]:
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
    elif animal in ["cat","meow","pussy"]:
        contents = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]
        url = contents["url"]
    
    
    elif animal == "movingcat":
        import random
        num = str(random.randint(1,100000))
        url = "https://cataas.com/cat/gif?lol"+num
    return url
