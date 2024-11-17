import argparse
from proxmoxer import ProxmoxAPI
from rich.table import Table
from rich.console import Console
from getpass import getpass
import json

class ProxmoxManager:
    def __init__(self, host, user, password, verify_ssl=False):
        self.proxmox = ProxmoxAPI(host, user=user, password=password, verify_ssl=verify_ssl)
    
    def _get_nodes(self):
        return self.proxmox.nodes.get()
    
    def _get_vm_ip(self, node_name, vm_id):
        try:
            vm_status = self.proxmox.nodes(node_name).qemu(vm_id).agent('network-get-interfaces').get()
            ips = []
            for interface in vm_status['result']:
                for ip_data in interface.get('ip-addresses', []):
                    ip_address = ip_data.get('ip-address')
                    if ip_address and ':' not in ip_address:  # Skip IPv6 addresses
                        if ip_address != "127.0.0.1" and ip_address != "0.0.0.0": # Skip loopback and local IP addresses
                            ips.append(ip_address)
            return ips
        except Exception:
            return ['']

    def _get_container_ip(self, node_name, container_id):
        try:
            config = self.proxmox.nodes(node_name).lxc(container_id).config.get()
            ips = []
            for key, value in config.items():
                if key.startswith('net') and 'ip' in value:
                    ip_info = value.split(',')
                    for entry in ip_info:
                        if entry.startswith('ip='):
                            ip_address = entry.split('=')[1]
                            if '/' in ip_address:  # Remove the CIDR notation if present
                                ip_address = ip_address.split('/')[0]
                            ips.append(ip_address)
            return ips
        except Exception:
            return ['']

    def get_objects_ips(self):
        object_ips = {}
        nodes = self._get_nodes()

        for node in nodes:
            node_name = node['node']

            # Fetch VMs and their IPs
            vms = self.proxmox.nodes(node_name).qemu.get()
            for vm in vms:
                vm_id = vm['vmid']
                object_ips[vm['name']] = {}
                object_ips[vm['name']]['ips'] = self._get_vm_ip(node_name, vm_id)
                object_ips[vm['name']]['type'] = 'vm'
                object_ips[vm['name']]['id'] = vm_id


            # Fetch Containers and their IPs
            containers = self.proxmox.nodes(node_name).lxc.get()
            for container in containers:
                container_id = container['vmid']
                object_ips[container['name']] = {}
                object_ips[container['name']]['ips'] = self._get_container_ip(node_name, container_id)
                object_ips[container['name']]['type'] = 'container'
                object_ips[container['name']]['id'] = container_id

        return object_ips

def get_password():
    return getpass("Enter your Proxmox password: ")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Proxmox VM and Container IP Fetcher")
    parser.add_argument("-s", "--server", required=True, help="Proxmox host address")
    parser.add_argument("-u", "--user", required=False, default="root@pam", help="Proxmox username (default: root@pam)")
    parser.add_argument("-p", "--password", help="Proxmox password (if not provided, will prompt interactively)")
    parser.add_argument("-o", "--output", help="Save collected data to a JSON file")
    output_format = parser.add_mutually_exclusive_group()
    output_format.add_argument("-a", "--array", action="store_true", help="Print as an array")
    output_format.add_argument("-j", "--jq", action="store_true", default=True, help="Print as JQ compatible JSON")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    proxmox_server = args.server
    user = args.user
    password = args.password if args.password else get_password()

    manager = ProxmoxManager(proxmox_server, user, password)
    
    object_ips = manager.get_objects_ips()
    if args.output:
        with open(args.output, 'w') as outfile:
            json.dump(object_ips, outfile, indent=4)

    if args.array:
        # Create table headers
        table_data = [["Name", "IPs", "Type", "ID"]]
        
        # Add data rows sorted by ID
        sorted_items = sorted(object_ips.items(), key=lambda x: x[1]['id'])
        for name, details in sorted_items:
            ips_str = ",".join(details['ips'])
            table_data.append([
                name,
                ips_str,
                details['type'],
                str(details['id'])
            ])

        table = Table()
        table.add_column("Name")
        table.add_column("IPs") 
        table.add_column("Type")
        table.add_column("ID")
        
        for row in table_data[1:]:
            table.add_row(*row)
            
        console = Console()
        console.print(table)
    else:
        print(json.dumps(object_ips, indent=4, separators=(',', ':')))
