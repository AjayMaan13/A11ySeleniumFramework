# Script to run all tests

import pytest

if __name__ == "__main__":
    # Run all tests with HTML report generation
    pytest.main(["-v", "--html=reports/report.html"])