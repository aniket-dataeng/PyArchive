**Project Name:** PyBak<br>

**Objective:**
PyBak is a professional, automated file backup and compression solution that periodically scans a source directory, compresses files using GZIP, and moves them to a destination directory. It integrates with cloud
storage, uses a REST API for remote control, and employs multithreading for optimized performance.

**Project Scope**
**Core Functionality:**
- PyBak will have two directories:
 1. Source Directory - Where files arrive.
 2. Destination Directory - Where compressed files are stored.
- Uses GZIP compression to reduce file size.
- Compressed files follow the naming format: filename_timestamp.gz.
- Duplicate files are discarded if they already exist in the source directory.
- Maintains a log file and generates a report of compressed files.
- Sends reports via email to designated recipients.
- Runs every 2 minutes, scanning for new files, compressing them, and moving them to the destination directory.

**Advanced Features**
1 **Cloud Integration**
- Support for AWS S3 and Google Cloud Storage (GCS).
PyBak - Advanced Project Document
- Option to upload compressed files directly to cloud storage.
2 **Performance Optimization**
- Implements multithreading/multiprocessing for faster file processing.
- Allows parallel compression of multiple files.
3 **Database Integration**
- Uses SQLite/PostgreSQL to track processed files.
- Stores metadata (filename, size, timestamp, hash) for each compressed file.
4 **REST API for Remote Triggering**
- Uses FastAPI to expose endpoints:
 - `/compress` Triggers file compression.
 - `/status` Displays active jobs.
 - `/logs` Retrieves logs.
5 **Deployment & CI/CD**
- Dockerized application for portability.
- GitHub Actions to automate testing and deployment.
- Runs on Kubernetes for scalability.
6 **Logging & Monitoring**
- Logs stored in a database instead of plain text.
- Flask/Dash web UI for visualization and monitoring.
7 **Security & Encryption**
- AES-256 encryption for compressed files.
- OAuth-protected API for secure access.
---
PyBak - Advanced Project Document
Deployment & Execution
- Runs every 2 minutes via cron job (Linux) or Windows Task Scheduler.
- Uses SMTP/Gmail integration for email reporting.
- Can be executed manually with command-line arguments.
- Configurable settings via YAML/JSON.
---
Future Enhancements
- Support for additional compression formats (ZIP, TAR, etc.).
- Implement a REST API to trigger jobs remotely.
- Add cloud storage integration (AWS S3, Google Drive, etc.) for remote backups.


