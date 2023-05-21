import paho.mqtt.client as mqtt

def on_publish(client, userdata, result): 
    print("Data published \n")
    pass

client = mqtt.Client()

client.on_publish = on_publish

client.connect("localhost", 1883, 60)

client.publish("testrangga", "Hello Rangga")
