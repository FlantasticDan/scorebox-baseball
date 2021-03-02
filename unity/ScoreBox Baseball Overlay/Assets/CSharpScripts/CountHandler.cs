using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class CountHandler : MonoBehaviour
{
    public SocketController socket;
    private Dictionary<string, string> gameState;
    public TextMeshProUGUI outs;
    public TextMeshProUGUI outsLabel;
    public TextMeshProUGUI count;
    // Start is called before the first frame update
    void Start()
    {
        gameState = socket.gameState;   
    }

    // Update is called once per frame
    void Update()
    {
        outs.text = gameState["outs"];
        if (gameState["outs"] == "1") {
            outsLabel.text = "out";
        }
        else {
            outsLabel.text = "outs";
        }

        if (gameState["strikes"] == "0" && gameState["balls"] == "0") {
            count.gameObject.SetActive(false);
        }
        else {
            count.text = gameState["balls"] + " - " + gameState["strikes"];
            count.gameObject.SetActive(true);
        }
    }
}
