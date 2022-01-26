import unittest
import json
import unittest
import requests


class BlogCategoriesTest(unittest.TestCase):

    def setUp(self):
        self.category_id = 4

    def testGetCategories(self):
        """
        Test get blog categories - list categories
        :assert: 201
        """
        url = 'http://localhost:8888/api/blog/categories/'
        headers = {'Accept': 'application/json'}
        response = requests.get(url=url, headers=headers)
        resp_array = [{'id': 1, 'name': 'Sci-Fi'}, {'id': 2, 'name': 'Politics'}, {'id': 3, 'name': 'Tech'}]
        self.assertEqual(200, response.status_code)

    def testGetCategoriesIncorrectUrl(self):
        """
        Test get blog categories for incorrect url
        :assert: 404
        """
        incorrect_url = 'http://localhost:8888/api/blog/categorie/'
        headers = {'Accept': 'application/json'}
        response = requests.get(url=incorrect_url, headers=headers)
        self.assertEqual(404, response.status_code)

    def testPostCategories(self):
        """
        Test post blog categories - create new category
        :assert: 201
        """
        new_category = "Entertainment"
        payload = json.dumps({
            "name": new_category
        })
        url = 'http://localhost:8888/api/blog/categories/'
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=url, headers=headers, data=payload)
        self.assertEqual(201, response.status_code)
        self.assertEqual('CREATED', response.reason)
        get_resp = requests.get(url=url, headers=headers)
        updated_json_resp = get_resp.json()
        new_category_flag = False
        for category_params in updated_json_resp:
            if category_params['name'] == new_category:
                new_category_flag = True
                break
        self.assertTrue(new_category_flag)

    def testPostCategoriesIncorrectParameter(self):
        """
        Test get blog post categories for incorrect parameters
        :assert: 404
        """
        url = 'http://localhost:8888/api/blog/categories/'
        headers = {"Content-Type": "application/json"}
        response = requests.post(url=url, headers=headers, data="")
        self.assertNotEqual(201, response.status_code)

    def testDeleteCategory(self):
        """
        Test delete blog category by category ID
        :assert: 204
        """
        url = 'http://localhost:8888/api/blog/categories/'
        headers = {"Content-Type": "application/json"}
        get_resp_before = requests.get(url=url, headers=headers)
        before_json_resp = get_resp_before.json()
        list_categories_before_deletion = []
        for category_params in before_json_resp:
            list_categories_before_deletion.append(category_params['id'])
        deleted_category_id = list_categories_before_deletion[0]
        updated_deletion_url = url + str(deleted_category_id)
        response = requests.delete(url=updated_deletion_url, headers=headers)
        self.assertEqual(204, response.status_code)
        get_resp_after = requests.get(url=url, headers=headers)
        after_json_resp = get_resp_after.json()
        list_categories_after_deletion = []
        for category_params in after_json_resp:
            list_categories_after_deletion.append(category_params['id'])
        self.assertNotEqual(len(list_categories_before_deletion), len(list_categories_after_deletion))
        self.assertEqual(len(list_categories_before_deletion) - 1, len(list_categories_after_deletion))

    def testDeleteCategoryNotFound(self):
        """
        Test delete blog category error with incorrect category ID
        :assert: 404
        """
        url = 'http://localhost:8888/api/blog/categories/999'
        headers = {"Content-Type": "application/json"}
        response = requests.delete(url=url, headers=headers)
        self.assertEqual(404, response.status_code)

    def testUpdateCategoryId(self):
        """
        Test update blog category by category ID
        :assert: 204
        """
        url = 'http://localhost:8888/api/blog/categories/'
        headers = {"Content-Type": "application/json"}
        get_resp_before = requests.get(url=url, headers=headers)
        before_json_resp = get_resp_before.json()
        for category_params in before_json_resp:
            self.category_id = category_params['id']
            break
        updated_category = "Updated Category"
        payload = json.dumps({
            "name": updated_category
        })
        url = url + str(self.category_id)
        headers = {"Content-Type": "application/json"}
        response = requests.put(url=url, headers=headers, data=payload)
        self.assertEqual(204, response.status_code)

    def testUpdateCategoryIdError(self):
        """
        Test update blog category error by incorrect category ID
        :assert: 404
        """
        updated_category = "Updated Category"
        payload = json.dumps({
            "name": updated_category
        })
        url = 'http://localhost:8888/api/blog/categories/' + str(0)
        headers = {"Content-Type": "application/json"}
        response = requests.put(url=url, headers=headers, data=payload)
        self.assertEqual(404, response.status_code)

    def tearDown(self):
        self.category_id = None
