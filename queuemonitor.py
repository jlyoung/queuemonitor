"""Raise Notification Center messages when new cases arrive in SalesForce Incoming Queue."""

import logging
import pprint
import sys
import time
from urlparse import urljoin

import yaml
from pync import Notifier
from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)
queue_front_page = set()

def retry_if_stale_element_reference_exception(exception):
	"""Return whether the exception is a StaleElementReferenceException exception."""
	return isinstance(exception, StaleElementReferenceException)

def retry_if_element_not_visible_exception(exception):
	"""Return whether the exception is a ElementNotVisibleException exception."""
	return isinstance(exception, ElementNotVisibleException)

@retry(retry_on_exception=retry_if_stale_element_reference_exception)
def check_queue(driver):
	"""Reload the Incoming Queue page. Raise Notification Center message if there is a new case."""
	global queue_front_page
	time.sleep(10)
	driver.find_element_by_id("00BE0000001ELz7_refresh").click()
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "x-grid3-body")))
	rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "x-grid3-row")))
	pp = pprint.PrettyPrinter(indent=4)
	for row in rows:
		row_dict = {}
		case_number = row.find_element_by_class_name("x-grid3-col-CASES_CASE_NUMBER")
		row_dict["case_number"] = case_number.text
		case_url = row.find_element_by_tag_name("a").get_attribute("href")
		row_dict["case_url"] = urljoin(driver.current_url, case_url)
		row_dict["problem_statement"] = row.find_element_by_class_name("x-grid3-col-00NE0000002C0mc").text
		try:
			row_dict["severity"] = row.find_element_by_class_name("x-grid3-col-00NE0000002BvKo").text.split()[0]
		except:
			row_dict["severity"] = ""
		if row_dict["case_number"] not in queue_front_page:
			message = u"New {severity} case #{case_number}: {problem_statement}".format(severity=row_dict["severity"], case_number=row_dict["case_number"], problem_statement=row_dict["problem_statement"])
			Notifier.notify(message, sound="Sosumi", open=row_dict["case_url"])
			pp.pprint(row_dict)
			logging.info(message)
			logging.info(u"Adding case {case_number} to the set of known cases...".format(case_number=row_dict["case_number"]))
			queue_front_page.add(row_dict["case_number"])
			logging.info("Awaiting new case notifications...")


@retry(retry_on_exception=retry_if_stale_element_reference_exception)
def populate_cases(driver):
	"""Populate the initial queue_front_page set with existing case information."""
	global queue_front_page
	pp = pprint.PrettyPrinter(indent=4)
	time.sleep(1)
	x_grid3_body = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "x-grid3-body")))
	rows = x_grid3_body.find_elements_by_class_name("x-grid3-row")
	for row in rows:
		row_dict = {}
		case_number = row.find_element_by_class_name("x-grid3-col-CASES_CASE_NUMBER")
		row_dict["case_number"] = case_number.text
		row_dict["case_url"] = urljoin(driver.current_url, case_number.find_element_by_tag_name("a").get_attribute("href"))
		row_dict["problem_statement"] = row.find_element_by_class_name("x-grid3-col-00NE0000002C0mc").text
		try:
			row_dict["severity"] = row.find_element_by_class_name("x-grid3-col-00NE0000002BvKo").text.split()[0]
		except:
			row_dict["severity"] = ""
		pp.pprint(row_dict)
		queue_front_page.add(row_dict["case_number"])
	logging.info("End listing of initial first page of incoming queue.")


@retry(retry_on_exception=retry_if_element_not_visible_exception, wait_fixed=1000)
def click_initial_response_column_header(driver):
	"""Sort by Initial Response timestamp."""
	title = "//div[@title='Initial Response Time']"
	initial_response_time_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, title)))
	time.sleep(2)
	driver.execute_script("return arguments[0].scrollIntoView();", initial_response_time_element)
	time.sleep(3)
	logging.info("Clicking column...")
	driver.find_element_by_xpath(title).click()


def main():
	"""Alert user via Notification Center messages when new cases arrive in Incoming Queue."""
	global queue_front_page
	username = None
	password = None
	logging.info("Accessing credentials...")
	with open("credentials.yml", "r") as stream:
		try:
			credentials = yaml.load(stream)
			username = credentials["username"]
			password = credentials["password"]
		except yaml.YAMLError as exc:
			logging.error(exc)
			sys.exit(1)
	chrome_options = Options()
	chrome_options.add_argument("restore-last-session")
	chrome_options.add_argument("start-maximized")
	driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=chrome_options)
	driver.maximize_window()
	logging.info("Accessing Hortonworks Okta Login Page...")
	driver.get("https://hortonworks.okta.com")
	element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "username")))
	element.clear()
	element.send_keys(username)
	element = driver.find_element_by_name("password")
	element.clear()
	element.send_keys(password)
	driver.find_element_by_id("remember").click()
	logging.info("Logging into Okta...")
	driver.find_element_by_id("signin-button").click()
	logging.info("Accessing SalesForce Incoming Queue..")
	driver.get("https://hortonworks.my.salesforce.com/500?fcf=00BE0000001ELz7")
	logging.info("Sorting by Initial Response Time Descending...")
	click_initial_response_column_header(driver)
	logging.info("Sorting by Initial Response Time Ascending...")
	click_initial_response_column_header(driver)
	# Initial page load
	logging.info("Listing initial first page of incoming queue...")
	populate_cases(driver)
	# Incoming Queue reloads
	logging.info("Awaiting new case notifications...")
	while True:
		check_queue(driver)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()
