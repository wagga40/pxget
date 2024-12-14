# PXGET

A Python script to fetch IP addresses of VMs and containers from a Proxmox Virtual Environment (PVE). The script uses the `proxmoxer` library to connect to the Proxmox API, retrieve network information, and output the results either to the console or to a JSON file.

## Prerequisites

- Python 3.x
- `proxmoxer` library
- `rich` library

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/wagga40/pxget.git
    cd pxget
    ```

2. **Install Required Python Libraries**

    Install the required Python packages using pip or another package manager:

    ```bash
    pip install proxmoxer rich
    ```

## Usage

### Command-Line Arguments

```bash
python script.py -s <PROXMOX_SERVER> [-u <USER>] [-p <PASSWORD>] [-o <OUTPUT_FILE>] [-a | -j]
```

- `-s`, `--server` (required): The IP address or hostname of the Proxmox server.
- `-u`, `--user`: The Proxmox username. Defaults to `root@pam`.
- `-p`, `--password`: The Proxmox password. If not provided, the script will prompt interactively.
- `-o`, `--output`: The path to save the output as a JSON file.
- `-a`, `--array`: Print the output as a formatted table in the console.
- `-j`, `--jq`: Print as JQ compatible JSON (default).

#### Sorting Output

You can sort the output based on different fields using the `--sort` option:

- `name`: Sort by the name of the VM or container.
- `id`: Sort by the VMID (default).
- `ips`: Sort by the IP addresses.
- `type`: Sort by the type (`vm` or `container`).

### Examples

1. **Fetch IPs and Display in Console (JSON format)**

    ```bash
    python script.py -s 192.168.0.XX
    ```

    This command will prompt for the password and then display the IP addresses of all VMs and containers in JSON format. By default, the username used for connection is `root@pam`.

2. **Fetch IPs and Save to JSON File**

    ```bash
    python script.py -s 192.168.0.XX -u root@pam -o output.json
    ```

    This command will fetch the IPs and save the results to `output.json`.

3. **Fetch IPs and Display as Table**

    ```bash
    python script.py -s 192.168.0.XX -a
    ```

    This command will prompt for the password and then display the IP addresses of all VMs and containers in a formatted table.

## Output Format

The script outputs the IP addresses in the following formats:

### JSON (JQ compatible)

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

### Table

When using the `-a` or `--array` option, the script will output the IP addresses in a formatted table as shown below:

| Name              | IPs                     | Type        | ID  |
|-------------------|-------------------------|-------------|-----|
| vm_name_1         | 192.168.0.2,192.168.0.3 | vm          | 101 |
| container_name_1  | 192.168.0.4             | container   | 102 |

- **Name**: The name of the VM or container.
- **IPs**: Comma-separated list of associated IP addresses.
- **Type**: Indicates whether the object is a VM or a container.
- **ID**: The VMID of the object in Proxmox.

## Author

- [wagga40](https://github.com/wagga40)
