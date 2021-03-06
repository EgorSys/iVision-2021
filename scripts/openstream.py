from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import requests

def process_browser_log_entry(entry):
	response = json.loads(entry['message'])['message']
	return response

class camera():
	def __init__(self, address):
		self.caps = DesiredCapabilities.CHROME
		self.caps['goog:loggingPrefs'] = {'performance': 'ALL'}
		self.options = webdriver.ChromeOptions()
		self.options.add_argument("--window-size=1920,1080")

		self.driver = webdriver.Chrome(desired_capabilities=self.caps,options=self.options)
		self.driver.get(address) # button is //*[@id="camera"]/button

	def stream(name):
		start = self.driver.find_elements_by_xpath('//*[@id="camera"]/button')[0]
		start.click()
		while True:
			browser_log = self.driver.get_log('performance')
			events = [process_browser_log_entry(entry) for entry in browser_log]
			events = [event for event in events if 'Network.response' in event['method']]

			for e in events:
				if 'response' in e['params']:
					if e['params']['response']['url'].endswith('.ts'):
						url=e['params']['response']['url']
						r1 = requests.get(url, stream=True)
						if(r1.status_code == 200):
							with open(name+'_stream.mpeg','wb') as f:
								for chunk in r1.iter_content(chunk_size=1024):
									f.write(chunk)