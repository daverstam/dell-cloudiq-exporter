# dell-cloudiq-exporter

Dell CloudIQ exporter for Prometheus. 

Exports data and metrics from these categories:
- Storage Systems
- Network Systems
- Server Systems  
and more...

# Usage
Tested on Linux and Mac with Python 3.10 however it will likely work fine with Python 3.9  

Install the necessary dependencies with pip:
```
pip install -r requirements.txt
```
Edit config.yml:
- Insert your tokens generated from CloudIQ
- Set the metrics you wish to fetch to true (use as few as possible since each metric will increase the scrape duration)
- Set a listening port in config.yml  

Run the exporter:
```
python cloudiq_exporter.py
```

# Configuration
You need to generate your own CloudIQ Client ID and Client Secret, you can do this from the the CloudIQ api website: https://cloudiq.emc.com/ui/index.html#/api  
These tokens will be valid for 12 months.  

Your account need to have the DevOps role to be able to generate API credentials.  
The exporter will fetch and use a specific token for each API request, this token is valid for 1 hour, if that time has exceeded the exporter will request a new token.

config.yml example:
```
---
cloudiq_base_url: "https://cloudiq.apis.dell.com/cloudiq"
cloudiq_token_url: "https://cloudiq.apis.dell.com/auth/oauth/v2/token"

# These tokens can be generated at https://cloudiq.emc.com/ui/index.html#/api
# A CloudIQ API Key expires after 12 months and you must regenerate it.
cloudiq_client_id: "id"
cloudiq_client_secret: "secret"

# Port the http exporter will be listening on
exporter_listening_port: 9090

# Set what you wish to collect to true, each metric you enable will increase the scrape duration
metrics:

# Hardware:
  ports:
    collect: false
    url: "/rest/v1/ports"

# Storage:
  datastores:
    collect: false
    url: "/rest/v1/datastores"
  drives:
    collect: false
    url: "/rest/v1/drives"
  filesystems:
    collect: false
    url: "/rest/v1/filesystems"
  hosts:
    collect: false
    url: "/rest/v1/hosts"
  pools:
    collect: false
    url: "/rest/v1/pools"
  storage_groups:
    collect: false
    url: "/rest/v1/storage_groups"
  storage_resource_pools:
    collect: false
    url: "/rest/v1/storage_resource_pools"
  volumes:
    collect: false
    url: "/rest/v1/volumes"

# Systems:
  network_systems:
    collect: false
    url: "/rest/v1/network_systems"
  server_systems:
    collect: true
    url: "/rest/v1/server_systems"
  storage_systems:
    collect: true
    url: "/rest/v1/storage_systems"
```

