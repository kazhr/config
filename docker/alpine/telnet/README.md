connection test by telnet

# how to
- build
```
# docker build -t alpine:telnet .
```

- run
```
docker run -d -p 127.0.0.1:23:23 alpine:telnet
```

- connect
```
$ telnet localhost
```
