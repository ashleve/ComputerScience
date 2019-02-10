using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarController : MonoBehaviour {

    public NeuralNet NN;
    public float[] inputs;

    public float fitnessScore;
    public Vector3 spawn;
    public Quaternion spawnRotation;
    public Quaternion rotation;

    float ACCELERATION = 20.0f;
    float TURN_SPEED = 90.0f;
    float MAX_SPEED = 30.0f;

    float velocity = 0.0f;

    public int time = 0;
    public bool showRay = false;
    public bool awake = true;
    public bool reachedTheGoal = false;

    List<float> l = new List<float>();
    public float[] OutputLayer;

    RaycastHit hit;
    List<Vector3> rayPosList = new List<Vector3>();
    float rayLength = 15.0f;


    // Use this for initialization
    void Start()
    {
        GetRays();
        inputs = new float[rayPosList.Count];

        spawn = transform.position;
        spawnRotation = transform.rotation;

        int numberOfInputs = rayPosList.Count;
        //int numberOfOutputs = CarManager.numberOfOutputs;
        NN = new NeuralNet(numberOfInputs, 6, 2);
    }

    void GetRays()
    {
        float angle = 3.1415f;
        float step = 0.5f;
        while(angle < 2*3.1415f)
        {
            float x = Mathf.Cos(angle);
            float y = Mathf.Sin(angle);
            rayPosList.Add(new Vector3(x, 0, y));
            angle += step;
        }
    }


    // Unity method for physics updates
    void FixedUpdate()
    {
        //if(GetComponent<Rigidbody>().velocity.magnitude < maxSpeed)
        //{
        //    GetComponent<Rigidbody>().AddRelativeForce(-Vector3.forward * 25);
        //}
        if (awake)
        {

        for(int i = 0; i < rayPosList.Count; i++)
        {
            Ray ray = new Ray(transform.position, transform.rotation * rayPosList[i] );

            if (Physics.Raycast(ray, out hit, rayLength))
            {
                if(showRay)
                    Debug.DrawRay(transform.position, transform.rotation * rayPosList[i] * rayLength, Color.red);
                inputs[i] = 1.0f;
            }
            else
            {
                if (showRay)
                    Debug.DrawRay(transform.position, transform.rotation * rayPosList[i] * rayLength, Color.green);
                inputs[i] = 0.0f;
            }
        }

        ForwardPropagate();
        //UpdateOutputs();
        ApplyForces();
        time++;
        }
    }

    private void ApplyForces()
    {
        float engineForce = NN.OutputLayer[0].value;
        float turning = NN.OutputLayer[1].value;

        if (engineForce > 1) engineForce = 1f;
        else if (engineForce < -1) engineForce = -1f;

        if (turning > 1) turning = 1f;
        else if (turning < -1) turning = -1f;


        velocity += engineForce * ACCELERATION * Time.deltaTime;
        if (velocity > MAX_SPEED) velocity = MAX_SPEED;
        else if (velocity < -MAX_SPEED) velocity = -MAX_SPEED;

        rotation = transform.rotation;
        rotation *= Quaternion.AngleAxis(turning * TURN_SPEED * Time.deltaTime, new Vector3(0, 1, 0));

        transform.rotation = rotation;
        Vector3 direction = new Vector3(0, 0, 1);
        direction = rotation * direction;
        transform.position += direction * velocity * Time.deltaTime;


    }

    public void UpdateOutputs()
    {
        l.Clear();
        foreach (var Neuron in NN.OutputLayer)
            l.Add(Neuron.value);
        OutputLayer = l.ToArray();
    }



    public void Respawn()
    {
        //GetComponent<Rigidbody>().velocity = Vector3.zero;
        transform.rotation = spawnRotation;

        //SetConstraints();
        transform.position = spawn;
        velocity = 0.0f;
        awake = true;
        time = 0;
    }


    public void SetConstraints()
    {
        GetComponent<Rigidbody>().constraints = RigidbodyConstraints.FreezeAll;
    }


    public void ReleaseConstraints()
    {
        GetComponent<Rigidbody>().constraints = RigidbodyConstraints.None;
    }

    public void ForwardPropagate()
    {
        NN.ForwardPropagate(inputs);
    }



    void OnCollisionEnter(Collision other)
    {
        if(other.gameObject.tag == "Wall")
        {
            SetConstraints();
            awake = false;
        }
        if (other.gameObject.tag == "Target")
        {
            reachedTheGoal = true;
        }
    }


}
