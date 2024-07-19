import subprocess
import sys
import os
import time


# Function to check if a module is installed
def check_and_install(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install watchdog and python-dotenv if not already installed
check_and_install("watchdog")
check_and_install("dotenv")

from dotenv import load_dotenv, set_key

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Path to the .env file
ENV_FILE_PATH = "C:\\Windows\\.env-YellowCanary"

#Path to event.log file location
EVENT_FILE_PATH = "C:\\Windows\\"

# Function to load or create .env file
def load_or_create_env():
    if os.path.exists(ENV_FILE_PATH):
        load_dotenv(ENV_FILE_PATH)
        print("Variables loaded from .env file.")
        return (
            os.getenv("DIRECTORY_TO_WATCH"),
            os.getenv("SENDER_EMAIL"),
            os.getenv("RECEIVER_EMAIL"),
            os.getenv("EMAIL_PASSWORD"),
            os.getenv("SMTP_SERVER"),
        )
    else:
        directory_to_watch = input("Please enter the directory to monitor: ")
        if not os.path.isdir(directory_to_watch):
            create_dir = input(f"The directory {directory_to_watch} does not exist. Would you like to create it? (yes/no): ").strip().lower()
            if create_dir == 'yes':
                try:
                    os.makedirs(directory_to_watch)
                    print(f"Directory {directory_to_watch} created successfully.")
                except Exception as e:
                    print(f"Failed to create directory: {e}")
                    sys.exit(1)
            else:
                print("Directory not created. Exiting.")
                sys.exit(1)
        #Collect SMTP details
        sender_email = input("Please enter the sender's email address: ")
        receiver_email = input("Please enter the receiver's email address: ")
        password = input("Please enter the sender's email password: ")
        smtp_server = input("Please enter the SMTP server address: ")

        #Write SMTP details to .env file for future use
        with open(ENV_FILE_PATH, 'w') as f:
            f.write(f"DIRECTORY_TO_WATCH={directory_to_watch}\n")
            f.write(f"SENDER_EMAIL={sender_email}\n")
            f.write(f"RECEIVER_EMAIL={receiver_email}\n")
            f.write(f"EMAIL_PASSWORD={password}\n")
            f.write(f"SMTP_SERVER={smtp_server}\n")
        
        return directory_to_watch, sender_email, receiver_email, password, smtp_server

class Watcher:
    def __init__(self, directory_to_watch):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.DIRECTORY_TO_WATCH)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, directory_to_watch):
        self.log_file_path = os.path.join(EVENT_FILE_PATH, 'YellowCanary-events.log')
        self.password_file_path = os.path.join(directory_to_watch, 'passwords.txt')
        self.bankdetails_file_path = os.path.join(directory_to_watch, 'bankdetails.csv')
        self.create_password_file()
        self.create_bankdetails_file()
        
    def create_password_file(self):
        with open(self.password_file_path, 'a') as password_file:
            password_file.write("Admin:Password123\n")

    def create_bankdetails_file(self):
        with open(self.bankdetails_file_path, 'a') as bankdetails_file:
            bankdetails_file.write("Admin,Password123\n")

    def log_event(self, event_type, file_path):
        with open(self.log_file_path, 'a') as log_file:
            log_file.write(f'Event type: {event_type}  Path: {file_path}\n')

    def process(self, event):
        # Ignore changes to events.log
        if event.src_path == self.log_file_path:
            return
        print(f'Event type: {event.event_type}  Path: {event.src_path}')
        self.log_event(event.event_type, event.src_path)
        send_email_alert(event.event_type, event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_opened(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def send_email_alert(event_type, file_path):
    # Email configuration
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"File Alert: {event_type}"
    
    body = f"The file {file_path} was {event_type}"
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == '__main__':
    directory_to_watch, sender_email, receiver_email, email_password, smtp_server = load_or_create_env()
    w = Watcher(directory_to_watch)
    w.run()
