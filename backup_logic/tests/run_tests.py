import unittest
import sys
import os
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        print(f"Loading environment variables from {env_path}")
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        return True
    return False

def run_tests():
    """Run all tests in the tests directory."""
    # Add project root directory to Python path
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    # Load environment variables
    if load_env_file():
        print("Environment variables loaded successfully")
    else:
        print("Warning: .env file not found")

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())