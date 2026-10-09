import requests

class SettingsAPITester:
    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.token = self.login_and_get_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        } if self.token else {}

    def login_and_get_token(self):  
        url = f"{self.base_url}/auth/login"
        payload = {
            "email": self.email,
            "password": self.password
        }
        try:
            response = requests.post(url, json=payload)
            print(f"Login status: {response.status_code}")
            if response.status_code == 200:
                token = response.json().get("token")
                print(f"Token obtained: {token}")
                return token
            else:
                print(f"Login failed: {response.text}")
                return None
        except Exception as e:
            print(f"Error during login: {e}")
            return None

    def fetch_settings(self):
        url = f"{self.base_url}/settings/fetch"
        try:
            response = requests.get(url, headers=self.headers)
            print(f"GET {url} => {response.status_code}")
            print(f"Response: {response.json()}\n")
        except Exception as e:
            print(f"Error fetching settings: {e}")

    def set_settings(self, settings_data):
        url = f"{self.base_url}/settings/set"
        try:
            response = requests.post(url, headers=self.headers, json=settings_data)
            print(f"POST {url} => {response.status_code}")
            print(f"Response: {response.json()}\n")
        except Exception as e:
            print(f"Error setting settings: {e}")

if __name__ == "__main__":
    # Example usage
    base_url = "http://localhost:5001"
    email = "a@gmail.com"  # Replace with a real email
    password = "Amine12!"        # Replace with a real password

    tester = SettingsAPITester(base_url, email, password)

    if tester.token:
        # Dummy settings data to update
        dummy_settings = {
            "calories": 2000,
            "bedtime": "22:00",
            "wakeupTime": "06:00",
            "sleep": 8,
            "meals": 3,
            "notificationsSleep": True,
            "notificationsMeals": True
        }

        print("Testing set_settings:")
        tester.set_settings(dummy_settings)

        print("Testing fetch_settings:")
        tester.fetch_settings()
    else:
        print("Could not perform settings tests without a valid token.")
