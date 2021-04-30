# for ansible test
FROM centos:7

RUN yum -y update && \
  yum -y install openssh-server sudo && \
  yum clean all

RUN useradd -m -s /bin/bash developer

COPY ./id_ed25519.pub /home/developer/authorized_keys

RUN mkdir /home/developer/.ssh && \
  chmod 700 /home/developer/.ssh && \
  mv /home/developer/authorized_keys /home/developer/.ssh/authorized_keys && \
  chmod 600 /home/developer/.ssh/authorized_keys && \
  chown developer:developer -R /home/developer/

COPY ./sudoers.d/developer /etc/sudoers.d/

CMD ["/sbin/init"]
