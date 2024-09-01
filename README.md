# PXGET

A Python script to fetch IP addresses of VMs and containers from a Proxmox Virtual Environment (PVE). The script uses the `proxmoxer` library to connect to the Proxmox API, retrieve network information, and output the results either to the console or to a JSON file.

## Prerequisites

- Python 3.x
- `proxmoxer` library

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/wagga40/pxget.git
    cd pxget
    ```

2. **Install Required Python Libraries**

    Install the required Python package using pip or an other package manager:

    ```bash
    pip install proxmoxer
    ```

## Usage

### Command-Line Arguments

```bash
python script.py -s <PROXMOX_SERVER> [-u <USER>] [-p <PASSWORD>] [-o <OUTPUT_FILE>]
```

- `-s`, `--server` (required): The IP address or hostname of the Proxmox server.
- `-u`, `--user`: The Proxmox username. Defaults to `root@pam`.
- `-p`, `--password`: The Proxmox password. If not provided, the script will prompt interactively.
- `-o`, `--output`: The path to save the output as a JSON file.

### Examples

1. **Fetch IPs and Display in Console**

    ```bash
    python script.py -s 192.168.0.XX
    ```

    This command will prompt for the password and then display the IP addresses of all VMs and containers in the console. By default the username used for connection is "root@pam".

2. **Fetch IPs and Save to JSON File**

    ```bash
    python script.py -s 192.168.0.XX -u root@pam -o output.json
    ```

    This command will fetch the IPs and save the results to `output.json`.

## Output Format

The script outputs the IP addresses in the following JSON format:

```json
{
    "vm_name_1": {
        "ips": ["192.168.0.2", "192.168.0.3"],
        "type": "vm",
        "id": 101
    },
    "container_name_1": {
        "ips": ["192.168.0.4"],
        "type": "container",
        "id": 102
    }
}
```

- **`ips`**: List of IP addresses associated with the VM or container.
- **`type`**: Indicates whether the object is a VM or a container.
- **`id`**: The VMID of the object in Proxmox.

## Author

- [wagga40](https://github.com/wagga40)
