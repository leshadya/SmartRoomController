using UnityEngine;

namespace WindTriggerSystem
{
    public class WindTrigger : MonoBehaviour
    {
        [Header("Fan Rotation")]
        [SerializeField] private Transform _fanRotation;
        [SerializeField] private float _fanRotateSpeed;
        public static bool _isFanOn = false;


        //sil:
        [SerializeField] private float _fanAcceleration = 0.2f;
        [SerializeField] private float _minFanSpeed = 0.0f;
        [SerializeField] private float _maxFanSpeed = 1500f;


        void Update()
        {
            if (_isFanOn)
            {
                _fanRotation.Rotate(Vector3.up * _fanRotateSpeed * Time.deltaTime);
            }
          

            /*
            if (Input.GetKeyDown(KeyCode.Space))
            {
                _isFanOn = true;
            }
            if (Input.GetKeyDown(KeyCode.P))
            {
                _isFanOn = false;
            }

            if (_isFanOn)
            {
                Acceleration();
            }
            else
            {
                Deceleration();
            }*/


        }

        
        private void Acceleration()
        {
            _fanRotateSpeed += _fanAcceleration;
           
            if (_fanRotateSpeed > _maxFanSpeed)
            {
                _fanRotateSpeed = _maxFanSpeed;
            }

           
        }

        private void Deceleration()
        {
            _fanRotateSpeed -= _fanAcceleration;
            

            if (_fanRotateSpeed < _minFanSpeed)
            {
                _fanRotateSpeed = _minFanSpeed;
            }

           
        }
    }
}