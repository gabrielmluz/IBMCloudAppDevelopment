const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

const DB_NAME='reviews';

async function main(params) {
   try {

   const authenticator = new IamAuthenticator({apikey: "Vfq3l4o7uhbV3b3zlyK5LWXUB3l3mCTy9vD1O-Vy7ggP"});
    const cloudant = CloudantV1.newInstance({authenticator: authenticator});
    cloudant.setServiceUrl("https://fea68551-8177-4d1d-b80b-a3f653e2e8f4-bluemix.cloudantnosqldb.appdomain.cloud");
   
   var dealerId=parseInt(params.id);

        let dbList = await cloudant.postFind({
            db: DB_NAME,
            selector:{"dealership":dealerId}
        });
        return  dbList.result;

    } catch (error) {
        return {
            error: error.description
        };
    }
}