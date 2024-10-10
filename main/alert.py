import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailAlert:
    """
    A class to send email alerts with attachments.
    
    Attributes:
    ----------
    user_email_address1 : str
        Primary user email address.
    user_email_address2 : str
        Secondary user email address.
    user_email_address3 : str
        Tertiary user email address.

    Methods:
    -------
    send_email_alert(toaddr, filename, absulutefilepath):
        Sends an email with a video file attachment to the specified address.
    """
    
    def __init__(self, users_email_list=None):
        if users_email_list is None:
            users_email_list = ["amitos684@gmail.com", "barloupo@gmail.com", "eyal@gat.org.il"]
        
        self.user_email_address1 = users_email_list[0]
        self.user_email_address2 = users_email_list[1]
        self.user_email_address3 = users_email_list[2]

    def send_email_alert(self, toaddr, filename, absulutefilepath):
        """
        Sends an email with an alert and attaches a video file.
        
        Parameters:
        ----------
        toaddr : str
            Recipient email address.
        filename : str
            Name of the video file.
        absulutefilepath : str
            Absolute path to the video file to be attached.
        """

        print(f"Sending email to: {toaddr}")
        print(f"Attaching file: {filename}")
        print(f"File path: {absulutefilepath}")

        fromaddr = "absabusedetection@gmail.com"
        # Use environment variables to securely store your email password.
        password = os.getenv("EMAIL_PASSWORD")

        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the sender's email address
        msg['From'] = fromaddr

        # storing the receiver's email address
        msg['To'] = toaddr

        # storing the subject
        msg['Subject'] = "ADS Alert"

        # Email body
        body = f"Hello,\nADS Alert: Warning, we found the following video to contain abuse.\nTime: {datetime.now()}"

        # Attach the body to the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # Attach the video file
        try:
            with open(absulutefilepath, "rb") as attachment:
                # Create MIMEBase instance
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())

                # Encode the file in base64
                encoders.encode_base64(p)

                # Add header for the attachment
                p.add_header('Content-Disposition', f"attachment; filename= {filename}")

                # Attach the file to the message
                msg.attach(p)

        except FileNotFoundError:
            print(f"Error: File {absulutefilepath} not found.")
            return

        # Create SMTP session and send the email
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)

            # Start TLS for security
            s.starttls()

            # Authentication
            s.login(fromaddr, password)

            # Convert the MIMEMultipart msg into a string
            text = msg.as_string()

            # Send the email
            s.sendmail(fromaddr, toaddr, text)
            print(f"[+][+] Email sent successfully to {toaddr}\n")

        except smtplib.SMTPException as e:
            print(f"Error: Unable to send email. {e}")

        finally:
            # Terminate the SMTP session
            s.quit()
