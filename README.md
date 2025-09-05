# SystemInfoCollector

This project is a Python-based system scanner that collects detailed information about a computer and saves it into a report file.
It is useful for:

System auditing

Quick hardware/software overview

Forensics and troubleshooting

Inventory management

The script automatically gathers:

System Info → OS, architecture, machine type, username, boot time

CPU Info → cores, frequency, usage stats

Memory Info → total, available, used, swap details

Disk Info → partitions, usage, free space

Network Info → hostname, IP, interfaces, connections

Running Processes → PID, name, CPU%, memory%

Environment Variables

Installed Packages (Python modules via pip list)

The output can be saved as JSON, TXT, or PDF depending on configuration.
