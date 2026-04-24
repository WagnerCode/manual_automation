resource "cloudru_evolution_compute_placement_group" "placement_group_aaaah" {
  #policy      = "soft-anti-affinity"
  policy      = "PLACEMENT_GROUP_POLICY_SOFT_ANTI_AFFINITY"
  description = "Placement group for cluster config.vm_params[0].ogid"
  project_id  = "c8283765-b545-415e-a8e8-0efdb1b8f10d"
  name        = "placement_group_aaaah"
}
