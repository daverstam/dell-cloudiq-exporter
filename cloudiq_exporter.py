#!/usr/bin/env python

import string
import requests
import yaml
import time
import json
import datetime
from operator import itemgetter
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class CloudiqConnection(object):
    def __init__(self):
        self.cloudiq_base_url = cfg['cloudiq_base_url']
        self.cloudiq_token_url = cfg['cloudiq_token_url']
        self.cloudiq_client_id = cfg['cloudiq_client_id']
        self.cloudiq_client_secret = cfg['cloudiq_client_secret']

    def request_api_token(self):
        data = {'grant_type': 'client_credentials',
                 'client_id': self.cloudiq_client_id,
                 'client_secret': self.cloudiq_client_secret}

        cloudiq_token_request = requests.post(self.cloudiq_token_url, data).json()
        cloudiq_token = cloudiq_token_request

        return cloudiq_token

class CloudiqMetrics(object):
    def __init__(self):
        self.cloudiq_base_url = cfg['cloudiq_base_url']
        self.cloudiq_token = ''

    def request_metrics(self, metric_url: string):
        if not self.cloudiq_token:
            self.cloudiq_token_data = CloudiqConnection().request_api_token()
            self.cloudiq_token = self.cloudiq_token_data['access_token']
            self.cloudiq_token_expiration = self.cloudiq_token_data['expires_in']
            self.cloudiq_token_creation_time = datetime.datetime.now()
        elif self.cloudiq_token:
            if datetime.datetime.now() > (self.cloudiq_token_creation_time + datetime.timedelta(seconds=self.cloudiq_token_expiration) - datetime.timedelta(minutes=10)):
                self.cloudiq_token_data = CloudiqConnection().request_api_token()
                self.cloudiq_token = self.cloudiq_token_data['access_token']
                self.cloudiq_token_expiration = self.cloudiq_token_data['expires_in']
                self.cloudiq_token_creation_time = datetime.datetime.now()

        headers = {'Authorization': f'Bearer {self.cloudiq_token}'}
        cloudiq_metric_request = requests.get(self.cloudiq_base_url + metric_url, headers=headers)

        return cloudiq_metric_request

    def request_live_metrics(self, resource_type: string, system_id: list, metric_name: string):
        if not self.cloudiq_token:
            self.cloudiq_token_data = CloudiqConnection().request_api_token()
            self.cloudiq_token = self.cloudiq_token_data['access_token']
            self.cloudiq_token_expiration = self.cloudiq_token_data['expires_in']
            self.cloudiq_token_creation_time = datetime.datetime.now()
        elif self.cloudiq_token:
            if datetime.datetime.now() > (self.cloudiq_token_creation_time + datetime.timedelta(seconds=self.cloudiq_token_expiration) - datetime.timedelta(minutes=10)):
                self.cloudiq_token_data = CloudiqConnection().request_api_token()
                self.cloudiq_token = self.cloudiq_token_data['access_token']
                self.cloudiq_token_expiration = self.cloudiq_token_data['expires_in']
                self.cloudiq_token_creation_time = datetime.datetime.now()

        metrics_url = '/rest/v1/metrics/query'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.cloudiq_token}'
        }
        body = {
            "resource_type": resource_type,
            "ids": system_id,
            "metrics": [
                f"{metric_name}"
            ],
            "interval": "PT5M",
        }
        cloudiq_live_metric_request = requests.post(self.cloudiq_base_url + metrics_url, headers=headers, data=json.dumps(body))

        return cloudiq_live_metric_request

    def collect(self):
        for k, v in cfg['metrics'].items():
            if v['collect'] is True:
                """
                HARDWARE
                """
                #
                # Ports
                #
                if k == 'ports':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'info': 'Info about ports.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'object_type',
                                'system_model',
                                'system_name',
                                'type',
                                'wwn_or_mac_address'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                object_type = i['object_type']
                                system_model = i['system_model']
                                system_name = i['system_name']
                                type_label = i['type']
                                wwn_or_mac_address = i['wwn_or_mac_address']
                                val = '1'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    object_type,
                                    system_model,
                                    system_name,
                                    type_label,
                                    wwn_or_mac_address
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Datastores
                #
                if k == 'datastores':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'info': 'Info about datastores.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'object_type',
                                'export_path',
                                'type'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                object_type = i['object_type']
                                export_path = i['export_path']
                                type_label = i['type']
                                val = '1'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    object_type,
                                    export_path,
                                    type_label
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                """
                STORAGE
                """
                #
                # Drives
                #
                if k == 'drives':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'endurance_percent': 'Percentage of write endurance left, based on specified maximum write endurance of drive.',
                        'free_size': 'Free Size of the drive.',
                        'issue_count': 'Number of health issues that are present on the drive.',
                        'used_size': 'Used Size of the drive.',
                        'size': 'Size of the drive.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'serial_number'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                serial_number = i['serial_number']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    serial_number
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Filesystems
                #
                if k == 'filesystems':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'allocated_size': 'The allocated size of the file system.',
                        'data_reduction_percent': 'The data reduction percent for the file system.',
                        'data_reduction_ratio': 'The data reduction ratio for the file system.',
                        'data_reduction_saved_size': 'The data reduction saved size for the file system.',
                        'issue_count': 'Number of health issues that are present on the file system.',
                        'total_size': 'The total size of the file system.',
                        'used_percent': 'Percentage used for the file system.',
                        'used_size': 'Size used for the file system.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Hosts
                #
                if k == 'hosts':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'issue_count': 'Number of health issues that are present on the host or server.',
                        'total_size': 'Total size of all LUNs or Volumes that are provisioned to the host or server from the system.',
                        'initiator_count': 'Number of initiators that are connected between the host or server and the monitored system.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'operating_system',
                                'system_model',
                                'system_name'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                operating_system = i['operating_system']
                                system_model = i['system_model']
                                system_name = i['system_name']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    operating_system,
                                    system_model,
                                    system_name
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Pools
                #
                if k == 'pools':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'free_size': 'Available capacity.',
                        'issue_count': 'Number of health issues that are present on the pool.',
                        'subscribed_percent': 'Percentage of pool capacity that is provisioned.',
                        'subscribed_size': 'Total subscribed capacity of the pool.',
                        'total_size': 'Total capacity of the pool.',
                        'used_percent': 'Percentage of pool capacity that is being used.',
                        'used_size': 'Capacity of the pool that is being used.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'system_model',
                                'system_name'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                system_model = i['system_model']
                                system_name = i['system_name']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    system_model,
                                    system_name
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Storage Groups
                #
                if k == 'storage_groups':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'allocated_size': 'The allocated capacity.',
                        'compressionratio': 'The Compression ratio for the SG.',
                        'compression_saved_percent': 'The compression percent.',
                        'data_reduction_ratio': 'Storage group efficiency data reduction ratio.',
                        'effective_used': 'Storage group capacity effective used.',
                        'free_size': 'The free subscribe capacity.',
                        'masking_view_count': 'Masking views.',
                        'physical_used': 'Storage group capacity physical used.',
                        'provisioned': 'Storage group capacity provisioned.',
                        'snaphot_physical_used': 'Storage group efficiency snapshot physical used.',
                        'snapshot_count': 'The total number of Snapshots associated with the SG.',
                        'snapshot_drr_ratio': 'Storage group efficiency snapshot data reduction ratio.',
                        'snapshot_effective_used': 'Storage group efficiency snapshot effective used.',
                        'snapshot_resources_percent': 'Storage group efficiency snapshot resources percent.',
                        'subscribed_size': 'The total Subscribe capacity.',
                        'total_size': 'The Total capacity.',
                        'unreducible_data': 'Storage group efficiency unreducible data.',
                        'volume_count': 'The total number of Volumes associated with the SG.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Storage Resource Pools
                #
                if k == 'storage_resource_pools':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'allocated_subscribed_percent': 'Percentage of the subscribed capacity.',
                        'allocated_subscribed_size': 'The used subscribe capacity.',
                        'ckd_data_reduction_data_reducing_percent': 'SRP capacity for CKD data reduction percent.',
                        'ckd_data_reduction_effective_used_data_reduction_disabled': 'SRP Capacity for CKD data reduction effective used data reduction disabled.',
                        'ckd_data_reduction_effective_used_enabled_and_reducing': 'SRP capacity for CKD data reduction effective used enabled and reducing.',
                        'ckd_data_reduction_effective_used_enabled_and_unevaluated': 'SRP capacity for CKD data reduction effective used enabled and unevaluated.',
                        'ckd_data_reduction_effective_used_enabled_and_unreducible': 'SRP capacity for CKD A data reduction effective used enabled and unreducible.',
                        'ckd_data_reduction_physical_used_data_reduction_disabled': 'SRP capacity for CKD data reduction physical used data reduction disabled.',
                        'ckd_data_reduction_physical_used_enabled_and_reducing': 'SRP capacity for CKD data reduction physical used enabled and reducing.',
                        'ckd_data_reduction_physical_used_enabled_and_unevaluated': 'SRP capacity for CKD data reduction physical used enabled and unevaluated.',
                        'ckd_data_reduction_physical_used_enabled_and_unreducible': 'SRP capacity for CKD data reduction physical used enabled and unreducible.',
                        'ckd_data_reduction_ratio_to_one': 'SRP capacity for CKD data reduction ratio to one.',
                        'ckd_data_reduction_savings': 'SRP capacity for CKD data reduction savings.',
                        'ckd_effective_capacity_resources_free': 'SRP Capacity for CKD effective capacity resources free.',
                        'ckd_effective_capacity_resources_total': 'SRP capacity for CKD effective capacity resources total.',
                        'ckd_effective_capacity_resources_used': 'SRP capacity for CKD effective capacity resources used.',
                        'ckd_effective_capacity_usage_free': 'SRP capacity for CKD effective capacity usage free.',
                        'ckd_effective_capacity_usage_snapshot_used': 'SRP capacity for CKD effective capacity usage snapshots used.',
                        'ckd_effective_capacity_usage_user_used': 'SRP capacity for CKD effective capacity usage user used.',
                        'ckd_effective_free': 'SRP capacity for CKD effective free.',
                        'ckd_effective_physical_free': 'SRP capacity for CKD effective physical free.',
                        'ckd_effective_physical_target': 'SRP capacity for CKD effective physical target.',
                        'ckd_effective_physical_total': 'SRP capacity for CKD effective physical total.',
                        'ckd_effective_physical_used': 'SRP capacity for CKD-FBCKD A effective physical used.',
                        'ckd_effective_target': 'SRP capacity for CKD-FCKD BA effective target.',
                        'ckd_effective_total': 'SRP capacity for CKD effective total.',
                        'ckd_effective_used': 'SRP capacity for CKD effective used.',
                        'ckd_effective_used_percent': 'SRP capacity for CKD effective used percent.',
                        'ckd_provisioned_effective': 'SRP capacity for CKD provisioned effective.',
                        'ckd_provisioned_provisioned_percent': 'SRP capacity for CKD provisioned percent.',
                        'ckd_provisioned_used': 'SRP capacity for CKD provisioned used.',
                        'ckd_snapshot_effective_used_percent': 'SRP capacity for CKD snapshot effective used percent.',
                        'ckd_snapshot_physical_used_percent': 'SRP capacity for CKD snapshot physical used percent.',
                        'ckd_snapshot_resource_used': 'SRP capacity for CKD snapshot resource used.',
                        'collection_timestamp': 'Last time when the configuration data has been collected.',
                        'data_reduction_enabled_percent': 'The Data reduction percent.',
                        'data_reduction_savings': 'The Data reduction ratio.',
                        'deduplication_and_compression_savings': 'SRP efficiency deduplication and compression.',
                        'drr_on_reducible_only_to_one': 'SRP efficiency DDR on reducible.',
                        'effective_capacity': 'The Effective Capacity used on the Storage Resource Pool.',
                        'fba_data_reduction_data_reducing_percent': 'SRP capacity for FBA data reducing percent.',
                        'fba_data_reduction_effective_used_data_reduction_disabled': 'SRP capacity for FBA data reduction effective used data reduction disabled.',
                        'fba_data_reduction_effective_used_enabled_and_reducing': 'SRP capacity for FBA data reduction effective used enabled and reducing.',
                        'fba_data_reduction_effective_used_enabled_and_unevaluated': 'SRP capacity for FBA data reduction effective used enabled and unevaluated.',
                        'fba_data_reduction_effective_used_enabled_and_unreducible': 'SRP capacity for FBA data reduction effective used enabled and unreducible.',
                        'fba_data_reduction_physical_used_data_reduction_disabled': 'SRP Capacity for FBA data reduction physical used data reduction disabled.',
                        'fba_data_reduction_physical_used_enabled_and_reducing': 'SRP capacity for FBA data reduction physical used enabled and reducing.',
                        'fba_data_reduction_physical_used_enabled_and_unevaluated': 'SRP capacity for FBA data reduction physical used enabled and unevaluated.',
                        'fba_data_reduction_physical_used_enabled_and_unreducible': 'SRP capacity for FBA data reduction physical used enabled and unreducible.',
                        'fba_data_reduction_ratio_to_one': 'SRP capacity for FBA data reduction ratio to one.',
                        'fba_data_reduction_savings': 'SRP capacity for FBA data reduction savings.',
                        'fba_effective_capacity_resources_free': 'SRP capacity for FBA effective capacity resources free.',
                        'fba_effective_capacity_resources_total': 'SRP capacity for FBA effective capacity resources total.',
                        'fba_effective_capacity_resources_used': 'SRP capacity for FBA effective capacity resources used.',
                        'fba_effective_capacity_usage_free': 'SRP capacity for FBA effective capacity usage free.',
                        'fba_effective_capacity_usage_snapshot_used': 'SRP capacity for FBA effective capacity usage snapshots used.',
                        'fba_effective_capacity_usage_user_used': 'SRP capacity for FBA effective capacity usage user used.',
                        'fba_effective_free': 'SRP capacity for FBA effective free.',
                        'fba_effective_physical_free': 'SRP capacity for FBA effective physical free.',
                        'fba_effective_physical_target': 'SRP capacity for FBA effective physical target.',
                        'fba_effective_physical_total': 'SRP capacity for FBA effective physical total.',
                        'fba_effective_physical_used': 'SRP capacity for FBA effective physical used.',
                        'fba_effective_target': 'SRP capacity for FBA effective target.',
                        'fba_effective_total': 'SRP capacity for FBA effective total.',
                        'fba_effective_used': 'SRP capacity for FBA effective used.',
                        'fba_effective_used_percent': 'SRP capacity for FBA effective used percent.',
                        'fba_provisioned_effective': 'SRP capacity for FBA provisioned effective.',
                        'fba_provisioned_provisioned_percent': 'SRP capacity for FBA provisioned percent.',
                        'fba_provisioned_used': 'SRP capacity for FBA provisioned used.',
                        'fba_snapshot_effective_used_percent': 'SRP capacity for FBA snapshot effective used percent.',
                        'fba_snapshot_physical_used_percent': 'SRP capacity for FBA snapshot physical used percent.',
                        'fba_snapshot_resource_used': 'SRP capacity for FBA snapshot resource used.',
                        'free_snapshot_size': 'The free Snapshot capacity.',
                        'free_subscribed_size': 'The free subscribe capacity.',
                        'free_usable_size': 'The free physical capacity.',
                        'overall_efficiency': 'The overall efficiency.',
                        'pattern_detection_savings': 'SRP efficiency pattern detection.',
                        'reducible_data': 'SRP efficiency reducible data.',
                        'reserved_capacity_percent': 'Percentage of Data Reduction.',
                        'snapshot_savings': 'The snapshot savings.',
                        'thin_savings': 'The thin savings.',
                        'total_snapshot_size': 'The total Snapshot capacity.',
                        'total_subscribed_size': 'The total subscribe capacity.',
                        'total_usable_size': 'The total physical capacity.',
                        'unreducible_data': 'SRP efficiency unreduicible data.',
                        'used_snapshot_percent': 'Percentage of the subscribed capacity.',
                        'used_snapshot_size': 'The used Snapshot capacity.',
                        'used_usable_percent': 'The used percentage of physical capacity.',
                        'used_usable_size': 'The used physical capacity.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Volumes
                #
                if k == 'volumes':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'allocated_size': 'The allocated size of the volume.',
                        'bandwidth': 'The bandwidth consumed by the volume. Aggregated for a rolling average over the last 24 hours.',
                        'data_reduction_percent': 'The data reduction percent for the volume.',
                        'data_reduction_ratio': 'The data reduction ratio for the volume.',
                        'data_reduction_saved_size': 'The data reduction capacity saved for the volume.',
                        'iops': 'The IOPS for the volume. Aggregated for a rolling average over the last 24 hours.',
                        'issue_count': 'Number of health issues that are present on the volume.',
                        'latency': 'The latency for the volume. Aggregated for a rolling average over the last 24 hours.',
                        'logical_size': 'The logical size for the volume.',
                        'snapshot_count': 'The snapshot count for the volume.',
                        'snapshot_size': 'The snapshot size for the volume.',
                        'total_size': 'The total provisioned size of the volume.',
                        'used_size': 'The used size of the volume.',
                        'used_size_unique': 'The unique used size of the volume.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'pool_id'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                pool_id = i['pool_id']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    pool_id
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                """
                SYSTEMS
                """
                #
                # Network Systems
                #
                if k == 'network_systems':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'bit_errors': 'Number of bit errors across all ports on the system.',
                        'capacity_impact': 'Impact point of highest impacting issue in the capacity health category.',
                        'capacity_issue_count': 'Total number of issues in the capacity health category.',
                        'configuration_impact': 'Impact point of highest impacting issue in the configuration health category.',
                        'configuration_issue_count': 'Total number of issues in the configuration health category.',
                        'congested_ports': 'Total number of congested ports on the switch.',
                        'cpu_utilization': 'Amount of CPU usage.',
                        'data_protection_impact': 'Impact point of highest impacting issue in the data protection health category.',
                        'data_protection_issue_count': 'Total number of issues in the data protection health category.',
                        'error_fc_ports': 'Number of FC ports with errors.',
                        'error_ge_ports': 'Number of GE ports with errors.',
                        'error_ports': 'Total number of ports with errors.',
                        'health_issue_count': 'Total amount of health issues.',
                        'health_score': 'Health score of the system.',
                        'incrementing_bit_errors': 'Incrementing bit errors for the system.',
                        'incrementing_link_resets': 'Incrementing link resets for the system.',
                        'link_resets': 'Number of link resets across all ports on the system.',
                        'offline_fc_ports': 'Total number of FC ports that are offline.',
                        'offline_ge_ports': 'Total number of GE ports that are offline.',
                        'online_fc_ports': 'Total number of FC ports that are online.',
                        'online_ge_ports': 'Total number of GE ports that are online.',
                        'online_ports': 'Total number of ports that are online.',
                        'performance_impact': 'Impact point of highest impacting issue in the performance health category.',
                        'performance_issue_count': 'Total number of issues in the performance health category.',
                        'ports_over_80_percent': 'Number of ports with over 80 percent utilization.',
                        'system_health_impact': 'Health impact for the system.',
                        'system_health_issue_count': 'Total amount of health issues for the system.',
                        'total_fc_ports': 'Total number of FC ports on the system.',
                        'total_ge_ports': 'Total number of GE ports on the system.',
                        'total_ports': 'Total number of ports on the system.',
                        'uptime': 'Time since last reboot of the system.',
                        'utilization': 'Overall bandwidth utilization of the system.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'city',
                                'country',
                                'location',
                                'model',
                                'site_name',
                                'type',
                                'version'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                city = i['city']
                                country = i['country']
                                location = i['location']
                                model = i['model']
                                site_name = i['site_name']
                                type_label = i['type']
                                version = i['version']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    city,
                                    country,
                                    location,
                                    model,
                                    site_name,
                                    type_label,
                                    version
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Server Systems
                #
                if k == 'server_systems':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'capacity_impact': 'Impact point of highest impacting issue in the capacity health category.',
                        'capacity_issue_count': 'Total number of issues in the capacity health category.',
                        'configuration_impact': 'Impact point of highest impacting issue in the configuration health category.',
                        'configuration_issue_count': 'Total number of issues in the configuration health category.',
                        'cpu_usage_percent': 'Percentage of CPU usage.',
                        'data_protection_impact': 'Impact point of highest impacting issue in the data protection health category.',
                        'data_protection_issue_count': 'Total number of issues in the data protection health category.',
                        'health_issue_count': 'Total amount of health issues.',
                        'health_score': 'Health score of the system.',
                        'inlet_temperature': 'Inlet temperature of a system. (Avg over last 24 hours)',
                        'memory_usage_percent': 'Percentage of memory usage for the system.',
                        'performance_impact': 'Impact point of highest impacting issue in the performance health category.',
                        'performance_issue_count': 'Total number of issues in the performance health category.',
                        'power_consumption': 'Power consumed by the system. (Avg over last 24 hours)',
                        'system_board_io_usage_percent': 'Percentage of I/O usage of the system board.',
                        'system_health_impact': 'Health impact for the system.',
                        'system_health_issue_count': 'Total amount of health issues for the system.',
                        'system_usage_percent': 'Percentage of system use.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'city',
                                'country',
                                'location',
                                'model',
                                'site_name',
                                'type',
                                'version'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                city = i['city']
                                country = i['country']
                                location = i['location']
                                model = i['model']
                                site_name = i['site_name']
                                type_label = i['type']
                                version = i['version']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    city,
                                    country,
                                    location,
                                    model,
                                    site_name,
                                    type_label,
                                    version
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                #
                # Storage Systems
                #
                if k == 'storage_systems':
                    metrics_data = json.loads(self.request_metrics(v['url']).content)
                    metrics_to_export = {
                        'bandwidth': 'The system bandwidth. Aggregated for a rolling average over the last 24 hours.',
                        'capacity_impact': 'Impact point of highest impacting issue in the capacity health category.',
                        'capacity_issue_count': 'Total number of issues in the capacity health category.',
                        'compression_savings': 'Storage efficiency ratio of data which has compression applied to it on the system.',
                        'configuration_impact': 'Impact point of highest impacting issue in the configuration health category.',
                        'configuration_issue_count': 'Total number of issues in the configuration health category.',
                        'configured_size': 'The configured size for this system.',
                        'data_protection_impact': 'Impact point of highest impacting issue in the data protection health category.',
                        'data_protection_issue_count': 'Total number of issues in the data protection health category.',
                        'free_percent': 'Free capacity in percent.',
                        'free_size': 'Free size.',
                        'health_issue_count': 'Total amount of health issues.',
                        'health_score': 'The overall health score of the system.',
                        'iops': 'The IOPS for the system. Aggregated for a rolling average over the last 24 hours.',
                        'latency': 'The latency for the system. Aggregated for a rolling average over the last 24 hours.',
                        'logical_size': 'The logical size written.',
                        'overall_efficiency': 'The overall system-level storage efficiency ratio based on Thin, Snapshots, Deduplication, and Data Reduction.',
                        'performance_impact': 'Impact point of highest impacting issue in the performance health category.',
                        'performance_issue_count': 'Total number of issues in the performance health category.',
                        'snaps_savings': 'The snaps savings for this system.',
                        'system_health_impact': 'Health impact for the system.',
                        'system_health_issue_count': 'Total amount of health issues for the system.',
                        'thin_savings': 'The savings due to thin provisioning.',
                        'total_size': 'The total size of the system.',
                        'unconfigured_size': 'The unconfigured capacity for this system.',
                        'used_percent': 'Percentage of capacity used for this system.',
                        'used_size': 'The value of used capacity for this system.'
                    }
                    for metric_name, metric_help in metrics_to_export.items():
                        metrics = GaugeMetricFamily(
                            f'cloudiq_{k}_{metric_name}',
                            f'{metric_help}',
                            labels = [
                                'id',
                                'object_name',
                                'city',
                                'country',
                                'location',
                                'model',
                                'site_name',
                                'type',
                                'version'
                            ]
                        )

                        for i in metrics_data['results']:
                            try:
                                id = i['id']
                                object_name = i['object_name']
                                city = i['city']
                                country = i['country']
                                location = i['location']
                                model = i['model']
                                site_name = i['site_name']
                                type_label = i['type']
                                version = i['version']
                                if i[f'{metric_name}']:
                                    val = i[f'{metric_name}']
                                else:
                                    val = '0'
                                metrics.add_metric([
                                    id,
                                    object_name,
                                    city,
                                    country,
                                    location,
                                    model,
                                    site_name,
                                    type_label,
                                    version
                                    ], val)
                            except KeyError:
                                pass

                        yield metrics

                    if v['collect_live_metrics'] is True:
                        live_metrics_to_export = {
                            'bandwidth': 'Amount of data transferred in bytes per second.',
                            'iops': 'Number of operations per second.',
                            'latency': 'Latency of the resource, in microseconds (also known as response time).'
                        }
                        live_metric_nodes = []

                        for i in metrics_data['results']:
                            live_metric_nodes.append(i['id'])

                        for metric_name, metric_help in live_metrics_to_export.items():
                            live_metric_data = json.loads(self.request_live_metrics('storage_system', live_metric_nodes, metric_name).content)
                            sorted_live_metric_data = sorted(live_metric_data['results'], key=itemgetter('id'))
                            sorted_metrics_data = sorted(metrics_data['results'], key=itemgetter('id'))
                            metrics = GaugeMetricFamily(
                                f'cloudiq_{k}_live_metric_{metric_name}',
                                f'{metric_help}',
                                labels = [
                                    'id',
                                    'object_name',
                                    'city',
                                    'country',
                                    'location',
                                    'model',
                                    'site_name',
                                    'type',
                                    'version'
                                ]
                            )
                            for (i, d) in zip(sorted_live_metric_data, sorted_metrics_data):
                                try:
                                    if i['id'] == d['id']:
                                        id = i['id']
                                        object_name = d['object_name']
                                        city = d['city']
                                        country = d['country']
                                        location = d['location']
                                        model = d['model']
                                        site_name = d['site_name']
                                        type_label = d['type']
                                        version = d['version']
                                    try:
                                        val = i['timestamps'][0]['values'][0]
                                    except IndexError:
                                        val = '0'
                                    metrics.add_metric([
                                        id,
                                        object_name,
                                        city,
                                        country,
                                        location,
                                        model,
                                        site_name,
                                        type_label,
                                        version
                                        ], val)
                                except KeyError:
                                    pass

                            yield metrics

if __name__ == '__main__':
    with open('./config.yml', 'r') as config:
        cfg = yaml.safe_load(config)

    REGISTRY.register(CloudiqMetrics())
    start_http_server(cfg['exporter_listening_port'])
    while True: time.sleep(1)