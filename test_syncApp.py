import os
import shutil
import tempfile
from unittest.mock import patch, Mock

import pytest

from syncApp import setup_logging, compare_folders, synchronize_folders

@pytest.fixture
def tem_dirs_setup():
    source_dir = tempfile.mkdtemp()
    replica_dir = tempfile.mkdtemp()
    yield source_dir, replica_dir
    shutil.rmtree(source_dir)
    shutil.rmtree(replica_dir)

@pytest.fixture
def mock_login():
    with patch('syncApp.logging') as mock_logging:
        yield mock_logging
    

