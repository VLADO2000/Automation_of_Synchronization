import os
import shutil
import tempfile
from unittest.mock import patch, Mock

import pytest

from syncApp import setup_logging, compare_folders, synchronize_folders

@pytest.fixture
def temp_dirs_setup():
    source_dir = tempfile.mkdtemp()
    replica_dir = tempfile.mkdtemp()
    yield source_dir, replica_dir
    shutil.rmtree(source_dir)
    shutil.rmtree(replica_dir)

@pytest.fixture
def mock_logging():
    with patch('syncApp.logging') as mock_logging:
        yield mock_logging
    
def test_setup_logging(mock_logging):
    log_file = 'test.log'
    setup_logging(log_file)
    assert mock_logging.basicConfig.called
    assert mock_logging.FileHandler.called_with(log_file, encoding='utf-8')
    assert mock_logging.StreamHandler.called

def test_compare_folders_non_exisitng_source(mock_logging, temp_dirs_setup):
    _, replica_dir = temp_dirs_setup
    non_existent_fpath = '/path/does/not/exist'
    actions = compare_folders(non_existent_fpath, replica_dir)
    assert mock_logging.error.called_with(f'Source folder {non_existent_fpath} doesn\'t exist')
    assert not actions

def test_compare_folders_new_replica(mock_logging, temp_dirs_setup):
    source_dir, replica_dir = temp_dirs_setup
    os.makedirs(os.path.join(source_dir, 'dir1'))
    open(os.path.join(source_dir, 'dir1', 'file1.txt'), 'w').close()
    actions = compare_folders(source_dir, replica_dir)
    assert mock_logging.called_with(f'Replica folder {replica_dir} created')
    assert len(actions) == 1 # Expected actions of file copying

def test_synchronize_folders(mock_logging, temp_dirs_setup):
    source_dir, replica_dir = temp_dirs_setup
    os.makedirs(os.path.join(source_dir, 'dir1'))
    open(os.path.join(source_dir, 'dir1', 'file1.txt'), 'w').close()
    actions = compare_folders(source_dir, replica_dir)
    synchronize_folders(actions)
    assert mock_logging.called_with(f"Copying {os.path.join(source_dir, 'dir1', 'file1.txt')} \
                                    to {os.path.join(replica_dir, 'dir1', 'file1.txt')}...")
    assert os.path.exists(os.path.join(replica_dir, 'dir1', 'file1.txt'))



