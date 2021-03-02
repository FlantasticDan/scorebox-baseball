using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ColorManager : MonoBehaviour
{
    public Color red;
    public Color orange;
    public Color yellow;
    public Color green;
    public Color blue;
    public Color purple;
    public Color gold;
    public Color silver;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public Color GetColor(string color)
    {
        if (color == "red")
        {
            return red;
        }

        if (color == "orange")
        {
            return orange;
        }

        if (color == "yellow")
        {
            return yellow;
        }

        if (color == "green")
        {
            return green;
        }

        if (color == "blue")
        {
            return blue;
        }

        if (color == "purple")
        {
            return purple;
        }

        if (color == "gold")
        {
            return gold;
        }

        if (color == "silver")
        {
            return silver;
        }

        return silver;
    }
}
