import io
import json
import oci
from fdk import response

def list_objects(signer):
    bucketName = "voice_uploads"
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    namespace = client.get_namespace().data
    object = client.list_objects(namespace, bucketName)
    print("found objects", flush=True)
    objects = [b.name for b in object.data.objects]
    print(f"Objects found in bucket + {bucketName} : {objects}", flush=True)
    return objects

def trigger_transcription(signer, object_list):
    try:
        ai_speech_client = oci.ai_speech.AIServiceSpeechClient(config={}, signer=signer)
        response_create_transcription_job = ai_speech_client.create_transcription_job(
            create_transcription_job_details=oci.ai_speech.models.CreateTranscriptionJobDetails(
                compartment_id="ABC",
                input_location=oci.ai_speech.models.ObjectListInlineInputLocation(
                    object_locations=[
                        oci.ai_speech.models.ObjectLocation(
                            bucket_name="voice_uploads",
                            namespace_name="ABC",
                            object_names= object_list,
                        )
                    ],
                ),
                output_location=oci.ai_speech.models.OutputLocation(
                    bucket_name="voice_transcripts",
                    namespace_name="ABC",
                    prefix="",
                ),
            )
        )
        
    except Exception as ex:
        print("ERROR: problem with trigger_transcription", ex, flush=True)
        raise

    return {"response": str(response_create_transcription_job.data)}
                                                                                                            
def handler(ctx, data: io.BytesIO = None):
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = trigger_transcription(signer, list_objects(signer)) 
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )
