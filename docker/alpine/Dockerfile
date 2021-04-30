# for connection test
# (SSH public key authentication & sudo without a password)
FROM alpine

# create a ssh user
RUN apk add --no-cache shadow

RUN adduser -s /bin/ash -D developer && \
  usermod -p "*" developer
  # 公開鍵認証だとしてもパスワードが空だと拒否される

COPY ./id_ed25519.pub /home/developer/authorized_keys

RUN mkdir /home/developer/.ssh && \
  chmod 700 /home/developer/.ssh && \
  mv /home/developer/authorized_keys /home/developer/.ssh/authorized_keys && \
  chown developer:developer -R /home/developer/

# setup suders
RUN apk add --no-cache sudo

COPY ./sudoers.d/developer /etc/sudoers.d/

# run sshd
RUN apk add --no-cache openssh && \
  ssh-keygen -A

CMD ["/usr/sbin/sshd", "-D", "-e"]
