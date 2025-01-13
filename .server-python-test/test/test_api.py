import unittest
import os
from unittest.mock import patch
from server.app.api import generate_content, configure_api_key, get_available_models

class TestAPI(unittest.TestCase):

    @patch('server.app.api.genai.GenerativeModel')
    def test_generate_content(self, mock_model):
        mock_response = mock_model.return_value.generate_content.return_value
        mock_response.text = 'This is a response'
        
        response = generate_content('Who are you?')
        
        assert response == 'This is a response'
        
    def test_configure_api_key(self):
        api_key = "my_api_key"
        
        configure_api_key(api_key)
        
        self.assertEqual(os.environ["GOOGLE_API_KEY"], api_key)

    @patch('genai.list_models')
    def test_get_available_models(self, mock_list_models):
        mock_list_models.return_value = ['model1', 'model2', 'model3']
        
        result = get_available_models()
        
        self.assertEqual(result, ['model1', 'model2', 'model3'])
        mock_list_models.assert_called_once()


if __name__ == '__main__':
    unittest.main()