import paho.mqtt.publish as publish

publish.single("casa1/sala/temp", "25.4", hostname="mqtt.eclipse.org")