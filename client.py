import requests
import sys
def main():
    response  = requests.get("http://localhost:8080/")
    if response.status_code == 200:
        print("Start page OK")
    else:
        print("Start page failed")
        sys.exit(1)
    response = requests.get("http://localhost:8080/get/0/name")
    if response.status_code == 200:
        print("Get first name OK")
    else:
        print("Get first name failed")
        sys.exit(1)
    response = requests.get("http://localhost:8080/all/name")
    if response.status_code == 200:
        print("Get all names OK")
    else:
        print("Get all names failed")
        sys.exit(1)
if(__name__ == "__main__"):
    main()