# how to
- build
```
# docker build -t centos:nopasswd .
```

- run
```
# docker run -d -p 22:22 --privileged centos:nopasswd
```

- connect
```
$ ssh -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -i ./id_ed25519 \
  developer@localhost
```
