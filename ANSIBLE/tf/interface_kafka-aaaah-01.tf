resource "cloudru_evolution_compute_interface" "interface_kafka-aaaah-01" {
  security_groups_identifiers = {
    value = [{
      # Нужно заполнить одно из значений - id, name.
      id = cloudru_evolution_compute_security_group.sg-kafka-digitalgov-smevpovd-aaaah.id
      #name = "sg-kafka-digitalgov-smevpovd-aaaah"
    }]
  }

  interface_security_enabled = true
  ip_address = "10.193.32.4"

  subnet_id   = cloudru_evolution_compute_subnet.tech-digitalgov-smevpovd-agentpodd-aaaah.id
  description = "VM kafka-aaaah-01 interface"
  name        = "interface_kafka-aaaah-01"

#  vm_id       = cloudru_evolution_compute_vm.kafka-aaaah-01.id

  zone_identifier = {
    # Нужно заполнить одно из значений - id, name.
    #id   = "03d88664-e91a-4a42-af71-29232677a22d"
    name = "ru.AZ-3"
  }
  
  type = "INTERFACE_TYPE_REGULAR"
  #type = "regular"

  project_id = "c8283765-b545-415e-a8e8-0efdb1b8f10d"
}

