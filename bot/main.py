import paho.mqtt.client as mqtt
import json
import process

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("mgsimplechat")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    obj = json.loads(msg.payload.decode("utf-8"))
    user = obj["name"].lower()
    text = obj["message"].lower()
    if msg.topic == "mgsimplechat" and text[:3]=="pls":
        try:
            payload = process.process_message(user,text)
            print(payload)
            client.publish("mgsimplechat", json.dumps(payload))
        except Exception as e:
            print(f"error {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("hmq.mridulganga.dev", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()