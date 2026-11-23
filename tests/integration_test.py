import unittest
from app import app  # Import your Flask app instance


class TestModelAppIntegration(unittest.TestCase):

	def setUp(self):
		app.testing = True
		self.client = app.test_client()
		
	def test_model_app_integration(self):
		# Valid test input that should work with the trained model
		form_data = {
			'temperature': '275.15',   # Kelvin
			'pressure': '1013',        # hPa
			'humidity': '85',          # %
			'wind_speed': '3.6',       # m/s
			'wind_deg': '180',         # degrees
			'rain_1h': '0',            # mm
			'rain_3h': '0',            # mm
			'snow': '0',               # mm
			'clouds': '20'             # %
		}

		response = self.client.post('/', data=form_data)
	
		# Complete below
		# Ensure that the result page (response.data) should include a weather prediction
		self.assertEqual(response.status_code, 200)
		html = response.data.decode('utf-8').lower()
		
		#checking for weather prediction
		self.assertIn('the weather is:', html)
		
		#checking for prediction time 
		#this uses regex to check there is a valid numerical value in the html with ms at the end
		self.assertRegex(html, r'prediction time:</strong>\s*\d+(\.\d+)?\s*ms')

		html_text = response.data.decode('utf-8').lower()
		valid_classes = [
			'clear', 'cloudy', 'drizzly', 'foggy', 'hazey',
			'misty', 'rainy', 'smokey', 'thunderstorm'
		]
		found = any(weather in html_text for weather in valid_classes)
		
		# Ensure that classification is in valid classes, provide an error message if not.
		self.assertTrue(any(valid in html for valid in valid_classes), "Invalid weather classification")

if __name__ == '__main__':
	unittest.main()
