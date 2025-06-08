# curl_mcp

A simple HTTP server that acts as a CORS-enabled proxy for making HTTP requests and returning responses in a consistent JSON format. It's particularly useful for frontend development when you need to bypass CORS restrictions.

## Features

- 🚀 Simple HTTP server for making CORS-enabled requests
- 🔄 Automatically parses JSON responses when possible
- ⏱️ Built-in 10-second timeout for requests
- 🔒 CORS headers included for web browser access
- 📅 Timestamp included in all responses
- 🛠️ Consistent JSON response format

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/curl_mcp.git
   cd curl_mcp
   ```

2. Ensure you have Python 3.6+ installed

## Usage

### Starting the Server

```bash
python main.py
```

By default, the server runs on `http://localhost:8888`

### Making Requests

#### Basic Request

```bash
curl http://localhost:8888/https://api.example.com/data
```

#### Request with Path and Query Parameters

```bash
curl "http://localhost:8888/https://api.example.com/users?page=1&limit=10"
```

## Response Format

### Successful Response

```json
{
    "success": true,
    "status": "success",
    "url": "https://api.example.com/data",
    "status_code": 200,
    "data": {
        "key": "value",
        "nested": {"example": true}
    },
    "timestamp": "Sun, 08 Jun 2025 12:34:56 GMT"
}
```

### Error Response

```json
{
    "success": false,
    "status": "error",
    "url": "https://nonexistent.example",
    "status_code": 500,
    "error": "curl: (6) Could not resolve host: nonexistent.example",
    "timestamp": "Sun, 08 Jun 2025 12:34:56 GMT"
}
```

## Browser Usage

One of the main advantages of this server is that it can be used directly in web browsers to bypass CORS restrictions. Here's how:

### Basic Browser Request

```javascript
// Example using fetch API
fetch('http://localhost:8888/https://api.example.com/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### Example: Fetching JSON Data in a Web Page

```html
<!DOCTYPE html>
<html>
<head>
    <title>Curl MCP Browser Example</title>
</head>
<body>
    <h1>API Data Fetcher</h1>
    <button onclick="fetchData()">Fetch Data</button>
    <pre id="output">Click the button to load data</pre>

    <script>
    async function fetchData() {
        const output = document.getElementById('output');
        output.textContent = 'Loading...';
        
        try {
            const response = await fetch('http://localhost:8888/https://jsonplaceholder.typicode.com/todos/1');
            const data = await response.json();
            output.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            output.textContent = 'Error: ' + error.message;
        }
    }
    </script>
</body>
</html>
```

### Important Notes for Browser Usage

1. **Development Only**: This is meant for development purposes only. For production, set up proper CORS on your API server.
2. **Same Origin Policy**: The server must be running on the same domain as your web page or have proper CORS headers (which it does).
3. **HTTPS**: Modern browsers require HTTPS for certain features. For local development, `http://localhost` is fine.

## Examples

### Fetching JSON Data

```bash
# Make a request to a JSON API
curl http://localhost:8888/https://jsonplaceholder.typicode.com/todos/1
```

### Fetching HTML Content

```bash
# Get website HTML
curl http://localhost:8888/https://example.com
```

## Error Handling

The server returns appropriate HTTP status codes and error messages in the response body:

- `200`: Successful request
- `400`: Bad request (e.g., invalid URL format)
- `500`: Server error (e.g., connection failed)

## CORS Support

The server includes the following CORS headers by default:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type`

## License

MIT
