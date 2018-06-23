# ScanTrust BDB API

ScanTrust BDB API is an API that enables collaboration between the scantrust toolset and __BigchainDB__.

  - Flask API app
  - Decentralized BigchaibDB

 This project includes a mock of the ScanTrust backend in order to provide a runnable demo.

### More Information
---
  - [Flask](http://flask.pocoo.org/) - Flask (A Python micro framework)
  - [BigchainDB](https://www.bigchaindb.com/) - BigchainDB partly decentralized database

### Installation
---
__Requirements:__
  - Python 3.5+
  - BigchainDB Driver

```sh
(virtualenv)$ cd backend
(virtualenv)$ pip install -r requirements.txt
```
Edit *backend/conf/sample_conf.cfg* and copy to *backend/app.cfg*

### Usage
---
Run a local test server:
```sh
(virtualenv)$ ./runserver.py
```