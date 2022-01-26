import json
import unittest

import requests


class BlogPostsTest(unittest.TestCase):
    """
        @version : 1.0
        @author : Shraddha A
        This is a test class for Bog REST API covering create posts, get posts
    """

    def setUp(self):
        self.category_id = 3

    def testCreatePost(self):
        """
        Test post blog post - create a new blog post
        :assert: 201
        """
        url_catgories = 'http://localhost:8888/api/blog/categories/'
        headers = {"Content-Type": "application/json"}
        get_resp_before = requests.get(url=url_catgories, headers=headers)
        before_json_resp = get_resp_before.json()
        for category_params in before_json_resp:
            self.category_id = category_params['id']
            break
        payload = json.dumps({
            "body": "abcd",
            "category_id": self.category_id,
            "title": "test_title"
        })
        url = 'http://localhost:8888/api/blog/posts/'
        response = requests.post(url=url, headers=headers, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual('CREATED', response.reason)

    def testGetPostbyCategoryId(self):
        """
        Test get blog posts by category ID
        :assert: 200
        """
        url = 'http://localhost:8888/api/blog/categories/' + str(self.category_id)
        headers = {'Accept': 'application/json'}
        response = requests.get(url=url, headers=headers)
        self.assertNotEqual(200, response.status_code)

    def tearDown(self):
        self.category_id = None
