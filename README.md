# Nebula Pro
Nebula Pro v 18.1 ` Python Pioneer ` 

 
Nebula Pro Agenda Application - Highly secure organizer in Python

Overview
Nebula Pro is a dynamic, encrypted Tkinter-based desktop agenda application that runs secure in memory and is designed to manage and organize events effectively.
The application includes features for adding, editing, viewing, searching, and deleting events in an intuitive and user-friendly interface.
It syncs with google drive and there is an alert system for appointments you can run in the background.
The visualizer included will help you visualize your appointments.

Nebula PRO is a highly secure Python-based organizer designed for professional and personal use. 
It offers robust encryption, cloud integration, and an intuitive GUI to manage your agenda securely.

AES encryption with user-defined passwords.
Securely stores sensitive files like credentials.json and token.json.
Automatic encryption/decryption during program startup and shutdown.

Supports Google Drive for cloud upload and restoration.
Automatically sync your agenda for easy access.

Multi-tab layout with options to view, add, edit, delete, and search events.
Customizable themes and styles for an enhanced user experience.

Guided setup to generate and secure a password.
Auto-detection of encryption keys and validation mechanisms

Analyze agenda data using a separate visualizer (Nebula Visualizer.py).
Built-in calendar for easy date selection.
Multi-selection mode for efficient management of multiple entries.


First-Time Setup: Launch NebulaPro.py Please note the source is obfuscated version, for an extra layer of security.

Follow the on-screen prompts to create a password and generate an encryption key.
Store your encryption key securely; it is essential for accessing your data.



Event Management:

Add events with descriptions, dates, and times.
Edit or delete events as needed.
Search events by keyword or date.
Cloud Features:

Use "Cloud Upload" to save your agenda to Google Drive.
Restore your agenda with "Cloud Restore."
Shutdown:

Upon exiting, all sensitive files are automatically encrypted, memory is wiped where applicable.



Password Handling: The application uses strong cryptographic practices (PBKDF2HMAC with SHA256 for key derivation and AES encryption via Fernet). 
These are industry standards and considered secure.
File Validation: The validate_salt_file() function ensures the integrity of the salt file by comparing checksums, which is good for preventing tampering.
Sensitive Data Protection: Critical files (token.json, credentials.json, encryption.key) are encrypted on shutdown, reducing exposure risk.
Key Derivation: Uses PBKDF2 with a 100,000 iteration count, which is standard for deriving keys securely.
Encryption Algorithm: Relies on Fernet (AES with a 128-bit key in CBC mode and HMAC for integrity). This ensures data confidentiality and authenticity.

Sensitive data is only stored in encrypted form.
Use secure_zero_memory() consistently for all sensitive data (e.g., passwords and decrypted agenda) to minimize memory exposure risks.

The databank is parsed JSON and accessed through Threading,extensive error handling and should handle big data well enough for an organizer.


Features:

Add Events
Easily add events by specifying a date, time, and description using the integrated calendar and input fields.

View Agenda
Displays a comprehensive list of all scheduled events in a table view. Events can be sorted by date, time, or description.

Edit Events
Allows modification of existing events by selecting and updating event details.

Delete Events
Delete individual events or selected events.
Delete all events on a specified date.
Clear the entire agenda.

Search Events
Search for events based on keywords in their date, time, or description fields.

Reload Button
Restart the application seamlessly for refreshing the session.

Persistent Storage
Automatically saves events to a file (userdata/nebula-agenda.txt) and reloads them upon startup.

About Section
Displays application details, including the developer's website and a count of total entries.

Visualizer:
Run the Visualizer program as well, from the same directory of Nebula to have extra functionality.

Cloud:
If you wish to use the cloud functionality, you will need an AUTH json file, from google, save it in the same directory.  It will save at your google drive.
It will overwrite the same file.
Data is encrypted in the cloud and on your drive. It is not kept insecure in memory nor on your disk.

if you wish to run it as exe 
compile with pyinstaller --hidden-import babel.numbers --hidden-import babel NebulaPro.py

compile the monitor with pyinstaller --onefile --windowed "Nebula Monitor.py"
however an exe has been provided



Before first run, generate your key from the about tab and keep it somewhere secure along your token file and credentials.  Encryption is through AES. 
You can set auto-sync with google drive from the about tab, or sync manually through the button. 
You get the token file after granting permission through google drive, the first time you use the cloud functionality.

 

Monitor:

