using Unity.VisualScripting.Antlr3.Runtime;
using UnityEngine;

public class RoomLight : MonoBehaviour
{
    public Material lightMaterial;
    public bool isOn = true;
    public void On()
    {
        isOn = true;
        this.gameObject.SetActive(true);
        lightMaterial.EnableKeyword("_EMISSION");

    }

    public void Off()
    {
        isOn = false;
        this.gameObject.SetActive(false);
        lightMaterial.DisableKeyword("_EMISSION");

    }
}
