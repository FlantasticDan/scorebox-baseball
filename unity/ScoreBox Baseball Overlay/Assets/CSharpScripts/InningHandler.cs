using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class InningHandler : MonoBehaviour
{
    public SocketController socket;
    public TextMeshProUGUI inning;
    public Image topArrow;
    public Image botArrow;
    public GameObject atBatContainer;
    public TextMeshProUGUI inningStatus;
    private Dictionary<string, string> gameState;
    // Start is called before the first frame update
    void Start()
    {
        gameState = socket.gameState;
    }

    // Update is called once per frame
    void Update()
    {
        if (gameState["inning_mode"] == "top") {
            topArrow.gameObject.SetActive(true);
            botArrow.gameObject.SetActive(false);
            atBatContainer.SetActive(true);
        }
        else {
            topArrow.gameObject.SetActive(false);
            if (gameState["inning_mode"] == "bot") {
                botArrow.gameObject.SetActive(true);
                atBatContainer.SetActive(true);
            }
            else {
                botArrow.gameObject.SetActive(false);
                atBatContainer.SetActive(false);
            }
        }

        inning.text = gameState["inning"];
        inningStatus.text = gameState["inning_status"];
    }
}
