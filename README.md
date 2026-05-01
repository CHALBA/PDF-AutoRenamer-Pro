PDF AutoRenamer Pro
A lightweight and efficient Python-based automation tool designed to rename bulk PDF files automatically by matching their internal text content against a predefined list of customer/vendor names.

Features
Smart Text Matching: Reads the first page of each PDF and matches the content with your target database.

Duplicate Handling: Automatically appends a numeric suffix if a file with the target name already exists in the destination directory.

Suffix Support: Allows you to append dynamic custom tags (e.g., date, batch name) to all processed files.

Clean Naming: Automatically strips out reserved and invalid Windows filename characters.

Prerequisites
Before running the application, make sure you have Python 3.x and the required dependencies installed on your system.

Python 3.x (Download from python.org)

Pip (Comes pre-installed with Python)

Installation
Open your terminal or command prompt and clone or download this repository.

Navigate to the project directory and install the required library:

Bash
pip install pypdf
How to Use
Prepare your files: Ensure all target PDF files are located together in a folder.

Run the script:

Bash
python rename_task.py
Provide Input in Terminal:

Step 1: Enter the full path of your PDF directory.

Step 2: (Optional) Enter extra information/suffix you want to add at the end of the filename. Just press Enter to skip.

Customization
To modify the database of names, open rename_task.py and update the target_names array present in the if __name__ == "__main__": block with your updated client or vendor list.

License
This project is licensed under the MIT License - see the LICENSE file for details.
