FROM alpine

# create a user
RUN adduser -s /bin/ash -D telnet && \
  echo "telnet:password"| chpasswd

# run
RUN apk add --no-cache busybox-extras
CMD ["/usr/sbin/telnetd", "-F", "-b", "0.0.0.0"]
