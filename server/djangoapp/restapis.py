import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions

# Make HTTP GET requests
def get_request(url, **kwargs):
    #print(kwargs)
    print("GET from {}".format(url))
    try:
        # Get the data from the API url
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occured")
    status_code = response.status_code
    print("With status {}".format(status_code))
    # Return the json_data
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Get dealer from cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Get the JSON result from the get_request function
    json_result = get_request(url)
    # If has any data
    if json_result:
        dealers = json_result["docs"]
        # Populate the dealer object
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            # Parse the JSON result to a CarDealer object list
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"], st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    # Return dealer data
    return results

# Get reviews by dealer id from a cloud function (id informed in the url path)
def get_dealer_reviews_from_cf(url, id):
    results = []
    # Get the JSON result from the get_request function
    # Filter by id
    json_result = get_request(url, **{"id":id})
    # If has any data
    if json_result:
        reviews = json_result["docs"]
        # Populate the review object
        for review in reviews:
            sentiment = analyze_review_sentiments(review['review'])
            # Verify if has a purchase and change the fields accordingly
            if review["purchase"]:
                # Parse the JSON result to a DealerReview object list
                review_obj = DealerReview(dealership=review["dealership"],name=review["name"],purchase=review["purchase"],
                                        id=review["id"],review=review["review"], sentiment=sentiment,
                                        **{
                                        "purchase_date":review["purchase_date"],
                                        "car_make":review["car_make"],
                                        "car_model":review["car_model"],
                                        "car_year":review["car_year"]}
                                        )
                results.append(review_obj)
            else:
                review_obj = DealerReview(dealership=review["dealership"],name=review["name"],purchase=review["purchase"],
                                        id=review["id"],review=review["review"], sentiment=sentiment)
                results.append(review_obj)
    # Return review data by the id informed in the url path
    return results
    

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/32393010-04a8-4e6f-a7da-6353072e4a33"
    api_key = "cnaTuwP6HOVe2N8pItDT69nAaqL4_NkaF05OSKXrJf50"
    authenticator = IAMAuthenticator(api_key)
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    
    response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
    
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    
    return(label)