using System;
using UnityEngine;
using M2MqttUnity;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

public class SmartRoomController : M2MqttUnityClient
{
    [Header("Settings")]
    public string topicToSubscribe = "house/data"; 
    public string topicToPublish = "house/status";

    [Header("Objects to activate: ")]
    [SerializeField] OpenableWindow window;
    [SerializeField] FireAlarmSystem alarmSystem;
    [SerializeField] Fan fan;

    const double FAN_ON_TEMP = 25.0;
    const double FAN_OFF_TEMP = 22.0;
    const double WINDOW_ON_TEMP = 550.0;
    const double WINDOW_OFF_TEMP = 500.0;


    [Serializable]
    public class SensorData
    {
        public float temperature;
        public float co2;
        public float humidity;
        public int smoke;
    }

    // This starts when an MQTT connection is established.
    protected override void OnConnected()
    {
        base.OnConnected();
        Debug.Log("Successfully connected! Subscribing...");
        SubscribeTopics();
    }

    protected override void SubscribeTopics()
    {
        client.Subscribe(new string[] { topicToSubscribe }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE });
    }

    // This part starts when a message arrives
    protected override void DecodeMessage(string topic, byte[] message)
    {
        // Convert incoming byte data to string
        string msg = System.Text.Encoding.UTF8.GetString(message);
        Debug.Log("Received message: " + msg);

        ProcessData(msg);
    }

    private void ReportStatus(string mesaj)
    {
        // We convert the message into a byte array and send it.
        client.Publish(topicToPublish, System.Text.Encoding.UTF8.GetBytes(mesaj));
        Debug.Log("Message sent: " + mesaj);
    }
    private void ProcessData(string jsonData)
    {
        try
        {
           // We are converting JSON data into a C# class.
            SensorData data = JsonUtility.FromJson<SensorData>(jsonData);

            UIManager.Instance.time.text = DateTime.Now.ToString();
            UIManager.Instance.temperature.text = data.temperature.ToString();
            UIManager.Instance.co2.text = data.co2.ToString();
            UIManager.Instance.humidity.text = data.humidity.ToString();
            UIManager.Instance.fireWarningPanel.SetActive(data.smoke == 1);

            //FAN
            if (!fan.IsFanOn && data.temperature >= FAN_ON_TEMP)
            {
                fan.IsFanOn = true;
                ReportStatus("fan_on");
            }
            else if (fan.IsFanOn && data.temperature <= FAN_OFF_TEMP)
            {
                fan.IsFanOn = false;
                ReportStatus("fan_off");
            }

            //WINDOW
            if (!window.isOpen && data.co2 > WINDOW_ON_TEMP)
            {
                window.Open();
                ReportStatus("window_open");

            }
            else if(window.isOpen && data.co2 < WINDOW_OFF_TEMP)
            {
                window.Close(); 
                ReportStatus("window_close");

            }

            //ALARM SYSTEM
            if (!alarmSystem.isAlarmActive && data.smoke == 1)
            {
                alarmSystem.SetAlarmState(true);
                ReportStatus("alarm_on");
                
            }
            else if(alarmSystem.isAlarmActive && data.smoke == 0)
            {
                alarmSystem.SetAlarmState(false);
                ReportStatus("alarm_off");
               
            }

        }
        catch (Exception e)
        {
            Debug.LogError("Data reading error: " + e.Message);
        }
    }


}
