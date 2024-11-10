# email_utils/email_sender.py
"""
Module to handle sending emails.
"""

import os
import logging
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz





# Set up logging
logger = logging.getLogger(__name__)

def send_email(sender_email, sender_password, recipient_email, subject, message, resume_path):
    """
    Sends an email with an attachment.
    
    Args:
        sender_email (str): Sender's email address.
        sender_password (str): Sender's email password.
        recipient_email (str): Recipient's email address.
        subject (str): Email subject.
        message (str): Email body message.
        company_name (str): Name of the company.
    """
    resume_filename = resume_path.split('\\')[-1]  # Update as necessary
    print("OSPath", os.getcwd(), resume_filename)
    # resume_path = os.path.join("/", resume_filename)
    print("resume_path:", resume_path)
    logger.info(f"Sending email to: {recipient_email}")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        print(f"E: -{sender_email}- | -{sender_password}-")
        server.login(sender_email, sender_password)
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        # msg.attach(MIMEText(message, 'plain'))
        msg.attach(MIMEText(message, 'html')) # uncomment if you want your message to be formatted
        
        with open(resume_path, 'rb') as file:
            resume_attachment = MIMEApplication(file.read(), Name=resume_filename)
        resume_attachment['Content-Disposition'] = f'attachment; filename="{resume_filename}"'
        msg.attach(resume_attachment)
        
        server.sendmail(sender_email, recipient_email, msg.as_string())
        logger.info(f"Email sent successfully to {recipient_email}")

        # # Log successfully sent email address to a text file
        # print("HAHHA", os.getcwd())
        # success_log_file = f"history/{scenario}/{company_name}_successfully_sent_emails.txt"
        # # Define US Eastern Standard Time timezone
        # est = pytz.timezone('America/New_York')

        # # Get the current date and time in EST
        # current_est_time = datetime.now(est)

        # # Format to only get the date if needed
        # current_est_date = current_est_time.date()

        # print("Current EST Date and Time:", current_est_time)
        # print("Current EST Date:", current_est_date)
        # with open(success_log_file, 'a') as file:
        #     file.write(recipient_email + f',{scenario},{str(current_est_date)}' '\n')

        server.quit()
    except Exception as e:
        logger.error("Error sending email:", exc_info=True)
        raise e