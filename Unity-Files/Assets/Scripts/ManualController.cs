using UnityEngine;
using UnityEngine.UI;

public class ManualController : MonoBehaviour
{
    [SerializeField] SmartRoomController roomController;
    [SerializeField] Image offImage;

    public enum DeviceType
    {
        Fan,
        Window,
        Light
    }

    public DeviceType deviceType;
    public Toggle toggle;

    private void Start()
    {
        toggle.onValueChanged.AddListener(OnToggleChanged);
    }

    void OnToggleChanged(bool isOn)
    {
        if (!isOn)
        {
            offImage.gameObject.SetActive(true);

        }
        else
        {
            offImage.gameObject.SetActive(false);

        }

        switch (deviceType)
        {
            case DeviceType.Fan:
                FanToggle(isOn);
                break;

            case DeviceType.Window:
                WindowToggle(isOn);
                break;

            case DeviceType.Light:
                LightToggle(isOn);
                break;
        }
    }
    private void OnEnable()
    {
        SyncInitialState();
    }

    void SyncInitialState()
    {
        bool currentState = false;

        switch (deviceType)
        {
            case DeviceType.Fan:
                currentState = roomController.fan.IsFanOn;
                break;

            case DeviceType.Window:
                currentState = roomController.window.isOpen;
                break;

            case DeviceType.Light:
                currentState = roomController.roomLight.isOn;
                break;
        }
        toggle.SetIsOnWithoutNotify(currentState);
        offImage.gameObject.SetActive(!currentState);
    }
    public void FanToggle(bool isOn)    
    { 
        roomController.fan.IsFanOn = isOn;
        if(isOn)
             roomController.ReportStatus("fan_on");
        else
            roomController.ReportStatus("fan_off");

    }

    public void WindowToggle(bool isOn)
    {
        if (isOn)
        {
            roomController.window.Open();
            roomController.ReportStatus("window_open");
        }
        else
        {
            roomController.window.Close();
            roomController.ReportStatus("window_close");
        }

    }

    void LightToggle(bool isOn)
    {
        if (isOn)
        {
            roomController.roomLight.On();
            roomController.ReportStatus("lights_on");
        }
        else
        {
            roomController.roomLight.Off();
            roomController.ReportStatus("lights_off");
        }
       
    }


   
}
