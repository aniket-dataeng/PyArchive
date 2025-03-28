import pytest
import os
import sys
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.file_handler import FileHandler
from scripts.database import DatabaseHandler
from unittest.mock import MagicMock

@pytest.fixture
def sample_config():
    return {
        "source_directory": "test_data/source",
        "destination_directory": "test_data/destination",
        "log_file": "test_data/test.log",
        "database": "test_data/test.db",
        "compression": {"timestamp_format": "%Y%m%d_%H%M%S"},
        "report": "test_data/reports"
    }

@pytest.fixture
def file_handler(sample_config):
    return FileHandler(sample_config)

def test_directories_created(file_handler):
    """Test if required directories are created."""
    assert os.path.exists(file_handler.src_dir)
    assert os.path.exists(file_handler.tgt_dir)
    assert os.path.exists(file_handler.report_loc)

@pytest.fixture
def mock_file_handler(mocker):
    """Fixture to create a FileHandler instance with a mocked DatabaseHandler."""
    mock_config = {
        "source_directory": "test_data/source",
        "destination_directory": "test_data/destination",
        "compression": {"timestamp_format": "%Y-%m-%d_%H-%M-%S"},
        "database": "test_data/db.sqlite",
        "log_file": "test_data/pybak.log",
        "report": "test_data/reports"
    }
    
    # Mocking DatabaseHandler
    mock_db_handler = mocker.patch("scripts.database.DatabaseHandler", autospec=True)
    mock_instance = mock_db_handler.return_value
    mock_instance.check_dups.return_value = 1  # Simulate that the file is a duplicate
    
    file_handler = FileHandler(mock_config)
    file_handler.db_handler = mock_instance  # Inject mock database
    
    return file_handler

def test_duplicate_files_skipped(mock_file_handler, mocker):
    """Test if duplicate files are skipped during compression."""
    mocker.patch("os.listdir", return_value=["testfile.txt"])
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=b"fake_content"))
    mocker.patch("hashlib.sha256", return_value=MagicMock(hexdigest=lambda: "fakehash"))

    # Mocking the logging to prevent real logs
    mocker.patch("logging.info")
    
    mock_file_handler.compress_files()
    
    # Ensure that insert_file_record was never called since it's a duplicate
    mock_file_handler.db_handler.insert_file_record.assert_not_called()

def test_report_generation(mock_file_handler):
    """Test if a report is generated after file processing."""
    sample_file = "test_data/source/sample.txt"
    with open(sample_file, "w") as f:
        f.write("Test content")
    
    mock_file_handler.gen_report()

    # Get all files in the reports directory
    report_dir = "test_data/reports"
    report_files = [f for f in os.listdir(report_dir) if f.endswith(".csv")]

    # Debugging print
    print("Generated report files:", report_files)

    # Assert that at least one CSV report exists
    assert report_files, "No CSV report file was generated"

