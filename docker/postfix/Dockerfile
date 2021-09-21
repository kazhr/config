FROM centos:7

RUN yum -y update && \
  yum -y install postfix python3 && \
  yum clean all

# ipv6の記述があるとfailedになるためコメントアウト
RUN sed -i -e 's/inet_protocols = all/inet_protocols = ipv4/' /etc/postfix/main.cf
RUN systemctl enable postfix

CMD ["/sbin/init"]
