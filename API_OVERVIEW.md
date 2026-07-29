## What is the API and Why Use It?

The API (Application Programming Interface) allows you to control Transmute **programmatically** without using the web interface. Instead of uploading files through a browser, you can send commands via code, scripts, or other applications.

This enables:
- **Automation** of repetitive tasks
- **Integration** with other tools and services
- **Batch processing** of large numbers of files
- **Custom workflows** tailored to your specific needs

---

## Key API Endpoints

### 1. File Management
| Endpoint | Description |
|----------|-------------|
| `POST /api/files` | Upload a file |
| `POST /api/files/url` | Upload a file from a URL |
| `GET /api/files` | List all uploaded files |
| `DELETE /api/files/{id}` | Delete a specific file |
| `GET /api/files/{id}` | Download a file |

### 2. Conversion
| Endpoint | Description |
|----------|-------------|
| `POST /api/jobs` | Create a conversion job |
| `GET /api/jobs` | List all conversion jobs |
| `GET /api/jobs/{id}` | Get job status |
| `POST /api/jobs/{id}/cancel` | Cancel a job |
| `POST /api/jobs/{id}/retry` | Retry a failed job |

### 3. Compression
| Endpoint | Description |
|----------|-------------|
| `POST /api/compression-jobs` | Create a compression job |
| `GET /api/compression-jobs` | List compression jobs |

### 4. Administration
| Endpoint | Description |
|----------|-------------|
| `GET /api/users` | List all users |
| `POST /api/users` | Create a user |
| `PATCH /api/users/{id}` | Update a user |
| `DELETE /api/users/{id}` | Delete a user |
| `GET /api/stats` | Get system statistics |

### 5. Settings
| Endpoint | Description |
|----------|-------------|
| `GET /api/settings` | Get current settings |
| `PATCH /api/settings` | Update settings |
| `GET /api/settings/themes` | List available themes |
| `POST /api/settings/themes` | Create custom theme (admin) |

---

## Authentication

### Getting an API Key

1. Log in to Transmute as an administrator
2. Navigate to **"My Account" → "API Keys"**
3. Click **"Create API Key"**
4. Provide a name (e.g., "my-script")
5. **Save the generated key immediately** — it is shown only once!

### Using an API Key

Include the key in the `Authorization` header for any endpoint that requires authentication:

```
Authorization: Bearer <your-api-key>
```

Alternatively, you can use a JWT token obtained through the authentication endpoint.

---

## Practical Examples

### Example 1: Automatic Conversion via cURL

```bash
# 1. Authenticate and get a token
TOKEN=$(curl -X POST http://localhost:3313/api/users/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}' \
  | jq -r '.access_token')

# 2. Upload a file
FILE_ID=$(curl -X POST http://localhost:3313/api/files \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/image.png" \
  | jq -r '.metadata.id')

# 3. Convert to WebP
JOB_ID=$(curl -X POST http://localhost:3313/api/jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"id\":\"$FILE_ID\",\"output_format\":\"webp\",\"quality\":\"high\"}" \
  | jq -r '.id')

# 4. Check job status
curl -X GET http://localhost:3313/api/jobs/$JOB_ID \
  -H "Authorization: Bearer $TOKEN"
```

### Example 2: Python Script for Batch Conversion

```python
import requests
import os

API_URL = "http://localhost:3313/api"
TOKEN = "your_api_key_or_jwt_token"

headers = {"Authorization": f"Bearer {TOKEN}"}

# Upload and convert all PNG files in a folder
for filename in os.listdir("./images"):
    if filename.endswith(".png"):
        with open(f"./images/{filename}", "rb") as f:
            response = requests.post(
                f"{API_URL}/files",
                headers=headers,
                files={"file": f}
            )
            file_id = response.json()["metadata"]["id"]
            
            # Convert to WebP
            job = requests.post(
                f"{API_URL}/jobs",
                headers=headers,
                json={"id": file_id, "output_format": "webp"}
            )
            print(f"Converting: {filename} -> job {job.json()['id']}")
```

### Example 3: Automatic File Cleanup

```bash
# Get list of all files
curl -X GET http://localhost:3313/api/files \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.files[].id'

# Delete a specific file
curl -X DELETE http://localhost:3313/api/files/{file_id} \
  -H "Authorization: Bearer $TOKEN"
```

### Example 4: Health Monitoring

```bash
# Liveness check
curl http://localhost:3313/api/health/live

# Readiness check
curl http://localhost:3313/api/health/ready

# Application metadata
curl http://localhost:3313/api/health/info
```

---

## What You Can Build with the API

| Use Case | Solution |
|----------|----------|
| **Automated folder processing** | Script monitors a folder and uploads new files to the API |
| **Telegram bot integration** | Bot receives files, converts them, and sends them back |
| **Scheduled cleanup** | Cron job deletes old files periodically |
| **Monitoring and alerts** | Check server health via `/api/health/ready` |
| **Batch processing** | Convert hundreds of files with a single command |
| **User management automation** | Programmatically create and manage users |

---

## Interactive Documentation

Full API documentation is available at:

**http://localhost:3313/api/docs**

From there you can:
- Browse all available endpoints
- View request/response schemas
- Test API calls directly from your browser

---

## ⚡ Quick Integration Tips

1. **Start simple** — Use the interactive docs to test endpoints before writing code
2. **Use API keys** for scripts and automated tasks
3. **Monitor jobs** — Always check job status after submitting conversion requests
4. **Handle errors** — The API returns appropriate HTTP status codes and error messages
5. **Keep it local** — Transmute runs on your machine; use `localhost` or your local IP

---

## Summary

With the Transmute API, you can:
- ✅ Upload and manage files programmatically
- ✅ Convert and compress files via code
- ✅ Automate repetitive tasks
- ✅ Integrate with other applications
- ✅ Monitor system health
- ✅ Manage users and settings

The API makes Transmute a powerful automation engine for all your file conversion needs!
```