# Coding-Questions-Scrapper
### Overview
* It is a python script to scrap coding questions data from [Leetcode](https://leetcode.com/problemset/all/) and upload it to your firebase database. HTML parser Beautiful Soup and firebase SDK have been used achieve this task.

### Screenshots
This what firebase realtime database looks like after uploading Leetcode question to it.

![Firebase Realtime Database](https://github.com/divyeshvala/Coding-Questions-Scrapper/blob/main/screenshots/database.png?raw=True "Firebase Realtime Database")

### How to use it?
Install following packages in your pc -
* beautifulsoup4
* requests
* firebase-admin
* download latest chromedriver (And place it into the driver directory)
* download your firebase admin sdk private key json file and place it in root directory
