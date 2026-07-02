from openai import OpenAI
from oci_openai import OciInstancePrincipalAuth
import httpx

client = OpenAI(
    base_url="https://inference.generativeai.us-phoenix-1.oci.oraclecloud.com/openai/v1",  # update region if needed
    api_key="not-used",
    project="ocid1.generativeaiproject.oc1.phx.abc",  # project OCID created earlier
    http_client=httpx.Client(auth=OciInstancePrincipalAuth()),
)


def oci_gen_chat(entry):
    response = client.responses.create(
        model="xai.grok-4-1-fast-reasoning",
        input=entry,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": ["vs_phx_abc"]
            }
        ]
    )
    return response
