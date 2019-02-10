using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarManager : MonoBehaviour {

    public GameObject Eve; //The Car used to create new creatures
    public GameObject Target;
    public CarController Champion;

    private int numberOfCreatures = 70;
    private List<CarController> creatures = new List<CarController>();

    //private float movementSpeed = 100.0f;

    private float fitnessSum;
    private float mutationRate = 0.03f;

    private int time = 0;
    private int generation = 0;


    //public static int numberOfOutputs = 2;

    // Use this for initialization
    void Start()
    {
        InitialiseCreatures();
    }



    void FixedUpdate()
    {
        if (AllCrashed() || time > 600)
        {


            NaturalSelection();
            SleepAll();
            StartCoroutine(Pause());

            //RespawnGeneration();
            //ReleaseConstraints();

            //time = 0;

            print(generation++);
            

        }

        time++;
    }

    IEnumerator Pause()
    {
        enabled = false;    //turn off update function
        yield return new WaitForSeconds(1f);  //pause
        enabled = true;     //turn on update function


        RespawnGeneration();
        ReleaseConstraints();

        time = 0;
    }

    void SleepAll()
    {
        for (int i = 0; i < numberOfCreatures; i++)
            creatures[i].awake = false;
    }

    bool AllCrashed()
    {
        for(int i = 0; i < numberOfCreatures; i++)
        {
            if (creatures[i].awake) return false;
        }
        return true;
    }

    void ReleaseConstraints()
    {
        for (int i = 0; i < numberOfCreatures; i++)
            creatures[i].ReleaseConstraints();
    }

    void InitialiseCreatures()
    {
        for (int i = 0; i < numberOfCreatures; i++)
        {
            GameObject creatureCopy = Instantiate(Eve);

            CarController controllerCopy = creatureCopy.GetComponent<CarController>();

            string[] name_tmp = { "car", (i + 1).ToString() };
            name = string.Join("", name_tmp, 0, 2);
            controllerCopy.gameObject.name = name;

            creatures.Add(controllerCopy);
        }
    }

    void RespawnGeneration()
    {
        int j = 0;
        for (int i = 0; i < numberOfCreatures; i++)
        {
            creatures[i].Respawn();
        }
    }


    //void ApplyForces(CarController creature)
    //{
    //    Vector3 v1 = new Vector3(0, creature.NN.OutputLayer[0].value, 0);
    //    float engine = creature.NN.OutputLayer[1].value;

    //    //creature.GetComponent<Rigidbody>().AddRelativeForce(v1 * movementSpeed);
    //    creature.GetComponent<Rigidbody>().AddTorque(v1 * movementSpeed);
    //    creature.GetComponent<Rigidbody>().AddRelativeForce(new Vector3(0, 0, engine * movementSpeed));
    //}




    void NaturalSelection()
    {
        SetChampion();

        CalculateFitness();
        CalculateFitnessSum();

        CopyBrain(creatures[0].gameObject, Champion.gameObject);    //Champion is always reborn in next generation unchanged

        for (int i = 1; i < numberOfCreatures; i++)
        {
            GameObject parent = SelectParent();
            CopyBrain(creatures[i].gameObject, parent);
            Mutate(creatures[i]);
        }

    }


    void CalculateFitness()
    {
        for (int i = 0; i < numberOfCreatures; i++)
        {
            float DistanceToTarget = Vector3.Distance(creatures[i].transform.position, Target.transform.position);
            int time = creatures[i].time;
            if(!creatures[i].reachedTheGoal)
                creatures[i].fitnessScore = 10000.0f / (DistanceToTarget * DistanceToTarget * DistanceToTarget * time);
            else
                creatures[i].fitnessScore = 1000000.0f / time;
        }
    }

    void CalculateFitnessSum()
    {
        fitnessSum = 0;
        for (int i = 0; i < numberOfCreatures; i++)
        {
            fitnessSum += creatures[i].fitnessScore;
        }
    }


    void SetChampion()
    {
        float bestScore = Vector3.Distance(creatures[0].transform.position, Target.transform.position);
        Champion = creatures[0];

        for (int i = 1; i < numberOfCreatures; i++)
        {
            float DistToTarget = Vector3.Distance(creatures[i].transform.position, Target.transform.position);
            if (DistToTarget < bestScore)
            {
                bestScore = DistToTarget;
                Champion = creatures[i];
            }
        }
    }


    GameObject SelectParent()
    {
        float rand = Random.Range(0.0f, fitnessSum);
        float runningSum = 0;

        for (int i = 0; i < numberOfCreatures; i++)
        {
            runningSum += creatures[i].fitnessScore;
            if (runningSum >= rand)
            {
                return creatures[i].gameObject;
            }
        }

        return null;    //should never come to this
    }


    void CopyBrain(GameObject creature, GameObject parent)
    {
        List<Neuron> HiddenLayer = creature.GetComponent<CarController>().NN.HiddenLayer;
        int i = 0;
        foreach (Neuron neuron in HiddenLayer)
        {
            int j = 0;
            foreach (float weight in neuron.inputWeights)
            {
                HiddenLayer[i].inputWeights[j] = parent.GetComponent<CarController>().NN.HiddenLayer[i].inputWeights[j];
                j++;
            }
            HiddenLayer[i].bias = parent.GetComponent<CarController>().NN.HiddenLayer[i].bias;
            i++;
        }

        List<Neuron> OutputLayer = creature.GetComponent<CarController>().NN.OutputLayer;
        i = 0;
        foreach (Neuron neuron in OutputLayer)
        {
            int j = 0;
            foreach (float weight in neuron.inputWeights)
            {
                OutputLayer[i].inputWeights[j] = parent.GetComponent<CarController>().NN.OutputLayer[i].inputWeights[j];
                j++;
            }
            OutputLayer[i].bias = parent.GetComponent<CarController>().NN.OutputLayer[i].bias;
            i++;
        }

    }


    void Mutate(CarController controller)
    {
        List<Neuron> HiddenLayer = controller.NN.HiddenLayer;
        for (int i = 0; i < HiddenLayer.Count; i++)
        {
            for (int j = 0; j < HiddenLayer[i].inputWeights.Count; j++)
            {
                float rand = Random.Range(0.0f, 1.0f);
                if (rand < mutationRate)
                {
                    HiddenLayer[i].inputWeights[j] = Random.Range(-1.0f, 1.0f);
                }
            }
        }


        List<Neuron> OutputLayer = controller.NN.OutputLayer;
        for (int i = 0; i < OutputLayer.Count; i++)
        {
            for (int j = 0; j < OutputLayer[i].inputWeights.Count; j++)
            {
                float rand = Random.Range(0.0f, 1.0f);
                if (rand < mutationRate)
                {
                    OutputLayer[i].inputWeights[j] = Random.Range(-1.0f, 1.0f);
                }
            }
        }
    }

}
