import requests
import sys

BASE_URL = "http://localhost:5000"

def test_homepage():
    r = requests.get(BASE_URL + '/')
    assert r.status_code == 200
    print("Homepage OK")

if __name__ == "__main__":
    try:
        test_homepage()
        print("All tests passed")
        sys.exit(0)
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)