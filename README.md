# 📩 Certificate Sender - Streamlit App

This Streamlit application allows you to **send a single PDF certificate to multiple participants** listed in a CSV file. Each participant receives the same file via email with a customized message.

> ✅ Built for university events, workshops, or any group where every participant gets the same certificate.

---

## 🚀 Features

- 📤 Upload a common PDF certificate.
- 📑 Upload a CSV file with participant **Name** and **Email**.
- 💬 Add a personalized message for all recipients.
- 📧 Emails are sent automatically using Gmail.
- 📊 Progress bar and success/failure tracking.
- ✅ Easy-to-use Streamlit interface.

---

## 📁 CSV Format

Your CSV file should have exactly **two columns**: `Name` and `Email`.  
Example:

```csv
Name,Email
toqeer azam,toqeerazam.1545@gmail.com
```
# Certificate Sender App

A Streamlit application to send certificates via email with Gmail SMTP.

## 📦 Install Requirements
Before running the app, make sure to install the required Python packages:

```bash
pip install streamlit pandas
