using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;


public class AutomationToggle : MonoBehaviour
{
    public List<GameObject> targets = new List<GameObject>();

    [SerializeField] Image offImage;


    [Header("State")]
    public bool isOn = true;

    public void Toggle()
    {
        foreach (GameObject obj in targets)
        {
            if (obj != null)
                obj.SetActive(!obj.activeSelf);
        }
        isOn = !isOn;

        if (!isOn)
        {
            offImage.gameObject.SetActive(true);
        }
        else
        {
            offImage.gameObject.SetActive(false);

        }

    }
}
