# This script was created specifically for registration in the Consensys project forms.

## Running Python Script
This repository contains a Python script that automates the process of filling out a web form using the CapMonster API. To use this script, you will need to have a CapMonster API key and a list of email addresses.

## Installation
Before running the script, you will need to install the required dependencies. You can do this by running the following command in your terminal:

<code>pip install -r requirements.txt</code>

## Configuration
Next, you will need to configure the script by filling in the CAPMONSTER_API_KEY constant in the config.py file. You can find your CapMonster API key in your CapMonster account dashboard.

You will also need to provide a list of email addresses that the script will use to fill out the web form. To do this, create a new file called email.txt in the project directory and add one email address per line.

## Usage
To run the script, simply execute the following command in your terminal:

<code>python main.py</code>

The script will use the CapMonster API to solve any CAPTCHAs on the web form, and then fill out the form using the provided email addresses. Once the script has finished running, you should see a message indicating that the form has been successfully submitted.

If you encounter any errors while running the script, please double-check that you have correctly configured the CAPMONSTER_API_KEY constant and provided a valid list of email addresses in the email.txt file.

That's it! You can now use this script to automate the process of filling out web forms.
