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


## Common Errors and Work-arounds
### Problem:
```
(tempqueuemonitor) HW13524:queuemonitor josephyoung$ python queuemonitor.py 
[2017-01-12 11:44:19,983] Accessing credentials...
Traceback (most recent call last):
  File "queuemonitor.py", line 152, in <module>
    main()
  File "queuemonitor.py", line 118, in main
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", chrome_options=chrome_options)
  File "/Users/josephyoung/.virtualenvs/tempqueuemonitor/lib/python2.7/site-packages/selenium/webdriver/chrome/webdriver.py", line 62, in __init__
    self.service.start()
  File "/Users/josephyoung/.virtualenvs/tempqueuemonitor/lib/python2.7/site-packages/selenium/webdriver/common/service.py", line 92, in start
    raise WebDriverException("Can not connect to the Service %s" % self.path)
selenium.common.exceptions.WebDriverException: Message: Can not connect to the Service /usr/local/bin/chromedriver
```
### Solution:
Ensure /etc/hosts has an entry for localhost - 127.0.0.1
```
HW13524:~ josephyoung$ ping localhost
ping: cannot resolve localhost: Unknown host
HW13524:~ josephyoung$ sudo vim /etc/hosts
127.0.0.1	localhost

HW13524:~ josephyoung$ ping localhost
PING localhost (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.050 ms
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.120 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.128 ms
^C
--- localhost ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 0.050/0.099/0.128/0.035 ms
```
