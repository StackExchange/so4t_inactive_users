# Stack Overflow for Teams Inactive Users (so4t_inactive_users)
A Python script that uses the Stack Overflow for Teams API to create inactive user reporting. You can see an example of what the output looks like in the [Examples directory](https://github.com/StackExchange/so4t_inactive_users/blob/main/Examples/inactive_users.csv)).


## Table of Contents
* [Requirements](https://github.com/StackExchange/so4t_inactive_users?tab=readme-ov-file#requirements)
* [Setup](https://github.com/StackExchange/so4t_inactive_users?tab=readme-ov-file#setup)
* [Usage](https://github.com/StackExchange/so4t_inactive_users?tab=readme-ov-file#usage)
* [Support, security, and legal](https://github.com/StackExchange/so4t_inactive_users?tab=readme-ov-file#support-security-and-legal)


## Requirements
* A Stack Overflow for Teams instance (Basic, Business, or Enterprise)
* Python 3.8 or higher ([download](https://www.python.org/downloads/))
* Operating system: Linux, MacOS, or Windows


## Setup

[Download](https://github.com/StackExchange/so4t_inactive_users/archive/refs/heads/main.zip) and unpack the contents of this repository

**Installing Dependencies**

* Open a terminal window (or, for Windows, a command prompt)
* Navigate to the directory where you unpacked the files
* Install the dependencies: `pip3 install -r requirements.txt`

**API Authentication**

For the Basic and Business tiers, you'll need an API token. For Enterprise, you'll need to obtain an API key.

* For Basic or Business, instructions for creating a personal access token (PAT) can be found in [this KB article](https://stackoverflow.help/en/articles/4385859-stack-overflow-for-teams-api).
* For Enterprise, documentation for creating an API key can be found within your instance at this url: `https://[your_site]/api/docs/authentication`


## Usage

In a terminal window, navigate to the directory where you unpacked the script. 
Run the script using the following format, replacing the URL, token, and/or key with your own:
* For Basic and Business: `python3 so4t_inactive_users.py --url "https://stackoverflowteams.com/c/TEAM-NAME" --token "YOUR_TOKEN"`
* For Enterprise: `python3 so4t_inactive_users.py --url "https://SUBDOMAIN.stackenterprise.co" --key "YOUR_KEY"`

As the script runs, it will continue to update the terminal window with its tasks. When the script completes, it will indicate that the reports have been generated, along with the name of the file. 

Three reports are generated:
* `all_users_inactive_for_##_days.csv` - as the name implies, this is all users who have not logged in within the specified number of days
* `contributing_users_inactive_for_##_days.csv` - this is a subset of the `all_users` report and includes only users who have contributed content. The use case for this report is identifying a subset of inactive users who might be adversely impacted if their account was deleted (i.e. they'd lose their user profile, reputation gains, content attribution, etc.)
* `noncontributing_users_inactive_for_##_days.csv` - this is a subset of the `all_users` report, including only users who have *not* contributed any content; in other words, the delta between the `all_users` and `contributing_users` reports. It's likely that these users can be safely deleted, and if they're deleted prematurely (or in error), they can simply register for a new account and create a new user profile without experiencing any loss of reputation points, content attribution, etc.


## Support, security, and legal
If you encounter problems using the script, please open a support issue with Stack Overflow. You can also clone and change the script to suit your needs. It is provided as-is, with no warranty or guarantee of any kind.

All data is handled locally on the device from which the script is run. The script does not transmit data to other parties, such as Stack Overflow. All of the API calls performed are read only, so there is no risk of editing or adding content on your Stack Overflow for Teams instance.
