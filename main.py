from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import shlex

PORT = 8888

class CurlMCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        request = json.loads(post_data)

        # Extract curl command from request
        curl_cmd = request.get("curl_cmd", "")
        if not curl_cmd:
            self.send_error(400, "Missing 'curl_cmd' in request")
            return

        try:
            # Execute the curl command
            args = shlex.split(curl_cmd)
            result = subprocess.run(["curl"] + args, capture_output=True, text=True)

            # Send response
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode,
                    }
                ).encode()
            )

        except Exception as e:
            self.send_error(500, f"Error executing curl: {str(e)}")


def run(server_class=HTTPServer, handler_class=CurlMCPHandler, port=PORT):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting curl MCP server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
