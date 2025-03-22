import paho.mqtt.client as mqtt

from persistence_worker.utils.logger_config import setup_logger


class MQTTClient:
    def __init__(self, broker, port, topic, on_message):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = self.on_disconnect
        self.logger = setup_logger(__name__)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.logger.info(f"🚀 Connected successfully to {self.broker}")
            client.subscribe(self.topic)
            self.logger.info(f"📡 Subscribed to topic: {self.topic}")
        else:
            self.logger.error(f"❌ Failed to connect, reason code: {reason_code}")

    def on_disconnect(self, client, userdata, reason_code):
        self.logger.warning(f"⚠️ Disconnected: {reason_code}")
        self.reconnect()

    def reconnect(self):
        try:
            self.client.reconnect()
        except Exception as e:
            self.logger.error(f"❌ Reconnection failed: {e}")

    def start(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            self.logger.error(f"❌ Connection failed: {e}")

    def stop(self):
        self.logger.info("🛑 MQTT client stopped")
        self.client.disconnect()
        self.client.loop_stop()
