# Logging
Logs are saved to the `logs/` directory of the current working directory of RedDrop. The logs are rotated based on the current day and are saved in JSON format. Here is an example of a JSON log:

```json
{
  "asctime": "2022-03-16 15:00:11,557",
  "created": 1647442811.557344,
  "filename": "app.py",
  "funcName": "processRequest",
  "levelname": "INFO",
  "levelno": 20,
  "lineno": 93,
  "module": "app",
  "msecs": 557.3439598083496,
  "message": "A Request Has Been Processed",
  "name": "reddrop.app",
  "pathname": "/reddrop/reddrop/app.py",
  "process": 1,
  "processName": "MainProcess",
  "relativeCreated": 703922.0747947693,
  "thread": 140006108112640,
  "threadName": "waitress-1",
  "time": "2022-03-16T15:00:11.284084",
  "remote_addr": "172.17.0.1",
  "src": "172.17.0.1",
  "method": "POST",
  "path": "var/log",
  "files": [
    {
      "fileDir": "/reddrop/uploads/172.17.0.1",
      "fileName": "16-Mar-2022-15-00-11.logs.-.tar.gz",
      "isArchive": true,
      "autoExtracted": true,
      "process": [
        "b64",
        "openssl-aes256-pbkdf2",
        "gzip",
        "hex",
        "b64",
        "gzip"
      ],
      "parameter": "logs"
    }
  ],
  "headers": {
    "Host": "172.17.0.1",
    "User-Agent": "curl/7.68.0",
    "Accept": "*/*",
    "Content-Length": "82416",
    "Content-Type": "multipart/form-data; boundary=------------------------7c51af53f65714ee",
    "Expect": "100-continue"
  },
  "data": [
    {
      "field": "listing",
      "originalValue": "H4sIAAAAAAAAA52SUW6EIBCG3z3FXAAiIyJ4gH1regasdtcUF4O02p6+6LZd2EQfOpkQEuZjfn6G\nuJk4siYwcNb62xKCsRxOXQOggMm6RGAZ2SkOpYLfiiWwsi4kaOM7d9W+/+gmaux5ly1lqRCeX8JW\nABM1l9CEg8k7Pd7BmZA7+O6HcVVYCRk15QKacLDXCJFVQdeTdj8v4gW049v5UFyBeYFxjxJedW+O\nkBDI/oxTdeD7a9st9OIH8z+Ksl8T3IMJqDBkKtDoyUe+PSJb5LHhFcyrb5kefZ1567UBJbLWzYsj\na6ZKea5E6iI9rk0eRemuBXK1Orm468dtBOjytfurHJGn1KWfvHWf8b9Gs6PbIegSUrCUCtM6bMg3\nf9gP+hEDAAA=",
      "processedValue": "-rw-r--r-- 1 root root    110 Feb  9 18:52 1\n-rw-r--r-- 1 root root  11064 Feb  8 15:38 alternatives.log\n-rw-r--r-- 1 root root  58592 Oct  6 16:48 bootstrap.log\n-rw-rw---- 1 root utmp    768 Feb  8 15:46 btmp\n-rw-r--r-- 1 root root 221738 Mar  9 18:43 dpkg.log\n-rw-r--r-- 1 root root  32032 Feb  8 15:45 faillog\n-rw-r--r-- 1 root root     21 Feb  9 19:32 index.html\n-rw-r--r-- 1 root root     21 Feb  9 19:32 index.html.1\n-rw-rw-r-- 1 root utmp 292292 Feb  8 15:45 lastlog\n-rw-rw-r-- 1 root utmp      0 Oct  6 16:47 wtmp\n\napt:\ntotal 96\ndrwxr-xr-x 1 root root  4096 Mar  9 18:43 .\ndrwxr-xr-x 1 root root  4096 Feb  9 19:32 ..\n-rw-r--r-- 1 root root  8032 Mar  9 18:43 eipp.log.xz\n-rw-r--r-- 1 root root 24224 Mar  9 18:43 history.log\n-rw-r----- 1 root adm  46861 Mar  9 18:43 term.log\n",
      "process": [
        "b64",
        "gzip"
      ]
    }
  ],
  "password": null
}
```