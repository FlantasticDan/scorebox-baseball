using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BaseHandler : MonoBehaviour
{
    public RawImage baseBG;
    public string baseNumber;
    public Color emptyBase;
    public Color occupiedBase;
    public SocketController socket;
    private Dictionary<string, string> gameState;
    // Start is called before the first frame update
    void Start()
    {
        gameState = socket.gameState;
    }

    // Update is called once per frame
    void Update()
    {
        bool state = bool.Parse(gameState["base_" + baseNumber]);
        if (state) {
            baseBG.color = occupiedBase;
        }
        else {
            baseBG.color = emptyBase;
        }
    }
}
