import requests
import sys

URL = "https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl"

def check_sri():
    print(f"📡 PROBING SRI TEST SERVER: {URL}")
    try:
        response = requests.get(URL, timeout=10)
        print(f"🔄 STATUS CODE: {response.status_code}")
        if response.status_code == 200:
            print("✅ CONNECTION SUCCESSFUL: SRI Gateway is reachable.")
            return True
        else:
            print("❌ CONNECTION FAILED: Non-200 Response.")
            return False
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    if check_sri():
        sys.exit(0)
    else:
        sys.exit(1)
