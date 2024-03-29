import hashlib
import os
import logging
import shutil


def setup_logging(log_file):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        handlers=[
                            logging.FileHandler(log_file, encoding='utf-8'),
                            logging.StreamHandler(),
                        ])

def get_file_hash(file_path):
    # A arbitrary (but fixed) buffer size
    # 16384 bytes = 16 kilobytes
    BUF_SIZE = 16384

    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk:= f.read(BUF_SIZE):
            sha256.update(chunk)
    # hexdigest() hashes the data, and returns 
    # the output in hexadecimal format
    return sha256.hexdigest()

def compare_folders(source, replica):
    actions = []
    if not os.path.exists(source):
        logging.error(f'Source folder {source} doesn\'t exist')
        return actions
    try:
        os.makedirs(replica)
    except FileExistsError:
         logging.info(f'Replica folder {replica} modification happened')
    else:
        logging.info(f'Replica folder {replica} created')

    #First and foremost look at source tree
    for root, dirs, files in os.walk(source):
        #Procuring relative path indicator of source folder
        #if root is usr/home/source and source is usr/home/source/folder1 - folder1 should be obtained
        rel_path = os.path.relpath(root, source)
        #Construction of replica full path
        replica_root = os.path.join(replica, rel_path)
        #Directories action constructor
        for dir_name in dirs:
            replica_dir_path = os.path.join(replica_root, dir_name)
            try:
                os.makedirs(replica_dir_path)
            except FileExistsError:
                logging.info(f"Creation of directory {replica_dir_path} has not happened this time due \
                             to modification of its content")
            else:
                logging.info(f"Creation of directory {replica_dir_path} on replica folder")
        #Files action construcor
        for file_name in files:
            source_file_path = os.path.join(root, file_name)
            replica_file_path = os.path.join(replica_root, file_name)
            if not os.path.exists(replica_file_path):
                actions.append(("copy", source_file_path, replica_file_path))
            elif get_file_hash(source_file_path) != get_file_hash(replica_file_path):
                actions.append(("copy", source_file_path, replica_file_path))    
    #Validation upon removal needs in replica tree moving from bottom towards top
    for root, dirs, files in os.walk(replica, topdown=False):
        rel_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, rel_path)

        for dir_name in dirs:
            source_dir_path = os.path.join(source_root, dir_name)
            replica_dir_path = os.path.join(root, dir_name)
            if not os.path.exists(source_dir_path):
                actions.append(('remove_dir', replica_dir_path))
        
        for file_name in files:
            source_file_path = os.path.join(source_root, file_name)
            replica_file_path = os.path.join(root, file_name)
            if not os.path.exists(source_file_path):
                actions.append(("remove_file", replica_file_path))
    return actions
        

def synchronize_folders(actions):
    for action, source, replica in actions:
        match action, source, replica:
            case 'copy', source, replica:
                logging.info(f"Copying {source} to {replica}...")
                shutil.copy2(source, replica)
            case 'remove_file', replica:
                logging.info(f"Removing {replica} file")
                os.remove(replica)
            case 'remove_dir', replica:
                logging.info(f"Removing {replica} directory")
                shutil.rmtree(replica)
            case _:
                logging.warning(f"Unnown action maube {action}")
        