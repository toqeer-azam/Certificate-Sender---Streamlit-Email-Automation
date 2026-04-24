import os
import pandas as pd
import smtplib
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import time

# Email credentials and SMTP server configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'add email'  # Replace with your email
EMAIL_PASSWORD = 'add your app password'    # Use Gmail App Password here

def send_email(to_address, participant_name, certificate_path, custom_message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = 'Your Certificate of Participation'

    body = f"Dear {participant_name},\n\n{custom_message}\n\nBest regards,\nBuitems Developers Club"
    msg.attach(MIMEText(body, 'plain'))

    # Attach certificate
    part = MIMEBase('application', 'octet-stream')
    with open(certificate_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(certificate_path)}')
    msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_address, msg.as_string())
        return 'Success'
    except Exception as e:
        return f'Failed: {e}'

# Streamlit UI
st.title('Send Common Certificate to All Participants')

csv_file = st.file_uploader('Upload CSV with Name and Email', type=['csv'])
certificate_file = st.file_uploader('Upload the Common Certificate (PDF)', type=['pdf'])
custom_message = st.text_area('Enter your message for all participants', value='Congratulations on your participation!')

if st.button('Send Certificates'):
    if not csv_file or not certificate_file or not custom_message:
        st.error('Please upload CSV, Certificate, and enter a message.')
    else:
        df = pd.read_csv(csv_file)
        df['Email'] = df['Email'].astype(str)
        df['Name'] = df['Name'].astype(str)

        total = len(df)
        success_count = 0
        failed_list = []
        progress = st.progress(0)

        # Save uploaded certificate to a temporary location
        cert_temp_path = f'temp_certificate.pdf'
        with open(cert_temp_path, 'wb') as f:
            f.write(certificate_file.read())

        for i, row in df.iterrows():
            name = row['Name'].strip()
            email = row['Email'].strip()

            result = send_email(email, name, cert_temp_path, custom_message)
            if result == 'Success':
                success_count += 1
            else:
                failed_list.append(f'{name} ({email}): {result}')

            progress.progress(int(((i + 1) / total) * 100))
            time.sleep(1)

        os.remove(cert_temp_path)

        st.success(f'✅ Sent: {success_count}/{total} certificates')
        if failed_list:
            st.warning('❌ Failed to send to:')
            for fail in failed_list:
                st.write(f'- {fail}')
