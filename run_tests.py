import os
import sys
import pytest

def run_tests():
    """Run all tests in the project and report results."""
    print("Starting test execution with pytest...")
    
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run pytest on the tests directory with detailed output
    exit_code = pytest.main([
        '-v',                         # Verbose output
        '--color=yes',                # Colored output
        f'{os.path.join(current_dir, "src", "tests")}',  # Test directory
        '--no-header',                # No pytest header
        '--no-summary',               # No summary
    ])
    
    # Check the exit code
    if exit_code == 0:
        print("\n✅ All tests passed successfully!")
        return True
    else:
        print(f"\n❌ Tests failed with exit code: {exit_code}")
        return False

if __name__ == "__main__":
    success = run_tests()
    # Exit with appropriate code for CI/CD pipelines
    sys.exit(0 if success else 1)
