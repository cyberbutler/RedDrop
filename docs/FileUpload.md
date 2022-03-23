# RedDrop File Upload
File upload is a core feature of RedDrop. It is enabled to all routes and allows any `multipart-form` request to be a file upload. Eventually, other types of requests may be added for file upload, but for the moment a request must be a `multipart-form` message similar to the following:

```http
POST / HTTP/1.1
Host: reddrop
User-Agent: curl/7.68.0
Accept: */*
Content-Length: 1123
Content-Type: multipart/form-data; boundary=------------------------d985840f7e960320
Expect: 100-continue

--------------------------d985840f7e960320
Content-Disposition: form-data; name="file"; filename="passwd"
Content-Type: application/octet-stream

root:x:0:0:root:/root:/bin/zsh
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin

--------------------------d985840f7e960320--
```

This file was uploaded with the following command:
```bash
curl http://reddrop/ -F 'file=@/etc/passwd'
```