from locust import task, FastHttpUser, between


class Browse(FastHttpUser):
    # Define the host URL for faster lookup
    host = "http://localhost:5000"

    # Reduce idle time between tasks for higher RPS
    wait_time = between(0.1, 0.2)

    # Default headers shared across requests
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def browse_page(self):
        """
        Simulates browsing by sending a GET request to /browse.
        """
        # Combine default headers with task-specific headers
        headers = {
            **self.default_headers,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Upgrade-Insecure-Requests": "1",
        }

        # Use a GET request to /browse with minimal processing
        with self.client.get("/browse", headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()  # Mark the request as successful
            else:
                response.failure(f"Unexpected status code: {response.status_code}")


if __name__ == "__main__":
    from locust import run_single_user
    run_single_user(Browse)
