import io
import json
import oci
from fdk import response

def trigger_sync(signer):
    try:
        generative_ai_client = oci.generative_ai.GenerativeAiClient(config={}, signer=signer)
        create_vector_store_connector_file_sync_response = generative_ai_client.create_vector_store_connector_file_sync(
            create_vector_store_connector_file_sync_details=oci.generative_ai.models.CreateVectorStoreConnectorFileSyncDetails(
                vector_store_connector_id="ocid1.generativeaivectorconnector.oc1.phx.abc")
                )
    except Exception as ex:
        print("ERROR: problem with trigger_sync", ex, flush=True)
        raise

    return {"response": str(create_vector_store_connector_file_sync_response.data)}
                                                                                                            
def handler(ctx, data: io.BytesIO = None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = trigger_sync(signer) 
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
