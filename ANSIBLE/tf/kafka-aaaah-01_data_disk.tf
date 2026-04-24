resource "cloudru_evolution_compute_disk" "kafka-aaaah-01_data_disk" {
  project_id = "c8283765-b545-415e-a8e8-0efdb1b8f10d"

  # Обязательные
  name = "kafka-aaaah-01_data_disk"
  size = 60

  zone_identifier = {
    name = "ru.AZ-3"
  }

  disk_type_identifier = {
    name = "SSD"
  }

  # Опциональные
  description = "Data disk for kafka-aaaah-01"
  bootable    = false
#  image_id    = "474c9e98-760f-4e54-aaa9-70024814f2b0"
  encrypted   = false
  readonly    = false
  shared      = false
}

