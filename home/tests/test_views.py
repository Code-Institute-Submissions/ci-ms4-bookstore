from django.test import TestCase
import home.views

class TestViews(TestCase):

    def test_get_index(self): 
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')


"""
    def test_get_archive():

    def test_can_add_item():

    def test_can_delete_item():

    def test_can_edit_item():

"""