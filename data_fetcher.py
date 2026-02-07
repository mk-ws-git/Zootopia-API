import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_data(animal_name):
  """
  Fetches the animals data for the animal 'animal_name'.
  Returns: a list of animals, each animal is a dictionary:
  {
    'name': ...,
    'taxonomy': {
      ...
    },
    'locations': [
      ...
    ],
    'characteristics': {
      ...
    }
  },
  """
  API_URL = "https://api.api-ninjas.com/v1/animals"
  API_KEY = os.getenv('API_KEY')

  if not API_KEY:
      raise RuntimeError("API_KEY is not set")

  response = requests.get(
      API_URL,
      params={"name": animal_name},
      headers={"X-Api-Key": API_KEY},
      timeout=20,
  )

  print("Status code:", response.status_code)
  response.raise_for_status()

  data = response.json()

  if isinstance(data, list):
      return data
  return []
