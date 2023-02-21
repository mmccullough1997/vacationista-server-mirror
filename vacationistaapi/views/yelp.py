import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
load_dotenv()

class YelpAPIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
      location = kwargs.get('param')
      yelp_token = os.environ.get('YELP_API_TOKEN')
      headers = {
          "Authorization": f"Bearer {yelp_token}"
      }
      url = "https://api.yelp.com/v3/businesses/search"
      params = {
          "location": location,
          "limit": 20,
          "sort_by": "distance",
      }
      response = requests.get(url, headers=headers, params=params)
      data = response.json()
      return Response(data)
