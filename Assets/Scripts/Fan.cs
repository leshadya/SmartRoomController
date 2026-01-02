using UnityEngine;

public class Fan : MonoBehaviour
{
    [SerializeField] private Transform _fanRotation;
    [SerializeField] private float _fanRotateSpeed;
    [SerializeField] private AudioSource _fanOnSound;

    public static bool _isFanOn = false;
    void Update()
    {
        if (IsFanOn)
        {
            _fanRotation.Rotate(Vector3.up * _fanRotateSpeed * Time.deltaTime);
        }
    }

    public bool IsFanOn
    {
        get => _isFanOn;
        set
        {
            _isFanOn = value;
            if (_isFanOn) _fanOnSound.Play();
            else _fanOnSound.Pause();
        }
    }
}
