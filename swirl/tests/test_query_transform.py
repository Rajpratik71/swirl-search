import os
import json
from swirl.serializers import SearchProviderSerializer
from django.conf import settings
import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from swirl.bs4 import bs
import requests

## General and shared

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_suser_pw():
    return 'password'

@pytest.fixture
def test_suser(test_suser_pw):
    """
    return the user if it's aleady there, otherwise create it.
    """
    try:
        return User.objects.get(username='admin')
    except ObjectDoesNotExist:
        pass

    return User.objects.create_user(
        username='admin',
        password=test_suser_pw,
        is_staff=True,  # Set to True if your view requires a staff user
        is_superuser=True,  # Set to True if your view requires a superuser
    )

@pytest.fixture
def search_provider_pre_query_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the absolute file path for the JSON file in the 'data' subdirectory
    json_file_path = os.path.join(script_dir, 'data', 'sp_web_google_pse.json')

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

@pytest.fixture
def search_provider_query_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the absolute file path for the JSON file in the 'data' subdirectory
    json_file_path = os.path.join(script_dir, 'data', 'sp_web_google_pse_with_qrx_processor.json')

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

@pytest.fixture
def search_provider_open_search_query_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the absolute file path for the JSON file in the 'data' subdirectory
    json_file_path = os.path.join(script_dir, 'data', 'open_search_provider.json')

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

@pytest.fixture
def search_provider_ds_266_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the absolute file path for the JSON file in the 'data' subdirectory
    json_file_path = os.path.join(script_dir, 'data', 'sp_DS-266.json')

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data


@pytest.fixture
def search_provider_ds_265_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the absolute file path for the JSON file in the 'data' subdirectory
    json_file_path = os.path.join(script_dir, 'data', 'sp_DS-265.json')

    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data


@pytest.fixture
def qrx_synonym_search_test():
    return {
        "name": "test one",
        "shared": True,
        "qrx_type": "synonym",
        "config_content": "# column1, column2\nnotebook, laptop\nlaptop, personal computer\npc, personal computer\npersonal computer, pc"
}

@pytest.fixture
def mock_result():
    return {
    "items": [
    {
      "kind": "customsearch#result",
      "title": "Notebook | Financial Times",
      "htmlTitle": "\u003cb\u003eNotebook\u003c/b\u003e | Financial Times",
      "link": "https://www.ft.com/content/b6f32818-aeda-11da-b04a-0000779e2340",
      "displayLink": "www.ft.com",
      "snippet": "Mar 8, 2006 ... We'll send you a myFT Daily Digest email rounding up the latest MG Rover Group Ltd news every morning. Patricia Hewitt once confided to Notebook ...",
      "htmlSnippet": "Mar 8, 2006 \u003cb\u003e...\u003c/b\u003e We&#39;ll send you a myFT Daily Digest email rounding up the latest MG Rover Group Ltd news every morning. Patricia Hewitt once confided to \u003cb\u003eNotebook\u003c/b\u003e&nbsp;...",
      "formattedUrl": "https://www.ft.com/content/b6f32818-aeda-11da-b04a-0000779e2340",
      "htmlFormattedUrl": "https://www.ft.com/content/b6f32818-aeda-11da-b04a-0000779e2340",
      "pagemap": {
        "cse_thumbnail": [
          {
            "src": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSr8n8mzhsf6uFZw3uY-3pizLTj1JFydMfMwCQ3e_GZTxjRnHSAXg5apLU",
            "width": "310",
            "height": "163"
          }
        ],
      }
    }
  ]
}

class SearchQueryTransformTestCase(TestCase):
    @pytest.fixture(autouse=True)
    def _init_fixtures(self, api_client,test_suser, test_suser_pw, search_provider_pre_query_data, search_provider_query_data, search_provider_open_search_query_data,
                       search_provider_ds_266_data, search_provider_ds_265_data, qrx_synonym_search_test, mock_result):
        self._api_client = api_client
        self._test_suser = test_suser
        self._test_suser_pw = test_suser_pw
        self._search_provider_pre_query = search_provider_pre_query_data
        self._search_provider_query = search_provider_query_data
        self._search_provider_open_search_query_data = search_provider_open_search_query_data
        self._search_provider_ds_266 = search_provider_ds_266_data
        self._search_provider_ds_265 = search_provider_ds_265_data
        self._qrx_synonym = qrx_synonym_search_test
        self._mock_result = mock_result

    def setUp(self):
        settings.SWIRL_TIMEOUT = 1
        settings.CELERY_TASK_ALWAYS_EAGER = True
        is_logged_in = self._api_client.login(username=self._test_suser.username, password=self._test_suser_pw)
        # Check if the login was successful
        assert is_logged_in, 'Client login failed'

        # Create a search provider
        #1
        serializer = SearchProviderSerializer(data=self._search_provider_ds_265)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self._test_suser)

    def tearDown(self):
        settings.SWIRL_TIMEOUT = 10
        settings.CELERY_TASK_ALWAYS_EAGER = False

    def get_data(self, url):
        response = requests.get(url)
        return response.json()

    def test_pre_query_transform_processor(self):
        # Call the viewset
        surl = reverse('search')
        response = self._api_client.get(surl, {'q': 'confluence:"team space"', 'providers':1})
        print(response)



