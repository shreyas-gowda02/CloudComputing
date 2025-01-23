from locust import task, FastHttpUser, between
from insert_product import login


class AddToCart(FastHttpUser):
    # Define the host (shared across all requests)
    host = "http://localhost:5000"

    # Set wait time to a small range to minimize idle time between tasks
    wait_time = between(0.1, 0.5)

    def on_start(self):
        """
        This is executed once per user at the beginning of their session.
        """
        self.username = "test123"
        self.password = "test123"

        # Perform login once and reuse the token
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")

        # Pre-build headers to reduce request preparation overhead
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "DNT": "1",
            "Referer": "http://localhost:5000/product/1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Cookie": f"token={self.token}",
        }

    @task
    def fetch_cart(self):
        """
        Simulates a user fetching their cart.
        """
        # Make a GET request to the cart endpoint
        with self.client.get("/cart", headers=self.headers, catch_response=True) as response:
            if response.status_code == 200:
                # Mark request as successful (minimal processing to save time)
                response.success()
            else:
                # Log any failed requests for debugging purposes
                response.failure(f"Unexpected status code: {response.status_code}")


if __name__ == "__main__":
    from locust import run_single_user
    run_single_user(AddToCart)
