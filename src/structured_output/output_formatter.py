import json

class OutputFormatter:
    def __init__(self):
        pass

    def format(self, structured_response, search_results=None, debug_data=None, retrieved_docs=None):
        return {
            "status": "success",
            "data": {
                "subtasks": structured_response.get("subtasks", []),
                "code": self._generate_code(structured_response, retrieved_docs),
                "gotchas": structured_response.get("gotchas", []),
                "best_practices": structured_response.get("best_practices", []),
                "difficulty": structured_response.get("difficulty", "Unknown"),
                "docs_link": structured_response.get("docs_link", ""),
                "raw": structured_response.get("raw", {}),
                "search_results": search_results,
                "retrieved_docs": retrieved_docs or [],
                "debug": debug_data or {}
            }
        }

    def _generate_code(self, structured_response, retrieved_docs):
        """
        Generate real code snippets:
        - Try to extract from retrieved docs.
        - If not found, fall back to context-aware templates.
        """
        # 1️⃣ Use retrieved_docs if they contain C#/C++/Blueprint snippets
        if retrieved_docs:
            for doc in retrieved_docs:
                if "public class" in doc or "foreach" in doc or "Blueprint" in doc:
                    # Extract first ~20 lines
                    snippet = "\n".join(doc.splitlines()[:20])
                    return snippet

        # 2️⃣ Otherwise infer from query
        raw_field = structured_response.get("raw", "")
        query_text = (
            json.dumps(raw_field).lower()
            if isinstance(raw_field, dict)
            else str(raw_field).lower()
        )

        if "teleport" in query_text and "unity" in query_text:
            return """using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class TeleportSetup : MonoBehaviour
{
    public XRInteractionManager interactionManager;
    public TeleportationProvider teleportationProvider;

    void Start()
    {
        if (teleportationProvider == null)
        {
            teleportationProvider = FindObjectOfType<TeleportationProvider>();
        }
    }

    public void SetupTeleportArea(GameObject floor)
    {
        var area = floor.AddComponent<TeleportationArea>();
        area.teleportationProvider = teleportationProvider;
    }
}"""

        if "snap turn" in query_text and "unity" in query_text:
            return """using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class SnapTurnSetup : MonoBehaviour
{
    public ActionBasedSnapTurnProvider snapTurnProvider;

    void Start()
    {
        if (snapTurnProvider == null)
        {
            snapTurnProvider = FindObjectOfType<ActionBasedSnapTurnProvider>();
        }
        snapTurnProvider.turnAmount = 45f; // degrees per snap
    }
}"""

        if "unreal" in query_text and "teleport" in query_text:
            return """// Unreal Engine Blueprint pseudocode:
// 1. Add NavMeshBoundsVolume in level
// 2. Enable 'Teleport' in MotionControllerPawn
// 3. Bind controller input to 'TeleportAction'
// 4. Use 'Teleport To' node with destination from Trace"""

        # Default
        return "// Example code snippet"
