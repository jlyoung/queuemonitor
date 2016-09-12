# queuemonitor

## Summary
**queuemonitor** is a SalesForce scraper written to poll the Incoming Queue for new support cases and alert the user with an OS X Notification Center message and audible tone.

## Requirements
- OS X
- Python version 2.6 or 2.7
- [pip](https://pip.pypa.io/en/stable/installing/)
- [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) installed at `/usr/local/bin/chromedriver`

## Installation
Clone this repository to download the source:
```
git clone https://github.com/jlyoung/queuemonitor.git
```

Modify `credentials.yml`:
- Replace `okta_username` with your actual Okta username.
- Replace `okta_password` with your actual Okta password.

Install required packages:
```
pip install -r requirements.txt
```

**Note:** If you receive an error message about not being able to upgrade the `six` module (*OSError: [Errno 1] Operation not permitted*), try:
```
pip install -r requirements.txt --ignore-installed six
```

## Usage
```
$ python queuemonitor.py
```




