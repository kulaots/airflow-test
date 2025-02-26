# Airflow test


podman run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_rsa:/root/id_rsa willhallonline/ansible:latest ansible-playbook playbook.yml
