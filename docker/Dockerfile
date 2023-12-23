FROM ubuntu:18.04
RUN apt-get update && apt-get install -y git python python-pip curl iptables openssh-server sudo
#library needed to run ssh commands and collect output
RUN pip install paramiko colorama scp
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sudo mkdir /var/run/sshd
RUN sudo mkdir /root/.ssh && sudo chmod 700 /root/.ssh
RUN sudo mkdir -p /etc/cron.d && sudo chmod 644 /etc/cron.d
COPY docker/hedge /root/.ssh/id_rsa
COPY docker/hedge.pub /root/.ssh/authorized_keys
RUN sudo chmod 600 /root/.ssh/id_rsa && sudo chmod 600 /root/.ssh/authorized_keys
RUN useradd -ms /bin/bash testuser
RUN groupadd testgroup

# key with non-default name that has to be passed manually to paramiko
# in order to connec to different host
COPY docker/hedge_unknown /root/.ssh/hedge_unknown
RUN sudo chmod 600 /root/.ssh/hedge_unknown