import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs,  auth=HTTPBasicAuth('apikey', 'l5o8giI2DQiT8mWCBpL_caR7H9yfkkmx6ESOUFTTPzI4'))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    print(json_data)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer['doc']
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)

    if json_result:
        dealers = json_result['data']['docs']
        print(dealers)
        for dealer in dealers:
            dealer_doc = dealer
   
            dealer_obj = DealerReview(
                dealership=dealer_doc["dealership"], 
                name=dealer_doc["name"],
                id=dealer_doc["id"], 
                purchase=dealer_doc["purchase"], 
                review=dealer_doc["review"],
                car_make = dealer_doc["car_make"],
                car_model = dealer_doc["car_model"],
                car_year = dealer_doc["car_year"],
                sentiment=''
                
            )
            sentiment=analyze_review_sentiments(dealer_obj.review)
            print(sentiment)
            dealer_obj.sentiment = sentiment
            results.append(dealer_obj)
    return results


def analyze_review_sentiments(text):
    
    url = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/b4e48f9a-83d4-459e-9fa8-633d5c7b1abf/'
    authenticator = IAMAuthenticator('l5o8giI2DQiT8mWCBpL_caR7H9yfkkmx6ESOUFTTPzI4')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2023-06-12',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    features = 'sentiment'
    return_analyzed_text = False
    language= "en"
    response = natural_language_understanding.analyze(
        text=text,
        language= language,
        features=Features(sentiment=SentimentOptions())).get_result()
        
    
    sentiment=response['sentiment']['document']['label'] 
    return sentiment
