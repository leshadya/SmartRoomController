using TMPro;
using UnityEditor.Rendering;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    public static UIManager Instance;
    public TextMeshProUGUI temperature;
    public TextMeshProUGUI humidity;
    public TextMeshProUGUI co2;
    public TextMeshProUGUI time;
    public GameObject fireWarningPanel;

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }

    }
}
