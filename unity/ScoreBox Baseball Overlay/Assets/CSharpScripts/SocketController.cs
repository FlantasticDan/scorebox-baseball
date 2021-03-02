using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using WebSocketSharp;
using Newtonsoft.Json;

public class SocketController : MonoBehaviour
{
    public Dictionary<string, string> gameState = new Dictionary<string, string>();

    // Start is called before the first frame update
    void Start()
    {
        Application.runInBackground = true;

        GenerateInitialGameState();

        var ws = new WebSocket ("ws://127.0.0.1:5500");

        ws.OnOpen += (sender, e) => {
            Debug.Log("Socket Connection Opened");
        };

        ws.OnMessage += (sender, e) => {
            Dictionary<string, string> payload = JsonConvert.DeserializeObject<Dictionary<string, string>>(e.Data);

            if (payload["mode"] == "game_state") {
                ProcessGameState(payload);
            }
        };

        ws.Connect ();

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void GenerateInitialGameState()
    {
        gameState.Add("home_team", "Home");
        gameState.Add("home_color", "red");
        gameState.Add("home_score", "0");
        gameState.Add("visitor_team", "Away");
        gameState.Add("visitor_color", "blue");
        gameState.Add("visitor_score", "0");
        gameState.Add("inning", "1");
        gameState.Add("inning_mode", "");
        gameState.Add("inning_status", "");
        gameState.Add("base_1", "False");
        gameState.Add("base_2", "False");
        gameState.Add("base_3", "False");
        gameState.Add("strikes", "0");
        gameState.Add("balls", "0");
        gameState.Add("outs", "0");
    }

    void ProcessGameState(Dictionary<string, string> payload)
    {
        gameState["home_team"] = payload["home_team"];
        gameState["home_color"] = payload["home_color"];
        gameState["home_score"] = payload["home_score"];
        gameState["visitor_team"] = payload["visitor_team"];
        gameState["visitor_color"] = payload["visitor_color"];
        gameState["visitor_score"] = payload["visitor_score"];
        gameState["inning"] = payload["inning"];
        gameState["inning_mode"] = payload["inning_mode"];
        gameState["inning_status"] = payload["inning_status"];
        gameState["base_1"] = payload["base_1"];
        gameState["base_2"] = payload["base_2"];
        gameState["base_3"] = payload["base_3"];
        gameState["strikes"] = payload["strikes"];
        gameState["balls"] = payload["balls"];
        gameState["outs"] = payload["outs"];
    }    
}
