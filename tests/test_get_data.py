import unittest
from unittest.mock import patch, MagicMock
import requests
from data import get_data

class TestTrainArrivalsErrorHandling(unittest.TestCase):
    
    @patch('data.get_data.requests.get')
    def test_timeout_retry(self, mock_get):
        """Test that Timeout is retried"""
        mock_get.side_effect = requests.Timeout("Connection timed out")
        
        result = get_data.call_get_train_arrivals(40470)
        
        # Should have been called max_retries times
        self.assertEqual(mock_get.call_count, get_data.max_retries)
        # Should return empty dict after retries exhausted
        self.assertEqual(result, {})
    
    @patch('data.get_data.requests.get')
    def test_500_error_retry(self, mock_get):
        """Test that 5xx errors are retried"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError(response=MagicMock(status_code=503))
        mock_get.return_value = mock_response
        
        result = get_data.call_get_train_arrivals(40470)
        
        self.assertEqual(mock_get.call_count, get_data.max_retries)
        self.assertEqual(result, {})
    
    @patch('data.get_data.requests.get')
    def test_400_error_no_retry(self, mock_get):
        """Test that 4xx errors don't retry"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError(response=MagicMock(status_code=401))
        mock_get.return_value = mock_response
        
        with self.assertRaises(requests.HTTPError):
            get_data.call_get_train_arrivals(40470)
        
        # Should only be called once (no retry)
        self.assertEqual(mock_get.call_count, 1)
    
    @patch('data.get_data.requests.get')
    def test_successful_response(self, mock_get):
        """Test successful response"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ctatt": {
                "eta": [
                    {"arrT": "2026-04-01T10:30:00", "destNm": "Downtown"},
                ]
            }
        }
        mock_get.return_value = mock_response
        
        result = get_data.call_get_train_arrivals(40470)
        
        self.assertIsNotNone(result)
        self.assertIn("ctatt", result)
        self.assertEqual(mock_get.call_count, 1)
    
    @patch('data.get_data.requests.get')
    def test_get_train_arrivals_returns_empty_df_on_error(self, mock_get):
        """Test that get_train_arrivals returns empty DataFrame on any error"""
        mock_get.side_effect = requests.Timeout()
        
        result = get_data.get_train_arrivals(40470)
        
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()
