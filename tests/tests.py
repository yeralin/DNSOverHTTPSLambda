import sys
import json
from os import path
from unittest import TestCase

# Hack to access assets
sys.path.append('../assets/doh-lambda')
from doh import lambda_handler

TEST_DATA_GET_PAYLOAD_PATH = path.join(path.dirname(__file__), 'get-request.json')
TEST_DATA_POST_PAYLOAD_PATH = path.join(path.dirname(__file__), 'post-request.json')


class DOHTests(TestCase):

    def setUp(self) -> None:
        with open(TEST_DATA_GET_PAYLOAD_PATH) as f:
            self.get_request_payload = json.load(f)
        with open(TEST_DATA_POST_PAYLOAD_PATH) as f:
            self.post_request_payload = json.load(f)

    def test_get_request(self):
        response = lambda_handler(self.get_request_payload, None)
        self.assertEqual(200, response['statusCode'])
        self.assertIsNotNone(response['body'])

    def test_post_request(self):
        response = lambda_handler(self.post_request_payload, None)
        self.assertEqual(200, response['statusCode'])
        self.assertIsNotNone(response['body'])
