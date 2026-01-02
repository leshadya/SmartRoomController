using System.Collections;
using UnityEngine;
using UnityEngine.Experimental.GlobalIllumination;

public class FireAlarmSystem : MonoBehaviour
{
    [Header("Components")]
    public Light alarmLight;        
    public Material sirenMaterial;   
    public AudioSource sirenAudio;    

    [Header("Settings")]
    public float blinkInterval = 0.5f;

    public bool isAlarmActive = false;
    private Coroutine _flashCoroutine;

    private void Start()
    {
        alarmLight.enabled = false;
    }
    public void SetAlarmState(bool isActive)
    {
        if (isActive)
        {
            if (isAlarmActive) return;

            isAlarmActive = true;
            if (!sirenAudio.isPlaying) sirenAudio.Play();

            //Start Light Flashing Routine
            if (_flashCoroutine != null) StopCoroutine(_flashCoroutine);
            _flashCoroutine = StartCoroutine(FlashLightsRoutine());
        }
        else
        {
            isAlarmActive = false;
            sirenAudio.Pause();
            if (_flashCoroutine != null) StopCoroutine(_flashCoroutine);
            ToggleVisuals(false);  //Reset Lights to Off (Cleanup)
        }
    }

    // Coroutine to handle the timing of the flashing lights
    IEnumerator FlashLightsRoutine()
    {
        while (isAlarmActive)
        {
            // Turn Lights ON
            ToggleVisuals(true);
            yield return new WaitForSeconds(blinkInterval);

            // Turn Lights OFF
            ToggleVisuals(false);
            yield return new WaitForSeconds(blinkInterval);
        }
    }

    private void ToggleVisuals(bool isOn)
    {
        if (alarmLight != null) alarmLight.enabled = isOn;

        if (sirenMaterial != null)
        {
            if (isOn) sirenMaterial.EnableKeyword("_EMISSION");
            else sirenMaterial.DisableKeyword("_EMISSION");
        }
    }
}