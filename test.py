# test.py
import unittest
import requests
import json

from invest import MAX_DATA_POINTS

class TestETFInvestmentSimulatorBackend(unittest.TestCase):
    BASE_URL = 'http://127.0.0.1:5000'

    def test_simulate_endpoint_success(self):
        url = f"{self.BASE_URL}/simulate"
        payload = {
            "etf_symbol": "SPY",
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "starting_principal": 10000,
            "auto_invest_amount": 100,
            "investment_interval": "Monday",
            "frequency": "weekly"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('profit', data)
        self.assertIn('plot_data', data)
        self.assertIn('dates', data['plot_data'])
        self.assertIn('profit_percentages', data['plot_data'])
        self.assertTrue(len(data['plot_data']['dates']) <= MAX_DATA_POINTS)

    def test_simulate_endpoint_missing_params(self):
        url = f"{self.BASE_URL}/simulate"
        payload = {
            "etf_symbol": "SPY",
            # Missing other required parameters
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('error', data)

    def test_simulate_endpoint_invalid_frequency(self):
        url = f"{self.BASE_URL}/simulate"
        payload = {
            "etf_symbol": "SPY",
            "start_date": "2020-01-01",
            "end_date": "2021-01-01",
            "starting_principal": 10000,
            "auto_invest_amount": 100,
            "investment_interval": "Monday",
            "frequency": "yearly"  # Invalid frequency
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn('error', data)
    
    def test_set_base_endpoint_success(self):
        url = f"{self.BASE_URL}/set_base"
        payload = {
            "new_base_params": {
                "etf_symbol": "DIA",
                "start_date": "2019-01-01",
                "end_date": "2020-01-01",
                "starting_principal": 5000,
                "auto_invest_amount": 50,
                "investment_interval": "Tuesday",
                "frequency": "monthly"
            }
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Base parameters updated.')

if __name__ == '__main__':
    unittest.main()