Nebula Monitor 3.3 has been included.
the monitor will warn only once for each appointment and check each five minutes, it will run continious
,place it in your windows startup folder so it launches on boot!

Both visualizer and monitor included, handle encryption in a secure way. 
Run the visualizer from within the program since, the data is now encrypted, add data before you run the visualizer
You need to setup a password before program launch. 
Your cloud token and credentials are encrypted too.
Your encryptionkey is best saved elsewhere, however, it is encrypted a second time too as extra measure. (use your password to access)
 
 PATCH 12: added multithreading
 
 PATCH 15: improved deletion functionality, GUI, improved stability
 
 PATCH 16: cloud functionality (restore and upload),autoupload
 
 PATCH 17: encrypted data and secured memory.    
 
 PATCH 18:  end of the release cycle, AES lock on program launch , token and credential security, improved encryption security.
 

For improved security obfuscated versions have been provided, these can be compiled too.  Some exes have been provided where possible, compiled errorfree
         pyinstaller --onefile --window
 


Nebula Visualizer v 30.1

Nebula Visualizer is designed to work with Nebula PRO agenda
Nebula Visualizer is a Python-based desktop application designed for visualizing and analyzing agenda data. The application is built using PyQt5 for the GUI and Plotly for data visualization, with added support for asynchronous processing and multithreading to handle large datasets efficiently.

Features
Dashboard Overview: Displays insights such as the total number of appointments, upcoming and historical appointments, and appointment categories.
Interactive Graphs: Includes dynamic, interactive plots for analyzing trends in the data.
Raw Data Viewer: Provides a detailed tabular view of the dataset with vertical and horizontal scrollbars.
Custom Styling: A visually appealing GUI with a cornflower blue background and responsive design.
Efficient Processing:
Multithreading for background data loading to keep the UI responsive.
Asyncio for concurrent data analysis and visualization.
The visualizer now reads the encrypted data.
Generate an encrypted key with Nebula PRO for this program to work.



![Screenshot 2024-12-19 105354](https://github.com/user-attachments/assets/55a2fef5-80f5-4b82-b924-722ea9cd2233)


![Screenshot 2024-12-19 105219](https://github.com/user-attachments/assets/dff3d1e0-653e-4a50-87e7-076505eeec6e)

![Screenshot 2024-12-19 105209](https://github.com/user-attachments/assets/0216635f-ff19-4339-93ac-28343425bcd9)

![Screenshot 2024-12-19 105156](https://github.com/user-attachments/assets/7b3fdd18-156c-434b-ba55-010e29f78e8b)

![Screenshot 2024-12-19 105150](https://github.com/user-attachments/assets/2de53f0d-023b-45c3-8587-5114874f5867)

![Screenshot 2024-12-19 105123](https://github.com/user-attachments/assets/cb9d741f-73b4-480a-81ab-f3dd8003564d)

![Screenshot 2024-12-19 105101](https://github.com/user-attachments/assets/ea58ab11-5ced-43db-a228-d7141061ec28)

![Screenshot 2024-12-19 105055](https://github.com/user-attachments/assets/165ba2c1-722c-4145-a3b8-d47997e38427)

![Screenshot 2024-12-19 105038](https://github.com/user-attachments/assets/5e630249-983a-4b8c-9d2c-bfd16da00ad7)
![Screenshot 2024-12-19 105032](https://github.com/user-attachments/assets/3ff40317-53b0-4ff2-adf3-7c050e020929)
![Screenshot 2024-12-19 105023](https://github.com/user-attachments/assets/3b1bb60d-3f66-4bfc-8fb3-f78c6eade51c)
![Screenshot 2024-12-19 110321](https://github.com/user-attachments/assets/2f8f57fd-654b-4e36-9517-a028c407f52a)
![Screenshot 2024-12-19 110327](https://github.com/user-attachments/assets/c7eabdce-a877-4772-ac24-2bdee2a8f35d)
![Screenshot 2024-12-19 110313](https://github.com/user-attachments/assets/90c7a47d-893c-4800-944e-cf44af002ee1)



If you would like to have the non-obfuscated source code, contact me through my website, and buy me a coffee!
These have been omitted to aid security. 
 
If you enjoy this program, buy me a coffee https://buymeacoffee.com/siglabo
You can use it free of charge or build upon my code. 
 
 
(c) Peter De Ceuster 2024
Software Distribution Notice: https://peterdeceuster.uk/doc/code-terms 

 
 

 

This software is released under the FPA General Code License.
 
   
  
