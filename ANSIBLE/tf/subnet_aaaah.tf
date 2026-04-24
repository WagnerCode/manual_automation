resource "cloudru_evolution_compute_subnet" "tech-digitalgov-smevpovd-agentpodd-aaaah" {
  project_id = "c8283765-b545-415e-a8e8-0efdb1b8f10d"

  # Обязательные
  name = "tech-digitalgov-smevpovd-agentpodd-aaaah"

  zone_identifier = {
    name = "ru.AZ-3"
  }

  # Опциональные
  description    = "Subnet 10.193.32.0/28 for digitalgov-smevpovd cluster aaaah"
  subnet_address = "10.193.32.0/28"
  routed_network = true
  default        = true
  #vpc_id         = data.cloudru_evolution_vpc_vpc_collection.vpc_default.vpcs[0].id
  vpc_id         = "790f116c-99b0-4ce9-bb43-aff5f4eafb4e"

  dns_servers = {
    value = [ "10.246.0.140", "10.246.0.141" ]
  }
}

