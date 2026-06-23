import pytest
import requests
import responses

LANGFLOW_API_URL = "http://127.0.0.1:7860/api/v1/run/2223d653-c81f-44cd-9d94-f01dfffe6b5d"
DLQ_MOCK_API = "http://127.0.0.1:3000/dlq/messages"


def run_agent(input_text):
    try:
        response = requests.post(
            LANGFLOW_API_URL,
            json={"input_value": input_text},
            timeout=15
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@responses.activate
def test_api_failure_routes_to_dlq():

    # Allow local Langflow server
    responses.add_passthru("http://127.0.0.1:7860")

    # Simulate Wikipedia failure
    responses.add(
        responses.GET,
        "https://en.wikipedia.org/w/api.php",
        status=503
    )

    responses.add(
        responses.GET,
        "https://www.wikipedia.org/",
        status=503
    )

    # Mock DLQ response
    responses.add(
        responses.GET,
        DLQ_MOCK_API,
        json=[{
            "original_prompt": "Where Morocco is located?",
            "status": "FAILED_ROUTED_TO_DLQ"
        }],
        status=200
    )

    run_agent("Where Morocco is located?")

    dlq_check = requests.get(DLQ_MOCK_API).json()

    assert len(dlq_check) > 0
    assert "Morocco" in dlq_check[0]["original_prompt"]
    assert dlq_check[0]["status"] == "FAILED_ROUTED_TO_DLQ"