# TASK2 – Asynchronous Python HTTP Server

## **Mô tả dự án**

* Xử lý **HTTP requests đồng bộ và bất đồng bộ** (synchronous & asynchronous).
* **Xác thực người dùng** qua **cookies** hoặc **Basic Auth**.
* Quản lý **sessions** cho người dùng đăng nhập.
* Dễ dàng đăng ký các **route** (endpoint) với các HTTP method khác nhau.
* Ví dụ app đi kèm với các route `/login`, `/echo`, và `/hello`.

Dự án được xây dựng với các module chính:

| Module               | Chức năng                                                       |
| -------------------- | --------------------------------------------------------------- |
| `asynaprous.py`      | Framework đăng ký route, chạy server, hỗ trợ async/sync handler |
| `auth.py`            | Quản lý users, sessions, cookie auth, decorator `require_auth`  |
| `backend.py`         | Tạo backend server và xử lý kết nối TCP socket                  |
| `httpadapter.py`     | Adapter xử lý HTTP request/response                             |
| `request.py`         | Parse HTTP request, headers, cookies, body                      |
| `response.py`        | Xây dựng HTTP response với status code, headers, cookies        |
| `start_sampleapp.py` | Ví dụ ứng dụng server với các route demo                        |

---

## **Chạy server**

```bash
python start_sampleapp.py
```

Server sẽ chạy trên:

```
IP: 0.0.0.0
Port: 2026
```

---

## **Các endpoint**

### **1. POST `/login`**

Đăng nhập người dùng.

* **Request JSON body**:

```json
{
  "username": "admin",
  "password": "123"
}
```

* **Response**:

```json
{
  "message": "login success",
  "session": "<session-id>"
}
```

Session ID sẽ được gửi về client để lưu trong cookie `session`.

---

### **2. POST `/echo`** (Yêu cầu auth)

* **Headers**:

  * Cookie `session=<session-id>` hoặc Basic Auth.

* **Request JSON body**:

```json
{
  "msg": "hello world"
}
```

* **Response**:

```json
{
  "received": {
    "msg": "hello world"
  }
}
```

---

### **3. PUT `/hello`** (Yêu cầu auth, async)

* **Headers**:

  * Cookie `session=<session-id>` hoặc Basic Auth.

* **Response**:

```json
{
  "msg": "hello async"
}
```

---

## **Tính năng nổi bật**

* **Async & Sync handler**: Route có thể là async function hoặc sync function.
* **Session management**: Quản lý session bằng cookies.
* **Basic Auth fallback**: Nếu không có cookie, hỗ trợ Basic Auth header.
* **Plug & play routes**: Dễ dàng thêm route mới với decorator `@app.route(...)`.

---

## **Cấu trúc thư mục**

```
TASK2/
├─ asynaprous.py       # Framework route, async/sync handler
├─ auth.py             # Xác thực, session, decorator
├─ backend.py          # Socket backend, chạy server
├─ httpadapter.py      # Adapter HTTP request/response
├─ request.py          # Parse HTTP request
├─ response.py         # Build HTTP response
├─ start_sampleapp.py  # Ví dụ server chạy với các route
├─ __pycache__/        # Python bytecode
```

---

## **Ví dụ sử dụng**

```python
from asynaprous import AsynapRous
from auth import require_auth

app = AsynapRous()

@app.route("/test", methods=["GET"])
@require_auth
def test(headers, body):
    return b'{"message": "ok"}'

app.prepare_address("127.0.0.1", 2026)
app.run()
```

---
<p align="center">
  <a href="https://www.facebook.com/Shiba.Vo.Tien">
    <img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"/>
  </a>
  <a href="https://www.tiktok.com/@votien_shiba">
    <img src="https://img.shields.io/badge/TikTok-000000?style=for-the-badge&logo=tiktok&logoColor=white" alt="TikTok"/>
  </a>
  <a href="https://www.facebook.com/groups/khmt.ktmt.cse.bku?locale=vi_VN">
    <img src="https://img.shields.io/badge/Facebook%20Group-4267B2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Group"/>
  </a>
  <a href="https://www.facebook.com/CODE.MT.BK">
    <img src="https://img.shields.io/badge/Page%20CODE.MT.BK-0057FF?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Page"/>
  </a>
  <a href="https://github.com/VoTienBKU">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>