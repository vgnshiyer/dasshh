# Abilities

Dasshh supports various tools to interact with your system using natural language commands.

More tools will be added in future versions. Please feel free to drop your suggestions [here](https://github.com/vgnshiyer/dasshh/issues).

!!! note
    Permission based tool execution is currently under development. As of now, Dasshh will perform a tool call if it seems appropriate.

## Available Tools

In the current version of Dasshh, the following tools are available:

### System Information

These tools provide information about your system's hardware and software:

| Tool Name | Description | Example Commands |
|-----------|-------------|-----------------|
| `system_info` | Get detailed information about your operating system | "What OS am I running?" |
| `cpu_info` | Get information about CPU and its current usage | "Show my CPU usage" |
| `memory_info` | Get memory (RAM) information and usage | "How much RAM do I have available?" |
| `disk_info` | Get disk space information for a specified path | "How much disk space is left on my main drive?" |
| `network_info` | Get network interface information | "Show my network interface details" |

### Process Management

These tools help you manage running processes on your system:

| Tool Name | Description | Example Commands |
|-----------|-------------|-----------------|
| `process_list` | List all running processes with basic information | "Show all running processes" |
| `find_process` | Find processes matching a specific name pattern | "Find all Chrome processes" |
| `get_process_info` | Get detailed information about a specific process by PID | "Give me details about process 1234" |
| `kill_process` | Terminate a process by its PID | "Kill process 1234" |
| `run_command` | Run a shell command and return its output | "Run ls -la" |

### File Operations

These tools help you manage files and directories:

| Tool Name | Description | Example Commands |
|-----------|-------------|-----------------|
| `current_directory` | Get the current working directory | "What's my current directory?" |
| `list_files` | List all files and directories in a specified directory | "List files in ~/Downloads" |
| `file_info` | Get detailed information about a file or directory | "Tell me about file.txt" |
| `read_file` | Read the contents of a file | "Read config.json" |
| `create_directory` | Create a new directory at the specified path | "Create a directory called 'projects'" |
| `delete_file` | Delete a file or directory | "Delete file.txt" |
| `copy_file` | Copy a file or directory from source to destination | "Copy file.txt to ~/backup/" |
| `move_file` | Move a file or directory from source to destination | "Move file.txt to ~/archive/" |

### Network Tools

These tools help you with network-related tasks:

| Tool Name | Description | Example Commands |
|-----------|-------------|-----------------|
| `ping` | Ping a host and return the results | "Ping google.com" |
| `get_ip_address` | Get IP address for a hostname or the local machine | "What's my IP address?" |
| `check_port` | Check if a specific port is in use on localhost | "Is port 8080 in use?" |
| `public_ip` | Get the public IP address of the current machine | "What's my public IP?" |
| `traceroute` | Perform a traceroute to a host | "Run traceroute to github.com" |

!!! note
    Based on your query, Dasshh can use multiple tools together to perform complex tasks.