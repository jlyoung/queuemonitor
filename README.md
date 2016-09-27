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
sudo pip install -r requirements.txt
```

**Note:** If you receive an error message about not being able to upgrade the `six` module (*OSError: [Errno 1] Operation not permitted*), try:
```
sudo pip install -r requirements.txt --ignore-installed six
```

**Note:** The 1.6.1 version of the pync module available in pypi does not handle non-ascii characters. If you get the following error, upgrade pync directly from GitHub.

### Error message: ###
```
  File "/Users/josephyoung/.virtualenvs/tempqueuemonitor/lib/python2.7/site-packages/pync/TerminalNotifier.py", line 77, in execute
    args = [str(arg) for arg in args]
UnicodeEncodeError: 'ascii' codec can't encode character u'\u2019' in position 50: ordinal not in range(128)
```

### Upgrading pync module: ###
```
sudo pip install --upgrade git+https://github.com/SeTeM/pync.git
```

## Usage
```
$ python queuemonitor.py
```




