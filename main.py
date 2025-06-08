from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import shlex
from urllib.parse import urlparse, unquote

PORT = 8888


class CurlMCPHandler(BaseHTTPRequestHandler):
    def _send_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def _execute_curl(self, url):
        try:
            # Execute curl with a 10-second timeout
            result = subprocess.run(
                ["curl", "-s", "-m", "10", url], capture_output=True, text=True
            )

            if result.returncode == 0:
                try:
                    json_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    json_data = result.stdout
                return {
                    "success": True,
                    "status": "success",
                    "url": url,
                    "status_code": 200,
                    "data": json_data,
                    "timestamp": self.date_time_string(),
                }
            else:
                return {
                    "success": False,
                    "status": "error",
                    "url": url,
                    "status_code": 500,
                    "error": result.stderr or "Unknown error occurred",
                    "timestamp": self.date_time_string(),
                }

        except Exception as e:
            return {
                "success": False,
                "status": "error",
                "url": url,
                "status_code": 500,
                "error": str(e),
                "timestamp": self.date_time_string(),
            }

    def do_GET(self):
        # Handle root path
        if self.path == "/":
            self._send_response(
                {
                    "status": "success",
                    "service": "Curl MCP Server",
                    "usage": "Access any URL by visiting /<url>",
                    "example": f"http://localhost:{PORT}/https://example.com",
                    "endpoints": [
                        "GET / - This help message",
                        "GET /<url> - Fetch URL content",
                    ],
                    "timestamp": self.date_time_string(),
                }
            )
            return

        try:
            # Extract URL from path
            url = self.path[1:]  # Remove leading /

            # Ensure URL has a protocol
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            # Execute the curl command
            result = self._execute_curl(url)

            # Send appropriate status code based on success
            status_code = result["status_code"]
            self._send_response(result, status_code)

        except json.JSONDecodeError as e:
            self._send_response(
                {
                    "status": "error",
                    "error": f"Invalid JSON: {str(e)}",
                    "timestamp": self.date_time_string(),
                },
                400,
            )

        except Exception as e:
            self._send_response(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": self.date_time_string(),
                },
                500,
            )

    def do_OPTIONS(self):
        """Handle preflight CORS requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run(server_class=HTTPServer, handler_class=CurlMCPHandler, port=PORT):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"✅ Curl MCP Server running on http://localhost:{port}")
    print(f"\nTry it with:\n  curl http://localhost:{port}/https://example.com\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()
        print("Server stopped.")


if __name__ == "__main__":
    run()
