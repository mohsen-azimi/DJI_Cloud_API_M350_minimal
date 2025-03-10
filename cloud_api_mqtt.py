#!/usr/bin/env python3

import os
import json
import pprint

from importlib.metadata import version

import yaml
import paho
import paho.mqtt.client as mqtt

configs = yaml.safe_load(open("config.yaml"))



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))


    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sys/#")
    client.subscribe("thing/#")
    print("🔗Subscribed")

    # subscribe wildcard (all) topics
    client.subscribe("#")

# Print interesting bits from message
def handle_osd_message(message: dict):
    data = message["data"]
    lat = data.pop("latitude", None)
    lon = data.get("longitude", None)

    # drop some data we are not interested in
    attitude_head = data.pop("attitude_head", None)
    attitude_pitch = data.pop("attitude_pitch", None)
    attitude_roll = data.pop("attitude_roll", None)
    height = data.pop("height", None)
    data.pop("wireless_link", None)
    data.pop("wireless_link_state", None)
    data.pop("battery", None)
    data.pop("live_status", None)

    print(
        f"🌍Status: Lat: {lat} Lon: {lon} height: {height} att_head {attitude_head} att_pitch {attitude_pitch} att_roll {attitude_roll}"
    )
    pprint.pprint(data)


# The callback for when a PUBLISH message is received from the server.
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    print("📨Got msg: " + msg.topic)
    try:
        message = json.loads(msg.payload.decode("utf-8"))
        print(f"📩 Raw Message: {message}")
    except Exception as e:
        print(f"Error decoding message: {e}")
        return


    if msg.topic.endswith("status"):
        if message["method"] != "update_topo":
            return
        response = {
            "tid": message["tid"],
            "bid": message["bid"],
            "timestamp": message["timestamp"] + 2,
            "data": {"result": 0},
        }
        client.publish(msg.topic + "_reply", payload=json.dumps(response))
        print("✅published")
    elif msg.topic.endswith("osd") and msg.topic.startswith("thing"):
        handle_osd_message(message)

PAHO_MAIN_VER = int(version("paho-mqtt").split(".")[0])
if PAHO_MAIN_VER == 1:
    client = mqtt.Client(transport="tcp")
if PAHO_MAIN_VER == 2:
    client = mqtt.Client(paho.mqtt.enums.CallbackAPIVersion.VERSION2, transport="tcp")
client.on_connect = on_connect
client.on_message = on_message


# client.connect(host_addr, 1883, 60)
client.connect(configs["mqtt"]["HOST"], configs["mqtt"]["PORT"], 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

