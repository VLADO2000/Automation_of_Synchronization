Automation Folder Synchronization

Overview


This Python script facilitates the synchronization of files between two folders, ensuring that the replica folder precisely mirrors the source folder. It employs sha256 checksums to detect alterations in files and includes comprehensive logging for tracking operations.

Features

File Synchronization: Maintains synchronization between two directories.
sha256 Checksum Validation: Detects file modifications accurately.
Logging: Records operations such as file copying, updating, and deletion.
Periodic Sync: Executes at specified intervals to uphold synchronization in seconds.

Usage

Execute the script from the command line: python3 main.py <source_folder> <replica_folder> --interval --log <log_file>

<source_folder>: Path of the source folder.
<replica_folder>: Path of the replica folder.
--interval: Synchronization interval in seconds.
<log_file>: Path to the log file.
Example: python3 main.py /path/to/source /path/to/replica --interval 5 --log sync.log

Functionality

Replicates the structure and files of the source directory in the replica directory.
Compares files based on the sha256 hash algorithm.
Removes files and directories from the replica that are no longer present in the source.
Logs all operations in the desired location.

Testing

To ensure reliability, the script has been thoroughly tested using pytest, unittest, mock, and patch libraries.





