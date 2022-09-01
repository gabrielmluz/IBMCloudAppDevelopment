const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main() {
      const authenticator = new IamAuthenticator({ apikey: "Vfq3l4o7uhbV3b3zlyK5LWXUB3l3mCTy9vD1O-Vy7ggP" })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl("https://fea68551-8177-4d1d-b80b-a3f653e2e8f4-bluemix.cloudantnosqldb.appdomain.cloud");
     
      try {
        let docList = await cloudant.postAllDocs({
            db: 'dealerships',
            includeDocs: true
        });
        return { "docs": docList.result.rows };
        } catch (error) {
          return { error: error.description };
      }
}