FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y openssh-server

RUN mkdir /root/.ssh
RUN chmod 700 /root/.ssh
ADD adds/authorized_keys /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/*
RUN chown -Rf root:root /root/.ssh

ADD adds/sshd_config /etc/ssh/sshd_config

EXPOSE 40

CMD /usr/bin/tail -f /dev/null