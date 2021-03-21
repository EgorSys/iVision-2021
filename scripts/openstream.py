from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import requests

def process_browser_log_entry(entry):
	response = json.loads(entry['message'])['message']
	return response

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(desired_capabilities=caps,options=options)
# button is //*[@id="camera"]/button
driver.get('https://moidom.citylink.pro/pub/10491')

start = driver.find_elements_by_xpath('//*[@id="camera"]/button')[0]
start.click()
time.sleep(5)
stt = time.time()
elap = 0
while elap<10:
	browser_log = driver.get_log('performance')
	events = [process_browser_log_entry(entry) for entry in browser_log]
	events = [event for event in events if 'Network.response' in event['method']]

	for e in events:
		if 'response' in e['params']:
			if e['params']['response']['url'].endswith('.ts'):
				url=e['params']['response']['url']
				r1 = requests.get(url, stream=True)
				if(r1.status_code == 200):
					with open('Lenintest.mpeg','ab') as f:
						for chunk in r1.iter_content(chunk_size=1024):
							f.write(chunk)
				else:
					print("Received unexpected status code {}".format(r1.status_code))
	elap = time.time() - stt