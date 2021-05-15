# how to
- build
```
# docker build -t alpine:nopasswd .
```

- connect
```
$ ssh -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -i ./id_ed25519 \
  developer@localhost
```