# Exported Metrics
```
# Hardware:
  ports:
    # HELP info about ports.
    # TYPE cloudiq_ports_info gauge

# Storage:
  datastores:
    # HELP cloudiq_datastores_info Info about datastores.
    # TYPE cloudiq_datastores_info gauge

  drives:
    # HELP cloudiq_drives_endurance_days Estimated number of days left before drive will reach specified write endurance and must be replaced.
    # TYPE cloudiq_drives_endurance_days gauge
    # HELP cloudiq_drives_endurance_percent Percentage of write endurance left, based on specified maximum write endurance of drive.
    # TYPE cloudiq_drives_endurance_percent gauge
    # HELP cloudiq_drives_free_size Free Size of the drive.
    # TYPE cloudiq_drives_free_size gauge
    # HELP cloudiq_drives_issue_count Number of health issues that are present on the drive.
    # TYPE cloudiq_drives_issue_count gauge
    # HELP cloudiq_drives_used_size Used Size of the drive.
    # TYPE cloudiq_drives_used_size gauge
    # HELP cloudiq_drives_size Size of the drive.
    # TYPE cloudiq_drives_size gauge

  filesystems:
    # HELP cloudiq_filesystems_allocated_size The allocated size of the file system.
    # TYPE cloudiq_filesystems_allocated_size gauge
    # HELP cloudiq_filesystems_data_reduction_percent The data reduction percent for the file system.
    # TYPE cloudiq_filesystems_data_reduction_percent gauge
    # HELP cloudiq_filesystems_data_reduction_ratio The data reduction ratio for the file system.
    # TYPE cloudiq_filesystems_data_reduction_ratio gauge
    # HELP cloudiq_filesystems_data_reduction_saved_size The data reduction saved size for the file system.
    # TYPE cloudiq_filesystems_data_reduction_saved_size gauge
    # HELP cloudiq_filesystems_issue_count Number of health issues that are present on the file system.
    # TYPE cloudiq_filesystems_issue_count gauge
    # HELP cloudiq_filesystems_total_size The total size of the file system.
    # TYPE cloudiq_filesystems_total_size gauge
    # HELP cloudiq_filesystems_used_percent Percentage used for the file system.
    # TYPE cloudiq_filesystems_used_percent gauge
    # HELP cloudiq_filesystems_used_size Size used for the file system.
    # TYPE cloudiq_filesystems_used_size gauge

  hosts:
    # HELP cloudiq_hosts_issue_count Number of health issues that are present on the host or server.
    # TYPE cloudiq_hosts_issue_count gauge
    # HELP cloudiq_hosts_total_size Total size of all LUNs or Volumes that are provisioned to the host or server from the system.
    # TYPE cloudiq_hosts_total_size gauge
    # HELP cloudiq_hosts_initiator_count Number of initiators that are connected between the host or server and the monitored system.
    # TYPE cloudiq_hosts_initiator_count gauge

  pools:
    # HELP cloudiq_pools_free_size Available capacity.
    # TYPE cloudiq_pools_free_size gauge
    # HELP cloudiq_pools_issue_count Number of health issues that are present on the pool.
    # TYPE cloudiq_pools_issue_count gauge
    # HELP cloudiq_pools_subscribed_percent Percentage of pool capacity that is provisioned.
    # TYPE cloudiq_pools_subscribed_percent gauge
    # HELP cloudiq_pools_subscribed_size Total subscribed capacity of the pool.
    # TYPE cloudiq_pools_subscribed_size gauge
    # HELP cloudiq_pools_total_size Total capacity of the pool.
    # TYPE cloudiq_pools_total_size gauge
    # HELP cloudiq_pools_used_percent Percentage of pool capacity that is being used.
    # TYPE cloudiq_pools_used_percent gauge
    # HELP cloudiq_pools_used_size Capacity of the pool that is being used.
    # TYPE cloudiq_pools_used_size gauge

  storage_groups:
    # HELP cloudiq_storage_groups_allocated_size The Allocated capacity.
    # TYPE cloudiq_storage_groups_allocated_size gauge
    # HELP cloudiq_storage_groups_compressionratio The Compression ratio for the SG.
    # TYPE cloudiq_storage_groups_compressionratio gauge
    # HELP cloudiq_storage_groups_compression_saved_percent The compression percent.
    # TYPE cloudiq_storage_groups_compression_saved_percent gauge
    # HELP cloudiq_storage_groups_data_reduction_ratio Storage group efficiency data reduction ratio.
    # TYPE cloudiq_storage_groups_data_reduction_ratio gauge
    # HELP cloudiq_storage_groups_effective_used Storage group capacity effective used.
    # TYPE cloudiq_storage_groups_effective_used gauge
    # HELP cloudiq_storage_groups_free_size The free subscribe capacity.
    # TYPE cloudiq_storage_groups_free_size gauge
    # HELP cloudiq_storage_groups_masking_view_count Masking views.
    # TYPE cloudiq_storage_groups_masking_view_count gauge
    # HELP cloudiq_storage_groups_physical_used Storage group capacity physical used.
    # TYPE cloudiq_storage_groups_physical_used gauge
    # HELP cloudiq_storage_groups_provisioned Storage group capacity provisioned.
    # TYPE cloudiq_storage_groups_provisioned gauge
    # HELP cloudiq_storage_groups_snaphot_physical_used Storage group efficiency snapshot physical used.
    # TYPE cloudiq_storage_groups_snaphot_physical_used gauge
    # HELP cloudiq_storage_groups_snapshot_count The total number of Snapshots associated with the SG.
    # TYPE cloudiq_storage_groups_snapshot_count gauge
    # HELP cloudiq_storage_groups_snapshot_drr_ratio Storage group efficiency snapshot data reduction ratio.
    # TYPE cloudiq_storage_groups_snapshot_drr_ratio gauge
    # HELP cloudiq_storage_groups_snapshot_effective_used Storage group efficiency snapshot effective used.
    # TYPE cloudiq_storage_groups_snapshot_effective_used gauge
    # HELP cloudiq_storage_groups_snapshot_resources_percent Storage group efficiency snapshot resources percent.
    # TYPE cloudiq_storage_groups_snapshot_resources_percent gauge
    # HELP cloudiq_storage_groups_subscribed_size The total Subscribe capacity.
    # TYPE cloudiq_storage_groups_subscribed_size gauge
    # HELP cloudiq_storage_groups_total_size The Total capacity.
    # TYPE cloudiq_storage_groups_total_size gauge
    # HELP cloudiq_storage_groups_unreducible_data Storage group efficiency unreducible data.
    # TYPE cloudiq_storage_groups_unreducible_data gauge
    # HELP cloudiq_storage_groups_volume_count The total number of Volumes associated with the SG.
    # TYPE cloudiq_storage_groups_volume_count gauge

  storage_resource_pools:
    # HELP cloudiq_storage_resource_pools_allocated_subscribed_percent Percentage of the subscribed capacity.
    # TYPE cloudiq_storage_resource_pools_allocated_subscribed_percent gauge
    # HELP cloudiq_storage_resource_pools_allocated_subscribed_size The used subscribe capacity.
    # TYPE cloudiq_storage_resource_pools_allocated_subscribed_size gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_data_reducing_percent SRP capacity for CKD data reduction percent.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_data_reducing_percent gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_data_reduction_disabled SRP Capacity for CKD data reduction effective used data reduction disabled.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_data_reduction_disabled gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_enabled_and_reducing SRP capacity for CKD data reduction effective used enabled and reducing.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_enabled_and_reducing gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_enabled_and_unevaluated SRP capacity for CKD data reduction effective used enabled and unevaluated.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_enabled_and_unevaluated gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_enabled_and_unreducible SRP capacity for CKD A data reduction effective used enabled and unreducible.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_effective_used_enabled_and_unreducible gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_data_reduction_disabled SRP capacity for CKD data reduction physical used data reduction disabled.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_data_reduction_disabled gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_enabled_and_reducing SRP capacity for CKD data reduction physical used enabled and reducing.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_enabled_and_reducing gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_enabled_and_unevaluated SRP capacity for CKD data reduction physical used enabled and unevaluated.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_enabled_and_unevaluated gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_enabled_and_unreducible SRP capacity for CKD data reduction physical used enabled and unreducible.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_physical_used_enabled_and_unreducible gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_ratio_to_one SRP capacity for CKD data reduction ratio to one.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_ratio_to_one gauge
    # HELP cloudiq_storage_resource_pools_ckd_data_reduction_savings SRP capacity for CKD data reduction savings.
    # TYPE cloudiq_storage_resource_pools_ckd_data_reduction_savings gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_capacity_resources_free SRP Capacity for CKD effective capacity resources free.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_capacity_resources_free gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_capacity_resources_total SRP capacity for CKD effective capacity resources total.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_capacity_resources_total gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_capacity_resources_used SRP capacity for CKD effective capacity resources used.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_capacity_resources_used gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_capacity_usage_free SRP capacity for CKD effective capacity usage free.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_capacity_usage_free gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_capacity_usage_snapshot_used SRP capacity for CKD effective capacity usage snapshots used.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_capacity_usage_snapshot_used gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_capacity_usage_user_used SRP capacity for CKD effective capacity usage user used.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_capacity_usage_user_used gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_free SRP capacity for CKD effective free.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_free gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_physical_free SRP capacity for CKD effective physical free.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_physical_free gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_physical_target SRP capacity for CKD effective physical target.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_physical_target gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_physical_total SRP capacity for CKD effective physical total.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_physical_total gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_physical_used SRP capacity for CKD-FBCKD A effective physical used.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_physical_used gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_target SRP capacity for CKD-FCKD BA effective target.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_target gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_total SRP capacity for CKD effective total.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_total gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_used SRP capacity for CKD effective used.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_used gauge
    # HELP cloudiq_storage_resource_pools_ckd_effective_used_percent SRP capacity for CKD effective used percent.
    # TYPE cloudiq_storage_resource_pools_ckd_effective_used_percent gauge
    # HELP cloudiq_storage_resource_pools_ckd_provisioned_effective SRP capacity for CKD provisioned effective.
    # TYPE cloudiq_storage_resource_pools_ckd_provisioned_effective gauge
    # HELP cloudiq_storage_resource_pools_ckd_provisioned_provisioned_percent SRP capacity for CKD provisioned percent.
    # TYPE cloudiq_storage_resource_pools_ckd_provisioned_provisioned_percent gauge
    # HELP cloudiq_storage_resource_pools_ckd_provisioned_used SRP capacity for CKD provisioned used.
    # TYPE cloudiq_storage_resource_pools_ckd_provisioned_used gauge
    # HELP cloudiq_storage_resource_pools_ckd_snapshot_effective_used_percent SRP capacity for CKD snapshot effective used percent.
    # TYPE cloudiq_storage_resource_pools_ckd_snapshot_effective_used_percent gauge
    # HELP cloudiq_storage_resource_pools_ckd_snapshot_physical_used_percent SRP capacity for CKD snapshot physical used percent.
    # TYPE cloudiq_storage_resource_pools_ckd_snapshot_physical_used_percent gauge
    # HELP cloudiq_storage_resource_pools_ckd_snapshot_resource_used SRP capacity for CKD snapshot resource used.
    # TYPE cloudiq_storage_resource_pools_ckd_snapshot_resource_used gauge
    # HELP cloudiq_storage_resource_pools_collection_timestamp Last time when the configuration data has been collected.
    # TYPE cloudiq_storage_resource_pools_collection_timestamp gauge
    # HELP cloudiq_storage_resource_pools_data_reduction_enabled_percent The Data reduction percent.
    # TYPE cloudiq_storage_resource_pools_data_reduction_enabled_percent gauge
    # HELP cloudiq_storage_resource_pools_data_reduction_savings The Data reduction ratio.
    # TYPE cloudiq_storage_resource_pools_data_reduction_savings gauge
    # HELP cloudiq_storage_resource_pools_deduplication_and_compression_savings SRP efficiency deduplication and compression.
    # TYPE cloudiq_storage_resource_pools_deduplication_and_compression_savings gauge
    # HELP cloudiq_storage_resource_pools_drr_on_reducible_only_to_one SRP efficiency DDR on reducible.
    # TYPE cloudiq_storage_resource_pools_drr_on_reducible_only_to_one gauge
    # HELP cloudiq_storage_resource_pools_effective_capacity The Effective Capacity used on the Storage Resource Pool.
    # TYPE cloudiq_storage_resource_pools_effective_capacity gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_data_reducing_percent SRP capacity for FBA data reducing percent.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_data_reducing_percent gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_effective_used_data_reduction_disabled SRP capacity for FBA data reduction effective used data reduction disabled.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_effective_used_data_reduction_disabled gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_effective_used_enabled_and_reducing SRP capacity for FBA data reduction effective used enabled and reducing.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_effective_used_enabled_and_reducing gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_effective_used_enabled_and_unevaluated SRP capacity for FBA data reduction effective used enabled and unevaluated.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_effective_used_enabled_and_unevaluated gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_effective_used_enabled_and_unreducible SRP capacity for FBA data reduction effective used enabled and unreducible.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_effective_used_enabled_and_unreducible gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_physical_used_data_reduction_disabled SRP Capacity for FBA data reduction physical used data reduction disabled.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_physical_used_data_reduction_disabled gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_physical_used_enabled_and_reducing SRP capacity for FBA data reduction physical used enabled and reducing.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_physical_used_enabled_and_reducing gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_physical_used_enabled_and_unevaluated SRP capacity for FBA data reduction physical used enabled and unevaluated.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_physical_used_enabled_and_unevaluated gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_physical_used_enabled_and_unreducible SRP capacity for FBA data reduction physical used enabled and unreducible.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_physical_used_enabled_and_unreducible gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_ratio_to_one SRP capacity for FBA data reduction ratio to one.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_ratio_to_one gauge
    # HELP cloudiq_storage_resource_pools_fba_data_reduction_savings SRP capacity for FBA data reduction savings.
    # TYPE cloudiq_storage_resource_pools_fba_data_reduction_savings gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_capacity_resources_free SRP capacity for FBA effective capacity resources free.
    # TYPE cloudiq_storage_resource_pools_fba_effective_capacity_resources_free gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_capacity_resources_total SRP capacity for FBA effective capacity resources total.
    # TYPE cloudiq_storage_resource_pools_fba_effective_capacity_resources_total gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_capacity_resources_used SRP capacity for FBA effective capacity resources used.
    # TYPE cloudiq_storage_resource_pools_fba_effective_capacity_resources_used gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_capacity_usage_free SRP capacity for FBA effective capacity usage free.
    # TYPE cloudiq_storage_resource_pools_fba_effective_capacity_usage_free gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_capacity_usage_snapshot_used SRP capacity for FBA effective capacity usage snapshots used.
    # TYPE cloudiq_storage_resource_pools_fba_effective_capacity_usage_snapshot_used gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_capacity_usage_user_used SRP capacity for FBA effective capacity usage user used.
    # TYPE cloudiq_storage_resource_pools_fba_effective_capacity_usage_user_used gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_free SRP capacity for FBA effective free.
    # TYPE cloudiq_storage_resource_pools_fba_effective_free gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_physical_free SRP capacity for FBA effective physical free.
    # TYPE cloudiq_storage_resource_pools_fba_effective_physical_free gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_physical_target SRP capacity for FBA effective physical target.
    # TYPE cloudiq_storage_resource_pools_fba_effective_physical_target gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_physical_total SRP capacity for FBA effective physical total.
    # TYPE cloudiq_storage_resource_pools_fba_effective_physical_total gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_physical_used SRP capacity for FBA effective physical used.
    # TYPE cloudiq_storage_resource_pools_fba_effective_physical_used gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_target SRP capacity for FBA effective target.
    # TYPE cloudiq_storage_resource_pools_fba_effective_target gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_total SRP capacity for FBA effective total.
    # TYPE cloudiq_storage_resource_pools_fba_effective_total gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_used SRP capacity for FBA effective used.
    # TYPE cloudiq_storage_resource_pools_fba_effective_used gauge
    # HELP cloudiq_storage_resource_pools_fba_effective_used_percent SRP capacity for FBA effective used percent.
    # TYPE cloudiq_storage_resource_pools_fba_effective_used_percent gauge
    # HELP cloudiq_storage_resource_pools_fba_provisioned_effective SRP capacity for FBA provisioned effective.
    # TYPE cloudiq_storage_resource_pools_fba_provisioned_effective gauge
    # HELP cloudiq_storage_resource_pools_fba_provisioned_provisioned_percent SRP capacity for FBA provisioned percent.
    # TYPE cloudiq_storage_resource_pools_fba_provisioned_provisioned_percent gauge
    # HELP cloudiq_storage_resource_pools_fba_provisioned_used SRP capacity for FBA provisioned used.
    # TYPE cloudiq_storage_resource_pools_fba_provisioned_used gauge
    # HELP cloudiq_storage_resource_pools_fba_snapshot_effective_used_percent SRP capacity for FBA snapshot effective used percent.
    # TYPE cloudiq_storage_resource_pools_fba_snapshot_effective_used_percent gauge
    # HELP cloudiq_storage_resource_pools_fba_snapshot_physical_used_percent SRP capacity for FBA snapshot physical used percent.
    # TYPE cloudiq_storage_resource_pools_fba_snapshot_physical_used_percent gauge
    # HELP cloudiq_storage_resource_pools_fba_snapshot_resource_used SRP capacity for FBA snapshot resource used.
    # TYPE cloudiq_storage_resource_pools_fba_snapshot_resource_used gauge
    # HELP cloudiq_storage_resource_pools_free_snapshot_size The free Snapshot capacity.
    # TYPE cloudiq_storage_resource_pools_free_snapshot_size gauge
    # HELP cloudiq_storage_resource_pools_free_subscribed_size The free subscribe capacity.
    # TYPE cloudiq_storage_resource_pools_free_subscribed_size gauge
    # HELP cloudiq_storage_resource_pools_free_usable_size The free physical capacity.
    # TYPE cloudiq_storage_resource_pools_free_usable_size gauge
    # HELP cloudiq_storage_resource_pools_overall_efficiency The overall efficiency.
    # TYPE cloudiq_storage_resource_pools_overall_efficiency gauge
    # HELP cloudiq_storage_resource_pools_pattern_detection_savings SRP efficiency pattern detection.
    # TYPE cloudiq_storage_resource_pools_pattern_detection_savings gauge
    # HELP cloudiq_storage_resource_pools_reducible_data SRP efficiency reducible data.
    # TYPE cloudiq_storage_resource_pools_reducible_data gauge
    # HELP cloudiq_storage_resource_pools_reserved_capacity_percent Percentage of Data Reduction.
    # TYPE cloudiq_storage_resource_pools_reserved_capacity_percent gauge
    # HELP cloudiq_storage_resource_pools_snapshot_savings The snapshot savings.
    # TYPE cloudiq_storage_resource_pools_snapshot_savings gauge
    # HELP cloudiq_storage_resource_pools_thin_savings The thin savings.
    # TYPE cloudiq_storage_resource_pools_thin_savings gauge
    # HELP cloudiq_storage_resource_pools_total_snapshot_size The total Snapshot capacity.
    # TYPE cloudiq_storage_resource_pools_total_snapshot_size gauge
    # HELP cloudiq_storage_resource_pools_total_subscribed_size The total subscribe capacity.
    # TYPE cloudiq_storage_resource_pools_total_subscribed_size gauge
    # HELP cloudiq_storage_resource_pools_total_usable_size The total physical capacity.
    # TYPE cloudiq_storage_resource_pools_total_usable_size gauge
    # HELP cloudiq_storage_resource_pools_unreducible_data SRP efficiency unreduicible data.
    # TYPE cloudiq_storage_resource_pools_unreducible_data gauge
    # HELP cloudiq_storage_resource_pools_used_snapshot_percent Percentage of the subscribed capacity.
    # TYPE cloudiq_storage_resource_pools_used_snapshot_percent gauge
    # HELP cloudiq_storage_resource_pools_used_snapshot_size The used Snapshot capacity.
    # TYPE cloudiq_storage_resource_pools_used_snapshot_size gauge
    # HELP cloudiq_storage_resource_pools_used_usable_percent The used percentage of physical capacity.
    # TYPE cloudiq_storage_resource_pools_used_usable_percent gauge
    # HELP cloudiq_storage_resource_pools_used_usable_size The used physical capacity.
    # TYPE cloudiq_storage_resource_pools_used_usable_size gauge

  volumes:
    # HELP cloudiq_volumes_allocated_size The allocated size of the volume.
    # TYPE cloudiq_volumes_allocated_size gauge
    # HELP cloudiq_volumes_bandwidth The bandwidth consumed by the volume. Aggregated for a rolling average over the last 24 hours.
    # TYPE cloudiq_volumes_bandwidth gauge
    # HELP cloudiq_volumes_data_reduction_percent The data reduction percent for the volume.
    # TYPE cloudiq_volumes_data_reduction_percent gauge
    # HELP cloudiq_volumes_data_reduction_ratio The data reduction ratio for the volume.
    # TYPE cloudiq_volumes_data_reduction_ratio gauge
    # HELP cloudiq_volumes_data_reduction_saved_size The data reduction capacity saved for the volume.
    # TYPE cloudiq_volumes_data_reduction_saved_size gauge
    # HELP cloudiq_volumes_iops The IOPS for the volume. Aggregated for a rolling average over the last 24 hours.
    # TYPE cloudiq_volumes_iops gauge
    # HELP cloudiq_volumes_issue_count Number of health issues that are present on the volume.
    # TYPE cloudiq_volumes_issue_count gauge
    # HELP cloudiq_volumes_latency The latency for the volume. Aggregated for a rolling average over the last 24 hours.
    # TYPE cloudiq_volumes_latency gauge
    # HELP cloudiq_volumes_logical_size The logical size for the volume.
    # TYPE cloudiq_volumes_logical_size gauge
    # HELP cloudiq_volumes_snapshot_count The snapshot count for the volume.
    # TYPE cloudiq_volumes_snapshot_count gauge
    # HELP cloudiq_volumes_snapshot_size The snapshot size for the volume.
    # TYPE cloudiq_volumes_snapshot_size gauge
    # HELP cloudiq_volumes_total_size The total provisioned size of the volume.
    # TYPE cloudiq_volumes_total_size gauge
    # HELP cloudiq_volumes_used_size The used size of the volume.
    # TYPE cloudiq_volumes_used_size gauge
    # HELP cloudiq_volumes_used_size_unique The unique used size of the volume.
    # TYPE cloudiq_volumes_used_size_unique gauge

# Systems:
  network_systems:
    # HELP cloudiq_network_systems_bit_errors Number of bit errors across all ports on the system.
    # TYPE cloudiq_network_systems_bit_errors gauge
    # HELP cloudiq_network_systems_capacity_impact Impact point of highest impacting issue in the capacity health category.
    # TYPE cloudiq_network_systems_capacity_impact gauge
    # HELP cloudiq_network_systems_capacity_issue_count Total number of issues in the capacity health category.
    # TYPE cloudiq_network_systems_capacity_issue_count gauge
    # HELP cloudiq_network_systems_configuration_impact Impact point of highest impacting issue in the configuration health category.
    # TYPE cloudiq_network_systems_configuration_impact gauge
    # HELP cloudiq_network_systems_configuration_issue_count Total number of issues in the configuration health category.
    # TYPE cloudiq_network_systems_configuration_issue_count gauge
    # HELP cloudiq_network_systems_congested_ports Total number of congested ports on the switch.
    # TYPE cloudiq_network_systems_congested_ports gauge
    # HELP cloudiq_network_systems_cpu_utilization Amount of CPU usage.
    # TYPE cloudiq_network_systems_cpu_utilization gauge
    # HELP cloudiq_network_systems_data_protection_impact Impact point of highest impacting issue in the data protection health category.
    # TYPE cloudiq_network_systems_data_protection_impact gauge
    # HELP cloudiq_network_systems_data_protection_issue_count Total number of issues in the data protection health category.
    # TYPE cloudiq_network_systems_data_protection_issue_count gauge
    # HELP cloudiq_network_systems_error_fc_ports Number of FC ports with errors.
    # TYPE cloudiq_network_systems_error_fc_ports gauge
    # HELP cloudiq_network_systems_error_ge_ports Number of GE ports with errors.
    # TYPE cloudiq_network_systems_error_ge_ports gauge
    # HELP cloudiq_network_systems_error_ports Total number of ports with errors.
    # TYPE cloudiq_network_systems_error_ports gauge
    # HELP cloudiq_network_systems_health_issue_count Total amount of health issues.
    # TYPE cloudiq_network_systems_health_issue_count gauge
    # HELP cloudiq_network_systems_health_score Health score of the system.
    # TYPE cloudiq_network_systems_health_score gauge
    # HELP cloudiq_network_systems_incrementing_bit_errors Incrementing bit errors for the system.
    # TYPE cloudiq_network_systems_incrementing_bit_errors gauge
    # HELP cloudiq_network_systems_incrementing_link_resets Incrementing link resets for the system.
    # TYPE cloudiq_network_systems_incrementing_link_resets gauge
    # HELP cloudiq_network_systems_link_resets Number of link resets across all ports on the system.
    # TYPE cloudiq_network_systems_link_resets gauge
    # HELP cloudiq_network_systems_offline_fc_ports Total number of FC ports that are offline.
    # TYPE cloudiq_network_systems_offline_fc_ports gauge
    # HELP cloudiq_network_systems_offline_ge_ports Total number of GE ports that are offline.
    # TYPE cloudiq_network_systems_offline_ge_ports gauge
    # HELP cloudiq_network_systems_online_fc_ports Total number of FC ports that are online.
    # TYPE cloudiq_network_systems_online_fc_ports gauge
    # HELP cloudiq_network_systems_online_ge_ports Total number of GE ports that are online.
    # TYPE cloudiq_network_systems_online_ge_ports gauge
    # HELP cloudiq_network_systems_online_ports Total number of ports that are online.
    # TYPE cloudiq_network_systems_online_ports gauge
    # HELP cloudiq_network_systems_performance_impact Impact point of highest impacting issue in the performance health category.
    # TYPE cloudiq_network_systems_performance_impact gauge
    # HELP cloudiq_network_systems_performance_issue_count Total number of issues in the performance health category.
    # TYPE cloudiq_network_systems_performance_issue_count gauge
    # HELP cloudiq_network_systems_ports_over_80_percent Number of ports with over 80 percent utilization.
    # TYPE cloudiq_network_systems_ports_over_80_percent gauge
    # HELP cloudiq_network_systems_system_health_impact Health impact for the system.
    # TYPE cloudiq_network_systems_system_health_impact gauge
    # HELP cloudiq_network_systems_system_health_issue_count Total amount of health issues for the system.
    # TYPE cloudiq_network_systems_system_health_issue_count gauge
    # HELP cloudiq_network_systems_total_fc_ports Total number of FC ports on the system.
    # TYPE cloudiq_network_systems_total_fc_ports gauge
    # HELP cloudiq_network_systems_total_ge_ports Total number of GE ports on the system.
    # TYPE cloudiq_network_systems_total_ge_ports gauge
    # HELP cloudiq_network_systems_total_ports Total number of ports on the system.
    # TYPE cloudiq_network_systems_total_ports gauge
    # HELP cloudiq_network_systems_uptime Time since last reboot of the system.
    # TYPE cloudiq_network_systems_uptime gauge
    # HELP cloudiq_network_systems_utilization Overall bandwidth utilization of the system.
    # TYPE cloudiq_network_systems_utilization gauge

  server_systems:
    # HELP cloudiq_server_systems_capacity_impact Impact point of highest impacting issue in the capacity health category.
    # TYPE cloudiq_server_systems_capacity_impact gauge
    # HELP cloudiq_server_systems_capacity_issue_count Total number of issues in the capacity health category.
    # TYPE cloudiq_server_systems_capacity_issue_count gauge
    # HELP cloudiq_server_systems_configuration_impact Impact point of highest impacting issue in the configuration health category.
    # TYPE cloudiq_server_systems_configuration_impact gauge
    # HELP cloudiq_server_systems_configuration_issue_count Total number of issues in the configuration health category.
    # TYPE cloudiq_server_systems_configuration_issue_count gauge
    # HELP cloudiq_server_systems_cpu_usage_percent Percentage of CPU usage.
    # TYPE cloudiq_server_systems_cpu_usage_percent gauge
    # HELP cloudiq_server_systems_data_protection_impact Impact point of highest impacting issue in the data protection health category.
    # TYPE cloudiq_server_systems_data_protection_impact gauge
    # HELP cloudiq_server_systems_data_protection_issue_count Total number of issues in the data protection health category.
    # TYPE cloudiq_server_systems_data_protection_issue_count gauge
    # HELP cloudiq_server_systems_health_issue_count Total amount of health issues.
    # TYPE cloudiq_server_systems_health_issue_count gauge
    # HELP cloudiq_server_systems_health_score Health score of the system.
    # TYPE cloudiq_server_systems_health_score gauge
    # HELP cloudiq_server_systems_inlet_temperature Inlet temperature of a system. (Avg over last 24 hours)
    # TYPE cloudiq_server_systems_inlet_temperature gauge
    # HELP cloudiq_server_systems_memory_usage_percent Percentage of memory usage for the system.
    # TYPE cloudiq_server_systems_memory_usage_percent gauge
    # HELP cloudiq_server_systems_performance_impact Impact point of highest impacting issue in the performance health category.
    # TYPE cloudiq_server_systems_performance_impact gauge
    # HELP cloudiq_server_systems_performance_issue_count Total number of issues in the performance health category.
    # TYPE cloudiq_server_systems_performance_issue_count gauge
    # HELP cloudiq_server_systems_power_consumption Power consumed by the system. (Avg over last 24 hours)
    # TYPE cloudiq_server_systems_power_consumption gauge
    # HELP cloudiq_server_systems_system_board_io_usage_percent Percentage of I/O usage of the system board.
    # TYPE cloudiq_server_systems_system_board_io_usage_percent gauge
    # HELP cloudiq_server_systems_system_health_impact Health impact for the system.
    # TYPE cloudiq_server_systems_system_health_impact gauge
    # HELP cloudiq_server_systems_system_health_issue_count Total amount of health issues for the system.
    # TYPE cloudiq_server_systems_system_health_issue_count gauge
    # HELP cloudiq_server_systems_system_usage_percent Percentage of system use.
    # TYPE cloudiq_server_systems_system_usage_percent gauge

  storage_systems:
    # HELP cloudiq_storage_systems_bandwidth The system bandwidth. Aggregated for a rolling average over the last 24 hours.
    # TYPE cloudiq_storage_systems_bandwidth gauge
    # HELP cloudiq_storage_systems_capacity_impact Impact point of highest impacting issue in the capacity health category.
    # TYPE cloudiq_storage_systems_capacity_impact gauge
    # HELP cloudiq_storage_systems_capacity_issue_count Total number of issues in the capacity health category.
    # TYPE cloudiq_storage_systems_capacity_issue_count gauge
    # HELP cloudiq_storage_systems_compression_savings Storage efficiency ratio of data which has compression applied to it on the system.
    # TYPE cloudiq_storage_systems_compression_savings gauge
    # HELP cloudiq_storage_systems_configuration_impact Impact point of highest impacting issue in the configuration health category.
    # TYPE cloudiq_storage_systems_configuration_impact gauge
    # HELP cloudiq_storage_systems_configuration_issue_count Total number of issues in the configuration health category.
    # TYPE cloudiq_storage_systems_configuration_issue_count gauge
    # HELP cloudiq_storage_systems_configured_size The configured size for this system.
    # TYPE cloudiq_storage_systems_configured_size gauge
    # HELP cloudiq_storage_systems_data_protection_impact Impact point of highest impacting issue in the data protection health category.
    # TYPE cloudiq_storage_systems_data_protection_impact gauge
    # HELP cloudiq_storage_systems_data_protection_issue_count Total number of issues in the data protection health category.
    # TYPE cloudiq_storage_systems_data_protection_issue_count gauge
    # HELP cloudiq_storage_systems_free_percent Free capacity in percent.
    # TYPE cloudiq_storage_systems_free_percent gauge
    # HELP cloudiq_storage_systems_free_size Free size.
    # TYPE cloudiq_storage_systems_free_size gauge
    # HELP cloudiq_storage_systems_health_issue_count Total amount of health issues.
    # TYPE cloudiq_storage_systems_health_issue_count gauge
    # HELP cloudiq_storage_systems_health_score The overall health score of the system.
    # TYPE cloudiq_storage_systems_health_score gauge
    # HELP cloudiq_storage_systems_iops The IOPS for the system. Aggregated for a rolling average over the last 24 hours.
    # TYPE cloudiq_storage_systems_iops gauge
    # HELP cloudiq_storage_systems_latency The latency for the system. Aggregated for a rolling average over the last 24 hours.
    # TYPE cloudiq_storage_systems_latency gauge
    # HELP cloudiq_storage_systems_logical_size The logical size written.
    # TYPE cloudiq_storage_systems_logical_size gauge
    # HELP cloudiq_storage_systems_overall_efficiency The overall system-level storage efficiency ratio based on Thin, Snapshots, Deduplication, and Data Reduction.
    # TYPE cloudiq_storage_systems_overall_efficiency gauge
    # HELP cloudiq_storage_systems_performance_impact Impact point of highest impacting issue in the performance health category.
    # TYPE cloudiq_storage_systems_performance_impact gauge
    # HELP cloudiq_storage_systems_performance_issue_count Total number of issues in the performance health category.
    # TYPE cloudiq_storage_systems_performance_issue_count gauge
    # HELP cloudiq_storage_systems_snaps_savings The snaps savings for this system.
    # TYPE cloudiq_storage_systems_snaps_savings gauge
    # HELP cloudiq_storage_systems_system_health_impact Health impact for the system.
    # TYPE cloudiq_storage_systems_system_health_impact gauge
    # HELP cloudiq_storage_systems_system_health_issue_count Total amount of health issues for the system.
    # TYPE cloudiq_storage_systems_system_health_issue_count gauge
    # HELP cloudiq_storage_systems_thin_savings The savings due to thin provisioning.
    # TYPE cloudiq_storage_systems_thin_savings gauge
    # HELP cloudiq_storage_systems_total_size The total size of the system.
    # TYPE cloudiq_storage_systems_total_size gauge
    # HELP cloudiq_storage_systems_unconfigured_size The unconfigured capacity for this system.
    # TYPE cloudiq_storage_systems_unconfigured_size gauge
    # HELP cloudiq_storage_systems_used_percent Percentage of capacity used for this system.
    # TYPE cloudiq_storage_systems_used_percent gauge
    # HELP cloudiq_storage_systems_used_size The value of used capacity for this system.
    # TYPE cloudiq_storage_systems_used_size gauge
```

# References
- https://cloudiq.emc.com/
- API Docs: https://developer.dell.com/apis/d1d6171c-cf6b-49c8-a3de-7994b6069d1a/versions/v1/docs/01-Introduction.md
