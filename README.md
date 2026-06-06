# **Image Hosting Service** 

# **Guide**

## **1\. System Requirements**

* **Operating System**: Windows 11 (also works on Linux/macOS)  
* **Docker Desktop** (version 20.10 or later) with WSL2 support (for Windows)  
* **Docker Compose** (included in Docker Desktop)  
* **Web browser**: Google Chrome (recommended) or any modern browser  
* **Free ports**: 8000 (backend) and 8080 (Nginx)

## **2\. Project Structure**
```
image_server/                                                                                                         |
├── app.py                            \# Main Python backend  
├── requirements.txt                  \# Python dependencies (Pillow)  
├── Dockerfile                        \# Backend image build instructions  
├── docker-compose.yml                \# Container orchestration (app \+ nginx)  
├── nginx.conf                        \# Nginx configuration  
├── static/                           \# Frontend templates  
│   ├── index.html  
│   ├── form/  
│   │   ├── upload.html  
│   │   └── images.html  
│   └── image-uploader/  
│       ├── css/                      \# Stylesheets  
│       ├── js/                       \# Scripts (upload.js, images.js, index.js)  
│       └── img/                      \# UI images  
├── images/                           \# Docker volume – uploaded pictures storage  
└── logs/                             \# Docker volume – log files (app.log)
```


## **3\. Start and Stop Commands**

### **First start (build and run)**

docker compose up \--build

After successful start you will see logs from both containers.

### **Stop**

Press Ctrl+C in the terminal where the project is running, or execute:

docker compose down

### **Run in background**

docker compose up \-d

Check status: docker compose ps

### **Full cleanup (including volumes with images and logs)**

docker compose down \-v

### **View backend logs**

docker compose logs app

## **4\. Routes and Functionality**

### **Access URLs**

| URL | Purpose |
| :---- | :---- |
| http://localhost:8080 | Main page (frontend) |
| http://localhost:8080/upload.html | Image upload page |
| http://localhost:8080/images.html | List of uploaded images |
| http://localhost:8000 | Backend (welcome message) |

### 

### **Backend API (accessible via Nginx on port 8080 or directly on port 8000\)**

#### **GET /**

Returns a text greeting with usage instructions.

#### **POST /upload**

Uploads an image to the server. Parameters: multipart/form-data, field file.

**Limits**:

* File size ![][image1] 5 MB  
* Allowed extensions: .jpg, .jpeg, .png, .gif  
* Actual content must be a valid image (Pillow verification)

Success response (200):

{  
  "status": "success",  
  "message": "File uploaded successfully",  
  "filename": "1706123456\_abc12345.jpg",  
  "url": "http://localhost:8080/images/1706123456\_abc12345.jpg"  
}

Error responses:

* **400** – unsupported format / file too large / missing file field  
* **415** – extension is allowed but content is not a valid image  
* **500** – internal server error

#### **/images/**

Direct image serving by Nginx. *Example*: http://localhost:8080/images/1706123456\_abc12345.jpg

### **Frontend (UI)**

* **Main page (/)** – randomly shows one of five images; button "Tail‑ent Showcase" leads to upload page.  
* **Upload page (/upload.html)** – select file via button or drag & drop; after successful upload shows the link and a COPY button; automatically saves record in localStorage for the list view.  
* **Images list page (/images.html)** – displays a table of all uploaded files with names and direct links; allows deletion of entries from the list (from localStorage).

## **5\. Notes**

* Uploaded images are stored in the Docker volume images and persist across container restarts.  
* Logs are written to the volume logs (file app.log) in the format:  
  \[2025-06-05 18:46:23\] INFO: Success: image 1706123456\_abc12345.jpg uploaded (original: photo.jpg)

* All errors (format, size, invalid content) are returned as JSON with a clear message and shown to the user via pop‑up alerts.  
* For CORS compatibility, the backend returns the header Access-Control-Allow-Origin: \*.

## 

## **6\. Verification**

1. Open http://localhost:8080 – you should see the main page with a random image.  
2. Click "Tail‑ent Showcase" – you will be redirected to the upload page.  
3. Select a valid .jpg/.png/.gif file (![][image1] 5 MB) – after upload, a link will appear.  
4. Click "COPY" – the link is copied to clipboard.  
5. Switch to the "Images" tab – you will see the list of uploaded files; links open the images in the browser.  
6. Try to upload a text file renamed to test.jpg – you should receive the message: Error: File content is not a valid image. Only JPEG, PNG, GIF are allowed.

## 

## **7\. Troubleshooting**

| Issue | Solution |
| :---- | :---- |
| Ports 8000 or 8080 already in use | Stop other applications or change ports in docker-compose.yml |
| Styles do not load | Clear browser cache (Ctrl+Shift+Delete) and refresh the page |
| Error 413 Request Entity Too Large | Ensure there is no client\_max\_body\_size line in nginx.conf (size limit is handled only by the backend) |
| Cannot access localhost:8000 | Verify that docker-compose.yml contains ports: \- "8000:8000" for the app service |

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAZCAYAAAA4/K6pAAAAiElEQVR4XmNgGAX0BQoKCp3y8vL/0cUJAqDGXSCNMjIynOhyeAFQ00OojczocngBUNMvcpzKCNIExB/RJQgCOTk5G6iNjOhyJAGyAwsdAA3phnpHEl2OJAB0UQTIICBtji5HElBUVNSDGhSBLkcSkJaWFiYneocCUFJS4gcmpkfEYnT9o4BCAABYEymt2Ee2aAAAAABJRU5ErkJggg==>