# CSEL
## Cyberpatriot Scoring Engine: Linux

CSEL is a scoring engine written in bash for scoring Linux CyberPatriot images. It is configured by adding scoring options into the csel.cfg and running the install file. It now includes a web page Score Report. It works (to varying degrees) with Ubuntu 14.04 and 16.04.

## Features
CSEL is still a baby and it's rough around the edges, but so far it can score the following events:
- Disabling the guest login
- Disabling the root login (WIP)
- Creating new users
- Deleting "bad" users
- Changing passwords on accounts
- Adding users to the sudo group (Administrator)
- Removing users from the sudo group(Administrator)
- Adding users to groups
- Removing users from groups
- Creating groups
- Securing /etc/sudoers file
- Disabling autologin
- Disabling usernames on the login page
- Setting the minimum password age
- Setting the maximum password age
- Setting the maximum number of login tries
- Setting the minimum password length
- Setting the maximum number of passwords to remember
- Setting the minimum password complexity
- Setting password history value
- Setting password length
- Installing "good" programs
- Uninstalling "bad" programs
- Deleting prohibited files
- Removing backdoors (malicious services)
- Modifying file permissions
- Enabling the firewall
- Configuring firewall rules
- Securing ssh
- Configuring the hosts files
- Updating the kernel
- Removing things from user crontabs
- Updating clamav virus definitions 
- Removing things from startup
- Answering the forensics question correctly
- Changing update options
- Adding or uncommenting lines from config files
- Deleting or commenting lines from config files
- Install update period
- Install updates automatically

CSEL can also take away points for:
- Removing critical users
- Removing or stopping critical services
- Removing critical programs

CSEL can be run with "silent misses" which simulates a CyberPatriot round where you have no idea where the points are until you earn them. It can also be run with the silent misses turned off which is helpful when you are debugging or when you have very inexperienced students who might benefit from the help. This mode gives you a general idea where the points are missing. CSEL can also create a scoreboard report that can be sent to an FTP server and manaipulated however you please.

## How to install
1. Go to [bitbucket](https://bitbucket.org/coastlinecollege/csel/src/master/configurator) and download this file. The executable contains everything you need to setup a local scoring engine.
2. Run `configurator` as an administrator.
3. Make your adjustments in `configurator` that you want scored.
3. Once finished click `Write to Config` at the top left.
4. After you are satisfied that it is working how you want, you can delete the CSEL directory.

Notes:
To add multiple keywords use spaces not commas
The settings are saved in the csel.txt file

**Important Note**: Your students _will_ be able to see the vulnerabilities if you leave the CSEL folder behind or if they cat the executable file that is created in /usr/local/bin/. I tell my students where the file is and that they should stay away from it. It is practice, after all.

## Known issues and planned updates
- Write a sample explianation for a FTP server
- Update all of the explanations
- Make Readme generator and setting setter (Maybe)