using UnityEngine;
using System.Collections;

public class OpenableWindow : MonoBehaviour
{
    public bool isOpen;
    [SerializeField] AudioSource openSound;
    [SerializeField] AudioSource closeSound;

    public IEnumerator RotateY(Transform target, float startY, float endY, float duration)
    {
        float elapsed = 0f;

        Quaternion startRot = Quaternion.Euler(0, startY, 0);
        Quaternion endRot = Quaternion.Euler(0, endY, 0);

        while (elapsed < duration)
        {
            float t = elapsed / duration;
            target.rotation = Quaternion.Slerp(startRot, endRot, t);
            elapsed += Time.deltaTime;
            yield return null;
        }

        // Son hali tam otursun
        target.rotation = endRot;
    }

    public void Open()
    {
        isOpen = true;
        openSound.Play();
        StartCoroutine(RotateY(transform, 0, -86, 1f));

    }

    public void Close()
    {
        isOpen = false;
        closeSound.Play();
        StartCoroutine(RotateY(transform, -86, 0, 1f));
    }
}
