# Yellow-Canary
A Simple Python canary file watcher

# Overview
This Python script is designed to create a set of files and continuously monitor them for any changes. When a change is detected, the script logs the event and sends an email alert to the end user. Currently, this script is available only for Windows, but efforts are underway to port it to an executable (.exe) file and create a Linux variant. The Python script creates 2 canary files (passwords.txt & bankdetails.csv) in the directory of your choice. A log file and .env file is created in C:\Windows and are named .env-YellowCanary & YellowCanary-events.log.

# Features
-File Creation: Generates a set of files in a specified directory.
-File Monitoring: Continuously monitors the files for any changes, such as modifications, deletions, or additions.
-Logging: Logs all detected changes to a log file for later review.
-Email Alerts: Sends email notifications to the end user when a change is detected.
-.env file: This file stores configuration settings

# Requirements
Python 3.x
Windows OS
Required Python packages: watchdog, smtplib, subprocess, dotenv, time libraries.

# Installation
Clone the Repository


```
git clone https://github.com/yourusername/file-monitoring-script.git
cd file-monitoring-script
```

# Install Dependencies

Use pip to install the necessary Python packages:

```
pip install watchdog
pip install dotenv
```

# Configure the Script

Open the script YellowCanary.py and configure the following settings:

directory_to_monitor: The path of the directory where the files will be created and monitored.
email_settings: Configure your email settings, such as SMTP server, port, sender email, receiver email, and password.

# Usage

Run the Script

Execute the script to start creating files and monitoring them:

YellowCanary.py
Monitor the Log File

The script will create a log file named YellowCanary-events.log in the Windows directory, where all changes will be recorded.

# Email Alerts
Ensure that your email settings are correctly configured in the script to receive email alerts. The script uses the smtplib and email libraries to send notifications.

# Future Plans
Executable File: We are in the process of porting this script to an executable (.exe) file for easier deployment on Windows systems.
Linux Support: A Linux variant of this script is also under development to extend support to other operating systems.

# Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact
For any questions or support, please contact Eric Lemire at eric[dot]lemire@mail[dot]com.
