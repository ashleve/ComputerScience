using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Neuron
{
    public float value;
    public float bias; 
    public List<float> inputWeights;

    public Neuron()
    {
        inputWeights = new List<float>();
        bias = GetRandom();
        value = 0;
    }

    public float GetRandom()
    {
        return Random.Range(-1.0f, 1.0f);
    }

    public void SetRandomWeights(List<Neuron> Layer)
    {
        inputWeights.Clear();
        foreach(Neuron neuron in Layer)
        {
            inputWeights.Add(GetRandom());
        }
    }

    public void CalculateValue(List<Neuron> Layer)
    {
        value = 0;
        int i = 0;
        foreach(float weight in inputWeights)
        {
            value += weight * Layer[i].value;
            i++;
        }
        value += bias;
        //ActivationFunction();
    }

    public void ActivationFunction()
    {
        value = 1 / (1 + Mathf.Exp(-value));
    }
}


public class NeuralNet
{
    public List<Neuron> InputLayer;
    public List<Neuron> HiddenLayer;
    public List<Neuron> OutputLayer;

    public NeuralNet(int inputSize = 8, int hiddenSize = 12, int outputSize = 6)
    {
        InputLayer = new List<Neuron>();
        HiddenLayer = new List<Neuron>();
        OutputLayer = new List<Neuron>();

        for (int i = 0; i < inputSize; i++)
        {
            InputLayer.Add(new Neuron());
        }

        for (int i = 0; i < hiddenSize; i++)
        {
            HiddenLayer.Add(new Neuron());
            HiddenLayer[i].SetRandomWeights(InputLayer);
        }

        for (int i = 0; i < outputSize; i++)
        {
            OutputLayer.Add(new Neuron());
            OutputLayer[i].SetRandomWeights(HiddenLayer);
        }
    }

    public void ForwardPropagate(params float[] inputs)
    {
        int i = 0;
        InputLayer.ForEach(a => a.value = inputs[i++]);
        HiddenLayer.ForEach(a => a.CalculateValue(InputLayer));
        OutputLayer.ForEach(a => a.CalculateValue(HiddenLayer));
    }

}
