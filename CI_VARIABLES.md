# Required GitLab CI/CD Variables

The following environment variables must be configured in GitLab CI/CD settings (Settings -> CI/CD -> Variables) for the pipeline to function correctly:

## Cloud.Ru Credentials
- `TF_VAR_CLOUDRU_KEY_ID`: Cloud.Ru API Key ID.
- `TF_VAR_CLOUDRU_SECRET`: Cloud.Ru API Secret.
- `CLOUDRU_PROJECT_ID`: Cloud.Ru Project ID.

## Cloud.Ru API URLs
- `CLOUDRU_COMPUTE_API_URL`: URL for Compute API.
- `CLOUDRU_MAGIC_ROUTER_API_URL`: URL for Magic Router API.
- `CLOUDRU_VPC_API_URL`: URL for VPC API.
- `CLOUDRU_QUOTES_API_URL`: URL for Quotes API.
- `CLOUDRU_IAM_API_URL`: URL for IAM API.
- `CLOUDRU_BAREMETAL_API_URL`: URL for Baremetal API.
- `CLOUDRU_MK8S_API_URL`: URL for MK8S API.
- `CLOUDRU_DNS_API_URL`: URL for DNS API.
- `CLOUDRU_NLB_API_URL`: URL for NLB API.
- `CLOUDRU_KAFKA_API_URL`: URL for Kafka API.
- `CLOUDRU_REDIS_API_URL`: URL for Redis API.
- `CLOUDRU_S3_API_URL`: URL for S3 API.

## FreeIPA Credentials
- `IPA_ADDER`: Username for FreeIPA domain joining.
- `IPA_ADDER_PASSWORD`: Password for FreeIPA domain joining.

## Deployment Configuration
- `ANSIBLE_USER`: SSH user for Ansible (default: `user1`).
- `ANSIBLE_PASSWORD`: SSH password for Ansible.
- `ANSIBLE_BECOME_PASS`: Sudo password for Ansible.
- `ANSIBLE_PORT`: SSH port (default: `22`).
- `DOMAIN`: Target domain (default: `agentpodd-platform.tech.pd36.digitalgov.gtn`).
- `ANSIBLE_SSH_COMMON_ARGS`: Additional SSH arguments (e.g., ProxyJump).
- `ANSIBLE_SSH_PRIVATE_KEY_FILE`: Path to the SSH private key file.
- `ANSIBLE_SSH_PRIVATE_KEY`: Content of the SSH private key (if you want to provide it via CI variable and write it to a file in `before_script`).
