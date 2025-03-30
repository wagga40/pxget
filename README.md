# PXGET

A Python script to fetch IP addresses and MAC addresses of VMs and containers from a Proxmox Virtual Environment (PVE). The script uses the `proxmoxer` library to connect to the Proxmox API, retrieve network information, and output the results in various formats.

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
python pxget.py -s <PROXMOX_SERVER> [-u <USER>] [-p <PASSWORD>] [-o <OUTPUT_FILE>] [-a | -j | -m] [-S | -T] [-n <NAME>] [--sort <FIELD>]
```

- `-s`, `--server` (required): The IP address or hostname of the Proxmox server.
- `-u`, `--user`: The Proxmox username. Defaults to `root@pam`.
- `-p`, `--password`: The Proxmox password. If not provided, the script will prompt interactively.
- `-o`, `--output`: The path to save the output as a JSON file.
- `-a`, `--array`: Print the output as a formatted table in the console.
- `-j`, `--jq`: Print as JQ compatible JSON (default).
- `-m`, `--markdown`: Print as Markdown table.
- `-S`, `--start`: Start a VM or container.
- `-T`, `--stop`: Stop a VM or container.
- `-n`, `--name`: Specify the name of the VM or container to start or stop.
- `--sort`: Sort the output by field (name, id, ips, or type). Defaults to id.

### Examples

1. **Fetch IPs and Display in Console (JSON format)**

    ```bash
    python pxget.py -s 192.168.0.XX
    ```

2. **Fetch IPs and Save to JSON File**

    ```bash
    python pxget.py -s 192.168.0.XX -u root@pam -o output.json
    ```

3. **Fetch IPs and Display as Table**

    ```bash
    python pxget.py -s 192.168.0.XX -a
    ```

4. **Fetch IPs and Display as Markdown**

    ```bash
    python pxget.py -s 192.168.0.XX -m
    ```

5. **Start a VM or Container**

    ```bash
    python pxget.py -s 192.168.0.XX -S -n vm_name
    ```

6. **Stop a VM or Container**

    ```bash
    python pxget.py -s 192.168.0.XX -T -n vm_name
    ```

## Output Format

The script outputs the information in the following formats:

### JSON (JQ compatible)

```json
{
    "vm_name_1": {
        "ips": ["192.168.0.2", "192.168.0.3"],
        "macs": ["00:11:22:33:44:55", "66:77:88:99:AA:BB"],
        "type": "vm",
        "id": 101
    },
    "container_name_1": {
        "ips": ["192.168.0.4"],
        "macs": ["00:11:22:33:44:55"],
        "type": "container",
        "id": 102
    }
}
```

### Table (Rich Console)

When using the `-a` or `--array` option, the script will output the information in a formatted table:

| ID  | Name              | IPs                     | MACs                    | Type        |
|-----|-------------------|-------------------------|-------------------------|-------------|
| 101 | vm_name_1         | 192.168.0.2,192.168.0.3 | 00:11:22:33:44:55,...   | vm          |
| 102 | container_name_1  | 192.168.0.4             | 00:11:22:33:44:55       | container   |

### Markdown

When using the `-m` or `--markdown` option, the script will output the information in Markdown table format:

```markdown
# Proxmox VMs and Containers

| ID | Name | IPs | MACs | Type |
|:--:|:-----|:----|:-----|:----:|
| 101 | vm_name_1 | 192.168.0.2<br>192.168.0.3 | 00:11:22:33:44:55<br>66:77:88:99:AA:BB | vm |
| 102 | container_name_1 | 192.168.0.4 | 00:11:22:33:44:55 | container |
```

## Author

- [wagga40](https://github.com/wagga40)



