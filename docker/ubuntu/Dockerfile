# for ansible test
FROM ubuntu:latest

# Configuring tzdataで止まらないように
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    openssh-server \
    sudo \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash developer
COPY ./sudoers.d/developer /etc/sudoers.d/

COPY ./id_ed25519.pub /home/developer/authorized_keys
RUN mkdir /home/developer/.ssh && \
  chmod 700 /home/developer/.ssh && \
  mv /home/developer/authorized_keys /home/developer/.ssh/authorized_keys && \
  chmod 600 /home/developer/.ssh/authorized_keys && \
  chown developer:developer -R /home/developer/

CMD ["/sbin/init"]
