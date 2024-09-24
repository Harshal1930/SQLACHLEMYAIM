import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_welcome_email(to_email: str, username: str, password: str):
    # Email configuration
    smtp_server = "smtp.mailtrap.io"  # Replace with your SMTP server
    smtp_port = 587  # For TLS
    smtp_user = "ce6c92225d3572"  # Replace with your email
    smtp_password = "995787ecae6960"  # Replace with your email password

    from_email = "harshal.mahajan@example.com"  # Replace with the desired "From" email address
    subject = "Welcome to Our Service"
    body = (
        f"Hello {username},\n\n"
        f"Welcome to our service! We are glad to have you with us.\n\n"
        f"Your login credentials are as follows:\n"
        f"Username: {username}\n"
        f"Password: {password}\n\n"
        f"Best regards,\nThe Team"
    )

    # Create email message
    msg = MIMEMultipart()
    msg['From'] = from_email  # Set the "From" address to the desired email address
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")