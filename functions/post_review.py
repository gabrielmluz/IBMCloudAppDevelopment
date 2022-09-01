import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    authenticator = IAMAuthenticator("Vfq3l4o7uhbV3b3zlyK5LWXUB3l3mCTy9vD1O-Vy7ggP")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://fea68551-8177-4d1d-b80b-a3f653e2e8f4-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
    try:
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }