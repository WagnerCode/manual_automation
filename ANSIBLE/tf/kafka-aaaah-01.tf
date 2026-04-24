resource "cloudru_evolution_compute_vm" "kafka-aaaah-01" {
  project_id = "c8283765-b545-415e-a8e8-0efdb1b8f10d"

  # Обязательные
  name = "kafka-aaaah-01"

  zone_identifier = {
    name = "ru.AZ-3"
  }

  flavor_identifier = {
    name = "low-16-32"
  }

  # Опциональные
  description = "Cluster aaaah VM kafka-aaaah-01"

  disk_identifiers = [
     {
        disk_id = cloudru_evolution_compute_disk.kafka-aaaah-01_system_disk.id
     },
     {
        disk_id = cloudru_evolution_compute_disk.kafka-aaaah-01_data_disk.id
     }
  ]

  network_interfaces = [{
    interface_id = cloudru_evolution_compute_interface.interface_kafka-aaaah-01.id
  }]

#  image_metadata      =  {
#         hostname = { 
#                 string_value = "kafka-aaaah-01"
#         }
#         public_key = {
#                string_value = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDTL2d9J5eHMnk+HZQcn3/7OfjlRFqIYyW8IvrKdaC2OvOssgcadVGAYYjUbUZb6pBx0/bxxqRyfE2ByNBb2b7TL4GuyyavvsvPFBOBETJXx1+WjMwF3lna8xNYX9nSVkOh7uDjX4kB8bIJQyT3ilWfrAJuv7A9pTpXrSQq5MMbTHNHGlVnDIxvFNqUc/5fVgtxGgFDVrEokWSYo6ptxdI+jmS692FdpRhQINLLegBQjO1h6LM3xlM3XkXSEbxujO5Rj/D9xezSyQYfhkwzj3V5wi8ffq5ConvP2AT7g6KnHw9rv2fv/8Cab1nTCLEx527wP5R5XlpZao4yOsILapwg/AAIq8cDaZuhlBzszF2TiAo4gImJSWi2OQZfq60EerpeI0vQ+fFrdyMbRDRF0ZMBklVAkOhi+wizPBs1W+EJTnfsLOCW36a3WAFYvwW6MQvJR0o55xcHEAlUW2Le4Loiou/nE8LX8Jfpr0khGJacehaeQm3burXSy0urE4V9vQM= dkulida@fedora"
#                #int_value = 801329956
#                #bool_value = false
#         },
#         name = {
#             string_value = "user1"
#         },
#         linux_password = {
#             string_value = "Test1@3456789"
#         }
#
#  }

  placement_group_id = cloudru_evolution_compute_placement_group.placement_group_aaaah.id

  cloud_init_userdata = base64encode(<<-CLOUDINIT
    #cloud-config
    package_update: true
    packages:
      - curl
      - wget
    runcmd:
      - echo "Hello from Terraform!" > /tmp/hello.txt
      - adduser -g wheel user1
      - echo 'user1:Test1@3456789' | chpasswd
      - echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDTL2d9J5eHMnk+HZQcn3/7OfjlRFqIYyW8IvrKdaC2OvOssgcadVGAYYjUbUZb6pBx0/bxxqRyfE2ByNBb2b7TL4GuyyavvsvPFBOBETJXx1+WjMwF3lna8xNYX9nSVkOh7uDjX4kB8bIJQyT3ilWfrAJuv7A9pTpXrSQq5MMbTHNHGlVnDIxvFNqUc/5fVgtxGgFDVrEokWSYo6ptxdI+jmS692FdpRhQINLLegBQjO1h6LM3xlM3XkXSEbxujO5Rj/D9xezSyQYfhkwzj3V5wi8ffq5ConvP2AT7g6KnHw9rv2fv/8Cab1nTCLEx527wP5R5XlpZao4yOsILapwg/AAIq8cDaZuhlBzszF2TiAo4gImJSWi2OQZfq60EerpeI0vQ+fFrdyMbRDRF0ZMBklVAkOhi+wizPBs1W+EJTnfsLOCW36a3WAFYvwW6MQvJR0o55xcHEAlUW2Le4Loiou/nE8LX8Jfpr0khGJacehaeQm3burXSy0urE4V9vQM= dkulida@fedora" >> /home/user1/.ssh/authorized_keys
      - chmod 600 /home/user1/.ssh/authorized_keys
      - mkdir -p /etc/net/ifaces/eth0
      - echo "ONBOOT=yes" > /etc/net/ifaces/eth0/options
      - echo "DISABLED=no" >> /etc/net/ifaces/eth0/options
      - echo "CONFIG_IPV4=yes" >> /etc/net/ifaces/eth0/options
      - echo "CONFIG_WIRELESS=no" >> /etc/net/ifaces/eth0/options
      - echo "TYPE=eth" >> /etc/net/ifaces/eth0/options
      - echo "NM_CONTROLLED=no" >> /etc/net/ifaces/eth0/options
      - echo "BOOTPROTO=static" >> /etc/net/ifaces/eth0/options
      - echo "10.193.32.4/28" >> /etc/net/ifaces/eth0/ipv4address
      - echo "default via 10.193.32.1" >> /etc/net/ifaces/eth0/ipv4route
      - sleep 10
      - hostnamectl hostname kafka-aaaah-01.agentpodd-platform.tech.pd36.digitalgov.gtn
      - systemctl restart network
      - rm /etc/resolv.conf
      - echo "nameserver 10.246.0.140" >> /etc/resolv.conf
      - echo "nameserver 10.246.0.141" >> /etc/resolv.conf
  CLOUDINIT
  )
}

