import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

// 移除了 public 修饰符，使得 MqttSubscriber 类变成包级私有
class MqttSubscriber {

    private MqttClient client;
    private MqttConnectOptions options = new MqttConnectOptions();

    public void connectAndSubscribe(String brokerUrl, String clientId, String topic, int qos) throws MqttException {
        String serverURI = "tcp://" + brokerUrl;
        client = new MqttClient(serverURI, clientId, new MemoryPersistence());
        options.setCleanSession(true); // 假设你想要一个干净的会话
        client.connect(options);
        client.subscribe(topic, qos, this::messageArrived);
    }

    public void disconnect() throws MqttException {
        if (client != null && client.isConnected()) {
            client.disconnect();
        }
    }

    private void messageArrived(String topic, MqttMessage message) {
        System.out.println("Received message: " + new String(message.getPayload()) + " on topic: " + topic);
    }
}

// 创建一个新的类，用于启动和运行 MqttSubscriber
class ScriptMain {
    public static void main(String[] args) {
        MqttSubscriber subscriber = new MqttSubscriber();
        // 填入你的 MQTT 服务器 URL、客户端 ID、主题和 QoS
        String brokerUrl = "your_broker_url";
        String clientId = "your_client_id";
        String topic = "your_topic";
        int qos = 1; // Quality of Service Level
        try {
            subscriber.connectAndSubscribe(brokerUrl, clientId, topic, qos);
            // 假设你想要在接收到消息后立即断开连接，或者在这里添加逻辑等待消息
            subscriber.disconnect();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }
}