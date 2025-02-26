# Use the official Ubuntu image as the base image
FROM ubuntu:latest
# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    apt-get install -y vim && \
    apt-get install -y git && \
    apt-get clean

RUN pip3 install --upgrade pip; \
    pip3 install "ansible==${ANSIBLE_VERSION}"; \
    pip3 install ansible
    
RUN git clone git@github.com:kulaots/airflow-test.git /

RUN mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# Expose the SSH port
EXPOSE 22



# Start the SSH server
CMD ["/usr/sbin/sshd", "-D"]