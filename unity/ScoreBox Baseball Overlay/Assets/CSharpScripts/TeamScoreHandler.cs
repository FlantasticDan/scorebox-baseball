using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class TeamScoreHandler : MonoBehaviour
{
    public SocketController socket;
    private Dictionary<string, string> gameState;
    public string team;
    public TextMeshProUGUI teamName;
    public TextMeshProUGUI teamScore;
    public RawImage teamBG;
    public ColorManager colors;

    // Start is called before the first frame update
    void Start()
    {
        gameState = socket.gameState;
    }

    // Update is called once per frame
    void Update()
    {
        teamName.text = gameState[team + "_team"];
        teamScore.text = gameState[team + "_score"];
        teamBG.color = colors.GetColor(gameState[team + "_color"]);
    }
}