################################################################################
## individual cases

## Test fixtures
@pytest.fixture
def qrx_record_1():
    return {
        "name": "xxx",
        "shared": True,
        "qrx_type": "rewrite",
        "config_content": "# This is a test\n# column1, colum2\nmobiles; ombile; mo bile, mobile\ncheapest smartphones, cheap smartphone"
}

@pytest.fixture
def qrx_synonym():
    return {
        "name": "synonym 1",
        "shared": True,
        "qrx_type": "synonym",
        "config_content": "# column1, column2\nnotebook, laptop\nlaptop, personal computer\npc, personal computer\npersonal computer, pc"
}

@pytest.fixture
def qrx_synonym_bag():
    return {
        "name": "bag 1",
        "shared": True,
        "qrx_type": "bag",
        "config_content": "# column1....columnN\nnotebook, personal computer, laptop, pc\ncar,automobile, ride"
}
@pytest.fixture
def qrx_rewrite():
    return {
        "name": "rewrite 1",
        "shared": True,
        "qrx_type": "rewrite",
        "config_content": "# This is a test\n# column1, colum2\nmobiles; ombile; mo bile, mobile\ncheapest smartphones, cheap smartphone\non"
}
@pytest.fixture
def noop_query_string():
    return "noop"
######################################################################

@pytest.fixture
def qrx_rewrite_process():
    return {
        "name": "rewrite 1",
        "shared": True,
        "qrx_type": "rewrite",
        "config_content":
        """
# This is a test
# column1, colum2
mobiles; ombile; mo bile, mobile
computers, computer
cheap.* smartphones, cheap smartphone
on
"""
}
@pytest.fixture
def qrx_rewrite_test_queries():
    return ['mobile phone', 'mobiles','ombile', 'mo bile', 'on computing', 'cheaper smartphones','computers, go figure']

@pytest.fixture
def qrx_rewrite_expected_queries():
    return ['mobile phone', 'mobile','mobile', 'mobile', 'computing', 'cheap smartphone','computer go figure']

######################################################################
@pytest.fixture
def qrx_synonym_test_queries():
    return [
        '',
        'a',
        'robot human',
        'notebook',
        'pc',
        'personal computer',
        'I love my notebook',
        'This pc, it is better than a notebook',
        'My favorite song is "You got a fast car"'
        ]

@pytest.fixture
def qrx_synonym_expected_queries():
    return [
        '',
        'a',
        'robot human',
        '(notebook OR laptop)',
        '(pc OR personal computer)',
        '(personal computer OR pc)',
        'I love my (notebook OR laptop)',
        'This (pc OR personal computer) , it is better than a (notebook OR laptop)',
        'My favorite song is " You got a fast (car OR ride) "'
        ]

@pytest.fixture
def qrx_synonym_process():
    return {
        "name": "synonym 1",
        "shared": True,
        "qrx_type": "synonym",
        "config_content":
        """
# column1, column2
notebook, laptop
laptop, personal computer
pc, personal computer
personal computer, pc
car, ride
"""
}


@pytest.fixture
def qrx_synonym_bag_process():
    return {
        "name": "bag 1",
        "shared": True,
        "qrx_type": "bag",
        "config_content": """
# column1....columnN
notebook, personal computer, laptop, pc
car,automobile, ride
"""
}
######################################################################
@pytest.fixture
def qrx_synonym_bag_test_queries():
    return [
        '',
        'a',
        'machine human',
        'car',
        'automobile',
        'ride',
        'pimp my ride',
        'automobile, yours is fast',
        'I love the movie The Notebook',
        'My new notebook is slow'
        ]

@pytest.fixture
def qrx_synonym_bag_expected_queries():
    return [
        '',
        'a',
        'machine human',
        '(car OR automobile OR ride)',
        '(automobile OR car OR ride)',
        '(ride OR car OR automobile)',
        'pimp my (ride OR car OR automobile)',
        '(automobile OR car OR ride) , yours is fast',
        'I love the movie The Notebook',
        'My new (notebook OR personal computer OR laptop OR pc) is slow'
        ]
