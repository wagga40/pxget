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
            macs = []
            for interface in vm_status['result']:
                mac = interface.get('hardware-address', '')
                if mac:
                    macs.append(mac)
                for ip_data in interface.get('ip-addresses', []):
                    ip_address = ip_data.get('ip-address')
                    if ip_address and ':' not in ip_address:  # Skip IPv6 addresses
                        if ip_address != "127.0.0.1" and ip_address != "0.0.0.0": # Skip loopback and local IP addresses
                            ips.append(ip_address)
            return ips, macs
        except Exception:
            return [''], ['']

    def _get_container_ip(self, node_name, container_id):
        try:
            config = self.proxmox.nodes(node_name).lxc(container_id).config.get()
            ips = []
            macs = []
            for key, value in config.items():
                if key.startswith('net'):
                    if 'ip' in value:
                        ip_info = value.split(',')
                        for entry in ip_info:
                            if entry.startswith('ip='):
                                ip_address = entry.split('=')[1]
                                if '/' in ip_address:  # Remove the CIDR notation if present
                                    ip_address = ip_address.split('/')[0]
                                ips.append(ip_address)
                    if 'hwaddr' in value:
                        mac_info = value.split(',')
                        for entry in mac_info:
                            if entry.startswith('hwaddr='):
                                mac_address = entry.split('=')[1]
                                macs.append(mac_address)
            return ips, macs
        except Exception:
            return [''], ['']

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
                ips, macs = self._get_vm_ip(node_name, vm_id)
                object_ips[vm['name']]['ips'] = ips
                object_ips[vm['name']]['macs'] = macs
                object_ips[vm['name']]['type'] = 'vm'
                object_ips[vm['name']]['id'] = vm_id


            # Fetch Containers and their IPs
            containers = self.proxmox.nodes(node_name).lxc.get()
            for container in containers:
                container_id = container['vmid']
                object_ips[container['name']] = {}
                ips, macs = self._get_container_ip(node_name, container_id)
                object_ips[container['name']]['ips'] = ips
                object_ips[container['name']]['macs'] = macs
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
    output_format.add_argument("-m", "--markdown", action="store_true", help="Print as Markdown")
    parser.add_argument("-S", "--start", action="store_true", help="Start a VM or container")
    parser.add_argument("-T", "--stop", action="store_true", help="Stop a VM or container")
    parser.add_argument("-n", "--name", help="Specify the name of the VM or container to start or stop")
    # add a group for sorting the output
    sort_group = parser.add_mutually_exclusive_group()
    sort_group.add_argument("--sort", choices=["name", "id", "ips", "type"], default="id", help="Sort the output by the specified field")
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
        table_data = [["Name", "IPs", "MACs", "Type", "ID"]]

        sorted_items = sorted(object_ips.items(), key=lambda x: x[1][args.sort])
        
        # Add data rows sorted by ID
        for name, details in sorted_items:
            ips_str = ",".join(details['ips'])
            macs_str = ",".join(details['macs'])
            table_data.append([
                str(details['id']),
                name,
                ips_str,
                macs_str,
                details['type']
            ])

        table = Table()
        table.add_column("ID")        
        table.add_column("Name")
        table.add_column("IPs") 
        table.add_column("MACs")
        table.add_column("Type")

        for row in table_data[1:]:
            table.add_row(*row)
            
        console = Console()
        console.print(table)
    elif args.markdown:
        md_content = "# Proxmox VMs and Containers\n\n"
        md_content += "| ID | Name | IPs | MACs | Type |\n"
        md_content += "|:--:|:-----|:----|:-----|:----:|\n"
        
        sorted_items = sorted(object_ips.items(), key=lambda x: x[1][args.sort])
        
        for name, details in sorted_items:
            ips_str = "<br>".join(details['ips'])
            macs_str = "<br>".join(details['macs'])
            md_content += f"| {details['id']} | {name} | {ips_str} | {macs_str} | {details['type']} |\n"
        
        print(md_content)
    else:
        print(json.dumps(object_ips, indent=4, separators=(',', ':')))

    if args.start and args.name:
        manager.start_object(args.name)
    elif args.stop and args.name:
        manager.stop_object(args.name)
