import requests
import random
import string

class AuthAPITester:
    def __init__(self, base_url):
        self.base_url = base_url

    def generate_random_user(self):
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        name = f"TestUser{random_id}"
        email = f"{random_id}@example.com"
        password = "password123"
        return name, email, password

    def test_signup(self, name, email, password):
        url = f"{self.base_url}/auth/signup"
        payload = {
            "name": name,
            "email": email,
            "password": password
        }
        try:
            response = requests.post(url, json=payload)
            print(f"POST {url} => {response.status_code}")
            print(f"Response: {response.json()}\n")
        except Exception as e:
            print(f"Error accessing {url}: {e}")

    def test_login(self, email, password):
        url = f"{self.base_url}/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        try:
            response = requests.post(url, json=payload)
            print(f"POST {url} => {response.status_code}")
            print(f"Response: {response.json()}\n")
        except Exception as e:
            print(f"Error accessing {url}: {e}")


if __name__ == "__main__":
    api = AuthAPITester("http://localhost:5001")  # Adjust as needed

    # Generate random test user
    test_name, test_email, test_password = api.generate_random_user()

    # Run tests
    print("Testing Signup:")
    api.test_signup(test_name, test_email, test_password)

    print("Testing Login:")
    api.test_login("Test10@gmail.com", 'FakePass1!')
