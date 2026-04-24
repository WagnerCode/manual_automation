terraform {
  required_providers {
    cloudru = {
      source  = "cloud.ru/cloudru/cloud"
      version = "2.0.0"
    }
  }
}

variable "CLOUDRU_KEY_ID" {
  description = "Auth key ID"
  type        = string
}
variable "CLOUDRU_SECRET" {
  description = "Auth secret"
  type        = string
}

provider "cloudru" {
    project_id = "c8283765-b545-415e-a8e8-0efdb1b8f10d"
    auth_key_id         = var.CLOUDRU_KEY_ID
    auth_secret         = var.CLOUDRU_SECRET
    region = "ru-central-1"

    # Идентификатор тенанта объектного хранилища.
    # Скопируйте его из console.cloud.ru, открыв вкладку "Object storage".
    # NOTE: Это опциональный параметр
    object_storage_tenant_id = ""

    # Ендпоинты сервисов продуктов.
    # NOTE: Это обязательный параметр
    endpoints = {
        # IAM
        iam_endpoint = "iam.api.cloud.ru:443"
        # ===

        # === Продукты группы IaaS ===
        # Виртуальные машины
        compute_endpoint = "compute.api.cloud.ru:443"
        
        # Аренда baremetal серверов
        baremetal_endpoint = "baremetal.api.cloud.ru:443"
        # ===

        # Managed Kubernetes
        mk8s_endpoint = "mk8s.api.cloud.ru:443"

        # === Продукты группы Network ===
        # VPC
        vpc_endpoint = "vpc.api.cloud.ru:443"

        # Magic router
        magic_router_endpoint = "magic-router.api.cloud.ru"

        # DNS
        dns_endpoint = "dns.api.cloud.ru:443"

        # Load balancer
        nlb_endpoint = "nlb.api.cloud.ru"
        # ===

        # === Продукты группы DBaaS ===
        # Kafka
        kafka_endpoint = "kafka.api.cloud.ru:443"

        # Redis
        redis_endpoint = "redis.api.cloud.ru:443"
        # ===

        # Объектное хранилище (S3)
        object_storage_endpoint = "https://s3.cloud.ru"
    }
}

