resource "cloudru_evolution_compute_disk" "kafka-aaaah-01_system_disk" {
  project_id = "c8283765-b545-415e-a8e8-0efdb1b8f10d"

  # Обязательные
  name = "kafka-aaaah-01_system_disk"
  size = 50

  zone_identifier = {
    name = "ru.AZ-3"
  }

  disk_type_identifier = {
    name = "SSD"
  }

  # Опциональные
  description = "System disk for kafka-aaaah-01"
  bootable    = true
  image_id    = data.cloudru_evolution_compute_image_collection.kafka-aaaah-01_image.images[0].id
  encrypted   = false
  readonly    = false
  shared      = false
}

