import requests

class DashboardTester:
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

    def set_initial_settings(self):
        url = f"{self.base_url}/settings/set"
        settings_data = {
            "calories": 2000,
            "bedtime": "22:00",
            "wakeupTime": "06:00",
            "sleep": 8,
            "meals": 3,
            "notificationsSleep": True,
            "notificationsMeals": True
        }
        try:
            response = requests.post(url, headers=self.headers, json=settings_data)
            print(f"POST {url} => {response.status_code}")
            print(f"Response: {response.json()}\n")
        except Exception as e:
            print(f"Error setting initial settings: {e}")

    def fetch_dashboard(self):
        url = f"{self.base_url}/dashboard/fetch"
        try:
            response = requests.get(url, headers=self.headers)
            print(f"GET {url} => {response.status_code}")
            print(f"Response: {response.json()}\n")
        except Exception as e:
            print(f"Error fetching dashboard: {e}")

if __name__ == "__main__":
    base_url = "http://localhost:5001"
    email = "a@gmail.com"  # Replace with real test email
    password = "Amine12!"         # Replace with real test password

    tester = DashboardTester(base_url, email, password)

    if tester.token:
        print("\nNow testing fetch_dashboard:")
        tester.fetch_dashboard()
    else:
        print("Token retrieval failed. Cannot proceed with test.")