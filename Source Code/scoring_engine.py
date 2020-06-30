import json
import os
import re
import time
from tkinter import messagebox
from datetime import date


# Scoring Report creation
def draw_head():
    f = open(scoreIndex, 'w+')
    f.write('<!doctype html><html><head><title>CSEL Score Report</title><meta http-equiv="refresh" content="60"></head><body style="background-color:powderblue;">''\n')
    f.write('<table align="center" cellpadding="10"><tr><td><img src="/usr/local/CyberPatriot/CCC_logo.png"></td><td><div align="center"><H2>Cyberpatriot Scoring Engine:Linux v3.0</H2></div></td><td><img src="/usr/local/CyberPatriot/SoCalCCCC.png"></td></tr></table><br><H2>Your Score: #TotalScore#/#PossiblePoints#</H2><H2>Vulnerabilities: #TotalVuln#/#PossibleVuln#</H2><hr>')
    f.close()


def record_hit(name, points, message):
    global total_points, possible_points
    global total_vulnerabilities, possible_vulnerabilities
    write_to_html(('<p style="color:green">' + name + ' (' + str(points) + ' points)</p>'))
    total_points += int(points)
    possible_points += int(points)
    total_vulnerabilities += 1
    possible_vulnerabilities += 1


def record_miss(name, points):
    global possible_points, possible_vulnerabilities
    possible_points += int(points)
    possible_vulnerabilities += 1
    if not save_dictionary["Main Menu"]['Silent Mode'] == 1:
        write_to_html(('<p style="color:red">MISS ' + name + ' Issue</p>'))


def record_penalty(name, points, message):
    global total_points
    write_to_html(('<p style="color:red">' + name + ' (' + str(points) + ' points)</p>'))
    total_points -= int(points)


def draw_tail():
    write_to_html('<hr><div align="center"><b>Coastline Collage</b><br>Created by Shaun Martin, Anthony Nguyen, and Minh-Khoi Do</br><br>Feedback welcome: <a href="mailto:smartin94@student.cccd.edu?Subject=CSEL Scoring Engine" target="_top">smartin94@student.cccd.edu</a></div>')
    print(str(total_points) + ' / ' + str(possible_points) + '\n' + str(total_vulnerabilities) + ' / ' + str(possible_vulnerabilities))
    replace_section(scoreIndex, '#TotalScore#', str(total_points))
    replace_section(scoreIndex, '#PossiblePoints#', str(possible_points))
    replace_section(scoreIndex, '#TotalVuln#', str(total_vulnerabilities))
    replace_section(scoreIndex, '#PossibleVuln#', str(possible_vulnerabilities))
    if not os.path.exists(os.path.join(Desktop, "ScoreReport.html")):
        os.system('#!/bin/bash \ncd ' + Desktop + ' \nln /usr/local/CyberPatriot/ScoreReport.html')


# Extra Functions
def check_runas():
    if os.getuid() != 0:
        messagebox.showerror('Administrator Access Needed', 'Please make sure the scoring engine is running as admin. If this message keeps showing please contact the distributors.')
        exit()


def check_score():
    global total_points
    global prePoints
    if total_points > prePoints:
        prePoints = total_points
        os.system("notify-send 'You gained points!!'")
    elif total_points < prePoints:
        prePoints = total_points
        os.system("notify-send 'You lost points!!'")
    if total_points == possible_points:
        time.sleep(5)
        os.system("notify-send 'Congratulations you finished the image.'")


def write_to_html(message):
    f = open(scoreIndex, 'a')
    f.write(message)
    f.close()


def replace_section(loc, search, replace):
    lines = []
    with open(loc) as file:
        for line in file:
            line = line.replace(search, replace)
            lines.append(line)
    with open(loc, 'w') as file:
        for line in lines:
            file.write(line)


# Option Check
def forensic_question():
    for idx, path in enumerate(save_dictionary["Forensic"]["Location"]):
        f = open(path, 'r')
        content = f.read().splitlines()
        for c in content:
            if 'ANSWER:' in c:
                if save_dictionary["Forensic"]["Categories"]["Answer"][idx] in c:
                    record_hit('Forensic question number ' + str(idx + 1) + ' has been answered.', save_dictionary["Forensic"]["Categories"]['Points'][idx], '')
                else:
                    record_miss('Forensic Question', save_dictionary["Forensic"]["Categories"]['Points'][idx])


def disable_guest():
    if os.path.exists("/etc/lightdm/lightdm.conf.d/50-ubuntu.conf"):
        filename = "/etc/lightdm/lightdm.conf.d/50-ubuntu.conf"
    elif os.path.exists("/etc/lightdm/lightdm.conf"):
        filename = "/etc/lightdm/lightdm.conf"
    f = open(filename, 'r')
    content = f.read()
    f.close()
    if 'allow-guest=false' in content:
        record_hit('The guest account haas been disabled.', save_dictionary["Account Management"]["Disable Guest"]["Categories"]['Points'][0], '')
    else:
        record_miss('User Management', save_dictionary["Account Management"]["Disable Guest"]["Categories"]['Points'][0])


def turn_on_firewall():
    if os.system("ufw status | grep 'Status: active'") == 0:
        record_hit('Firewall has been turned on.', save_dictionary["Policy Options"]["Turn On Firewall"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Policy Options"]["Turn On Firewall"]["Categories"]['Points'][0])
    return


def minimum_password_age():
    if 30 <= current_settings["Minimum Password Age"] <= 60:
        record_hit('Minimum password age is set to 30-60.', save_dictionary["Password Policy"]["Minimum Password Age"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Password Policy"]["Minimum Password Age"]["Categories"]['Points'][0])


def maximum_password_age():
    if 60 <= current_settings["Maximum Password Age"] <= 90:
        record_hit('Maximum password age is set to 60-90.', save_dictionary["Password Policy"]["Maximum Password Age"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Password Policy"]["Maximum Password Age"]["Categories"]['Points'][0])


def maximum_login_tries():
    if 5 <= current_settings["Maximum Login Tries"] <= 10:
        record_hit('Maximum login tries is set to 5-10.', save_dictionary["Password Policy"]["Maximum Login Tries"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Password Policy"]["Maximum Login Tries"]["Categories"]['Points'][0])


def minimum_password_length():
    if current_settings["Minimum Password Length"] >= 10:
        record_hit('Minimum password length is set to 10-29.', save_dictionary["Password Policy"]["Minimum Password Length"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Password Policy"]["Minimum Password Length"]["Categories"]['Points'][0])


def password_history():
    if current_settings["Password History"] >= 5:
        record_hit('Password history size is set to 5-10.', save_dictionary["Password Policy"]["Password History"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Password Policy"]["Password History"]["Categories"]['Points'][0])


def password_complexity():
    if current_settings["Password Complexity"] == -3:
        record_hit('Password complexity has been enabled.', save_dictionary["Password Policy"]["Password Complexity"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Password Policy"]["Password Complexity"]["Categories"]['Points'][0])


def disable_user_greeter():
    if os.path.exists("/etc/lightdm/lightdm.conf.d/50-ubuntu.conf"):
        filename = "/etc/lightdm/lightdm.conf.d/50-ubuntu.conf"
    elif os.path.exists("/etc/lightdm/lightdm.conf"):
        filename = "/etc/lightdm/lightdm.conf"
    f = open(filename, 'r')
    content = f.read()
    f.close()
    if 'greeter-hide-users=true' in content:
        record_hit('User Greeter has been disabled.', save_dictionary["Policy Options"]["Disable User Greeter"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Policy Options"]["Disable User Greeter"]["Categories"]['Points'][0])


def disable_auto_login():
    if os.path.exists("/etc/lightdm/lightdm.conf.d/50-ubuntu.conf"):
        filename = "/etc/lightdm/lightdm.conf.d/50-ubuntu.conf"
    elif os.path.exists("/etc/lightdm/lightdm.conf"):
        filename = "/etc/lightdm/lightdm.conf"
    f = open(filename, 'r')
    content = f.read()
    f.close()
    if not re.search('autologin-user=.+', content):
        record_hit('Auto Login has been enabled.', save_dictionary["Policy Options"]["Disable Auto Login"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Policy Options"]["Disable Auto Login"]["Categories"]['Points'][0])


def keep_user():
    for idx, name in enumerate(save_dictionary["Account Management"]["Keep User"]["Categories"]['User Name']):
        if os.system('getent passwd ' + name.lower()) > 0:
            record_penalty(name + ' was removed.', save_dictionary["Account Management"]["Keep User"]["Categories"]['Points'][idx], '')


def add_user():
    for idx, name in enumerate(save_dictionary["Account Management"]["Add User"]["Categories"]['User Name']):
        if os.system('getent passwd ' + name.lower()) == 0:
            record_hit(name + ' has been added', save_dictionary["Account Management"]["Add User"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Add User"]["Categories"]['Points'][idx])


def remove_user():
    for idx, name in enumerate(save_dictionary["Account Management"]["Remove User"]["Categories"]['User Name']):
        if os.system('getent passwd ' + name.lower()) > 0:
            record_hit(name + ' has been removed.', save_dictionary["Account Management"]["Remove User"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Remove User"]["Categories"]['Points'][idx])


def add_admin():
    for idx, name in enumerate(save_dictionary["Account Management"]["Add Admin"]["Categories"]['User Name']):
        if os.system('getent group sudo | grep ' + name.lower()) == 0:
            record_hit(name + ' has been promoted to administrator.', save_dictionary["Account Management"]["Add Admin"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Add Admin"]["Categories"]['Points'][idx])


def remove_admin():
    for idx, name in enumerate(save_dictionary["Account Management"]["Remove Admin"]["Categories"]['User Name']):
        if os.system('getent group sudo | grep ' + name.lower()) > 0:
            record_hit(name + ' has been demoted to standard user.', save_dictionary["Account Management"]["Remove Admin"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["Remove Admin"]["Categories"]['Points'][idx])


def add_user_to_group():
    for idx, name in enumerate(save_dictionary["Account Management"]['Add User to Group']["Categories"]['Group Name']):
        if os.system('getent group ' + name.lower() + ' | grep ' + save_dictionary["Account Management"]['Add User to Group']["Categories"]['User Name'][idx].lower()) == 0:
            record_hit(save_dictionary["Account Management"]['Add User to Group']["Categories"]['User Name'][idx] + ' is in the ' + name + ' group.', save_dictionary["Account Management"]['Add User to Group']["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]['Add User to Group']["Categories"]['Points'][idx])


def remove_user_from_group():
    for idx, name in enumerate(save_dictionary["Account Management"]['Remove User from Group']["Categories"]['Group Name']):
        if os.system('getent group ' + name.lower() + ' | grep ' + save_dictionary["Account Management"]['Remove User from Group']["Categories"]['User Name'][idx].lower()) > 0:
            record_hit(save_dictionary["Account Management"]['Remove User from Group']["Categories"]['User Name'][idx] + ' is no longer in the ' + name + ' group.', save_dictionary["Account Management"]['Remove User from Group']["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]['Remove User from Group']["Categories"]['Points'][idx])


def user_change_password():
    current_date = date.today().strftime("%b %d, %Y")
    for idx, name in enumerate(save_dictionary["Account Management"]["User Change Password"]["Categories"]['User Name']):
        if current_date in current_settings["Current Password " + name]:
            record_hit(name + '\'s password was changed.', save_dictionary["Account Management"]["User Change Password"]["Categories"]['Points'][idx], '')
        else:
            record_miss('User Management', save_dictionary["Account Management"]["User Change Password"]["Categories"]['Points'][idx])


def check_startup():
    for idx, program in enumerate(save_dictionary["Miscellaneous"]["Check Startup"]["Categories"]['Program Name']):
        os.system('ls /etc/ > startup')
        f = open('startup')
        startup_file = f.read().splitlines()
        for file in startup_file:
            if re.search('rc.\.d', file):
                if not os.path.exists('/etc/' + file + program):
                    record_hit('Program Removed from Startup', save_dictionary["Miscellaneous"]["Check Startup"]["Categories"]['Points'][idx], '')
                else:
                    record_miss('Program Management', save_dictionary["Miscellaneous"]["Check Startup"]["Categories"]['Points'][idx])


def update_check_period():
    if current_settings["Update Check Period"] == 1:
        record_hit('Update check period is set to 1 in /etc/apt/apt.conf.d/10periodic.', save_dictionary["Miscellaneous"]["Update Check Period"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Miscellaneous"]["Update Check Period"]["Categories"]['Points'][0])


def update_auto_install():
    if current_settings["Update Auto Install"] == 1:
        record_hit('Updates set to 1 in /etc/apt/apt.conf.d/10periodic.', save_dictionary["Miscellaneous"]["Update Auto Install"]["Categories"]['Points'][0], '')
    else:
        record_miss('Policy Management', save_dictionary["Miscellaneous"]["Update Auto Install"]["Categories"]['Points'][0])


def cron_tab():
    for idx, name in enumerate(save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["User Name"]):
        if os.system('crontab -u ' + name + ' -l | grep ^# | grep ' + save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["Task Name"][idx]) == 0:
            record_hit('Cron job ' + save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["Task Name"][idx] + ' in ' + name + ' has been commented out.', save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["Points"][idx], '')
        else:
            if os.system('crontab -u ' + name + ' -l | grep ' + save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["Task Name"][idx]) > 0:
                record_hit('Cron job ' + save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["Task Name"][idx] + ' in ' + name + ' has been deleted.', save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["Points"][idx], '')
            else:
                record_miss('Program Management', save_dictionary["Miscellaneous"]["Cron Tab"]["Categories"]["Points"][idx])


def secure_sudoers():
    for idx, name in save_dictionary["Account Management"]["Secure Sudoers"]["Categories"]["User Name"]:
        if os.system('cat /etc/sudoers | grep ' + name) > 0:
            record_hit(name + ' has been removed from the /etc/sudoers file.', save_dictionary["Account Management"]["Secure Sudoers"]["Categories"]["Points"][idx], '')
        else:
            record_miss('Account Management', save_dictionary["Account Management"]["Secure Sudoers"]["Categories"]["Points"][idx])


def add_text_to_file():
    for idx, file in enumerate(save_dictionary["File Management"]["Add Text to File"]["Categories"]['File Path']):
        if os.system('cat ' + file + ' | grep ' + save_dictionary["File Management"]["Add Text to File"]["Categories"]['Text to Add'][idx]) == 0:
            record_hit(save_dictionary["File Management"]["Add Text to File"]["Categories"]['Text to Add'][idx] + ' has been added to ' + file, save_dictionary["File Management"]["Add Text to File"]["Categories"]['Points'][idx], '')
        else:
            record_miss('File Management', save_dictionary["File Management"]["Add Text to File"]["Categories"]['Points'][idx])


def remove_text_from_file():
    for idx, file in enumerate(save_dictionary["File Management"]["Remove Text From File"]["Categories"]['File Path']):
        if os.system('cat ' + file + ' | grep ' + save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Text to Remove'][idx]) > 0:
            record_hit(save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Text to Remove'][idx] + ' has been removed from ' + file, save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Points'][idx], '')
        else:
            record_miss('File Management', save_dictionary["File Management"]["Remove Text From File"]["Categories"]['Points'][idx])


def check_hosts():
    for idx, item in enumerate(save_dictionary["File Management"]["Check Hosts"]["Categories"]['Text']):
        if os.system('grep ' + item + ' /etc/hosts') > 0:
            record_hit(item + ' removed from /etc/hosts.', save_dictionary["File Management"]["Check Hosts"]["Categories"]['Points'][idx], '')
        else:
            record_miss('File Management', save_dictionary["File Management"]["Check Hosts"]["Categories"]['Points'][idx])


def services():
    for idx, name in save_dictionary["Program Management"]["Service"]["Categories"]['Service Name']:
        if os.system('systemctl status ' + name + ' | grep "(' + save_dictionary["Program Management"]["Service"]["Categories"]['Service Status'][idx] + ')"'):
            record_hit(name + ' has been set to ' + save_dictionary["Program Management"]["Service"]["Categories"]['Service Status'][idx], save_dictionary["Program Management"]["Service"]["Categories"]['Points'][idx], '')
        else:
            record_miss('Program Management', save_dictionary["Program Management"]["Service"]["Categories"]['Points'][idx])


def good_program():
    for idx, program in save_dictionary["Program Management"]["Good Program"]["Categories"]['Program Name']:
        if os.system('apt-cache policy ' + program + ' | grep "Installed: (none)"') > 0:
            record_hit(program + ' is installed', save_dictionary["Program Management"]["Good Program"]["Categories"]['Points'][idx], '')
        else:
            record_miss('Program Management', save_dictionary["Program Management"]["Good Program"]["Categories"]['Points'][idx])


def bad_program():
    for idx, program in enumerate(save_dictionary["Program Management"]["Bad Program"]["Categories"]['Program Name']):
        if os.system('apt-cache policy ' + program + ' | grep "Installed: (none)"') == 0:
            record_hit(program + ' is uninstalled', save_dictionary["Program Management"]["Bad Program"]["Categories"]['Points'][idx], '')
        else:
            record_miss('Program Management', save_dictionary["Program Management"]["Bad Program"]["Categories"]['Points'][idx])


def anti_virus():
    if os.system('apt-cache policy clamav | grep "Installed: (none)"') > 0:
        record_hit('Clamav has been installed.', save_dictionary["Miscellaneous"]["Anti-Virus"]["Categories"]['Points'][0], '')
    else:
        record_miss('Security', save_dictionary["Miscellaneous"]["Anti-Virus"]["Categories"]['Points'][0])


def bad_file():
    for idx, item in enumerate(save_dictionary["File Management"]["Bad File"]["Categories"]['File Path']):
        if not os.path.exists(item):
            record_hit('The item ' + item + ' has been removed.', save_dictionary["File Management"]["Bad File"]["Categories"]['Points'][idx], '')
        else:
            record_miss('File Management', save_dictionary["File Management"]["Bad File"]["Categories"]['Points'][idx])


def load_config():
    global save_dictionary
    filename = 'save_data.json'
    if os.path.exists(filename):
        f = open(filename)
        save_dictionary = json.load(f)
        f.close()
    else:
        messagebox.showerror('Save Error', 'You are missing the configuration file. Please notify a mentor or re-extract the VM.')


def load_current_settings():
    global current_settings
    filename = 'current_settings.json'
    if os.path.exists(filename):
        f = open(filename)
        current_settings = json.load(f)
        f.close()


def create_shell():
    f = open('current_settings.sh', 'w+')
    f.write("#!/bin/bash\ncurrentSettings='{\"place\": 1'\n")
    if save_dictionary["Password Policy"]["Minimum Password Age"]["Enabled"] == 1:
        f.write("currentMin=$(cat /etc/login.defs | grep ^PASS_MIN_DAYS | awk '{print $2;}')\ncurrentSettings=$currentSettings', \"Minimum Password Age\": '$currentMin\n")
    if save_dictionary["Password Policy"]["Maximum Password Age"]["Enabled"] == 1:
        f.write("currentMax=$(cat /etc/login.defs | grep ^PASS_MAX_DAYS | awk '{print $2;}')\ncurrentSettings=$currentSettings', \"Maximum Password Age\": '$currentMax\n")
    if save_dictionary["Password Policy"]["Maximum Login Tries"]["Enabled"] == 1:
        f.write("currentTry=$(cat /etc/login.defs | grep ^LOGIN_RETRIES | awk '{print $2;}')\ncurrentSettings=$currentSettings', \"Maximum Login Tries\": '$currentTry\n")
    if save_dictionary["Password Policy"]["Minimum Password Length"]["Enabled"] == 1:
        f.write("if [[ `grep minlen /etc/pam.d/common-password` ]] ; then \nif [ `grep -o -P '(?<=minlen=).*(?=\\ )' /etc/pam.d/common-password` ] ; then \ncurrentPassLength=$(grep -oP '(?<=minlen=).*(?=\\ )' /etc/pam.d/common-password )\nelse \ncurrentPassLength=$(grep -oPz '(?<=minlen=)(.*\\n)' /etc/pam.d/common-password )\nfi\ncurrentSettings=$currentSettings', \"Minimum Password Length\": '$currentPassLength\nelse\ncurrentSettings=$currentSettings', \"Minimum Password Length\": 0'\nfi\n")
    if save_dictionary["Password Policy"]["Password History"]["Enabled"] == 1:
        f.write("if [[ `grep remember /etc/pam.d/common-password` ]] ; then \nif [ `grep -o -P '(?<=remember=).*(?=\\ )' /etc/pam.d/common-password` ] ; then \ncurrentPassHist=$(grep -oP '(?<=remember=).*(?=\\ )' /etc/pam.d/common-password )\nelse \ncurrentPassHist=$(grep -oPz '(?<=remember=)(.*\\n)' /etc/pam.d/common-password )\nfi\ncurrentSettings=$currentSettings', \"Password History\": '$currentPassHist\nelse\ncurrentSettings=$currentSettings', \"Password History\": 0'\nfi\n")
    if save_dictionary["Password Policy"]["Password Complexity"]["Enabled"] == 1:
        f.write("if [[ `grep ucredit=-1 /etc/pam.d/common-password` ]] ; then \ncurrentPassHistU=-1\nfi\nif [[ `grep dcredit=-1 /etc/pam.d/common-password` ]] ; then \ncurrentPassHistD=-1\nfi\nif [[ `grep ocredit=-1 /etc/pam.d/common-password` ]] ; then \ncurrentPassHistO=-1\nfi\ncurrentPassCompx=$((currentPassHistU+currentPassHistD+currentPassHistO))\ncurrentSettings=$currentSettings', \"Password Complexity\": '$currentPassCompx\n")
    if save_dictionary["Miscellaneous"]["Update Auto Install"]["Enabled"] == 1:
        f.write("auto_install=$(grep -oP '(?<=Unattended-Upgrade \").' /etc/apt/apt.conf.d/10periodic)\ncurrentSettings=$currentSettings', \"Update Auto Install\": '$auto_install\n")
    if save_dictionary["Miscellaneous"]["Update Check Period"]["Enabled"] == 1:
        f.write("check_period=$(grep -oP '(?<=Update-Package-Lists \").' /etc/apt/apt.conf.d/10periodic)\ncurrentSettings=$currentSettings', \"Update Check Period\": '$check_period\n")
    if save_dictionary["Account Management"]["User Change Password"]["Enabled"] == 1:
        for name in save_dictionary["Account Management"]["User Change Password"]["Categories"]['User Name']:
            f.write("current_password_" + name + "=$(chage -l " + name + " | grep 'Last password change')\ncurrentSettings=$currentSettings', \"Current Password " + name + "\": \"'$current_password_" + name + "'\"'\n")
    f.write("currentSettings=$currentSettings'}'\necho $currentSettings > current_settings.json\nchmod 777 current_settings.json")
    f.close()
    os.chmod('current_settings.sh', 0o777)
    os.system('sudo ./current_settings.sh')
    load_current_settings()


def user_management():
    write_to_html('<H3>USER MANAGEMENT</H3>')
    if save_dictionary["Account Management"]["Disable Guest"]["Enabled"] == 1:
        disable_guest()
    if save_dictionary["Account Management"]["Keep User"]["Enabled"] == 1:
        keep_user()
    if save_dictionary["Account Management"]["Remove User"]["Enabled"] == 1:
        remove_user()
    if save_dictionary["Account Management"]["Add User"]["Enabled"] == 1:
        add_user()
    if save_dictionary["Account Management"]["User Change Password"]["Enabled"] == 1:
        user_change_password()
    if save_dictionary["Account Management"]["Add Admin"]["Enabled"] == 1:
        add_admin()
    if save_dictionary["Account Management"]["Remove Admin"]["Enabled"] == 1:
        remove_admin()
    if save_dictionary["Account Management"]["Add User to Group"]["Enabled"] == 1:
        add_user_to_group()
    if save_dictionary["Account Management"]["Remove User from Group"]["Enabled"] == 1:
        remove_user_from_group()


def security_policies():
    write_to_html('<H3>SECURITY POLICIES</H3>')
    if save_dictionary["Policy Options"]["Turn On Firewall"]["Enabled"] == 1:
        turn_on_firewall()
    if save_dictionary["Password Policy"]["Minimum Password Age"]["Enabled"] == 1:
        minimum_password_age()
    if save_dictionary["Password Policy"]["Maximum Password Age"]["Enabled"] == 1:
        maximum_password_age()
    if save_dictionary["Password Policy"]["Maximum Login Tries"]["Enabled"] == 1:
        maximum_login_tries()
    if save_dictionary["Password Policy"]["Minimum Password Length"]["Enabled"] == 1:
        minimum_password_length()
    if save_dictionary["Password Policy"]["Password History"]["Enabled"] == 1:
        password_history()
    if save_dictionary["Password Policy"]["Password Complexity"]["Enabled"] == 1:
        password_complexity()
    if save_dictionary["Policy Options"]["Disable Auto Login"]["Enabled"] == 1:
        disable_auto_login()
    if save_dictionary["Policy Options"]["Disable User Greeter"]["Enabled"] == 1:
        disable_user_greeter()


def program_management():
    write_to_html('<H3>PROGRAMS</H3>')
    if save_dictionary["Program Management"]["Good Program"]["Enabled"] == 1:
        good_program()
    if save_dictionary["Program Management"]["Bad Program"]["Enabled"] == 1:
        bad_program()
    if save_dictionary["Program Management"]["Services"]["Enabled"] == 1:
        services()


def file_management():
    write_to_html('<H3>FILE MANAGEMENT</H3>')
    if save_dictionary["Forensic"]["Enabled"] == 1:
        forensic_question()
    if save_dictionary["File Management"]["Bad File"]["Enabled"] == 1:
        bad_file()
    if save_dictionary["File Management"]['Check Hosts']["Enabled"] == 1:
        check_hosts()
    if save_dictionary["File Management"]["Add Text to File"]["Enabled"] == 1:
        add_text_to_file()
    if save_dictionary["File Management"]["Remove Text From File"]["Enabled"] == 1:
        remove_text_from_file()


def miscellaneous():
    write_to_html('<H3>MISCELLANEOUS</H3>')
    if save_dictionary["Miscellaneous"]["Check Startup"]["Enabled"] == 1:
        check_startup()
    if save_dictionary["Miscellaneous"]["Cron Tab"]["Enabled"] == 1:
        cron_tab()
    if save_dictionary["Miscellaneous"]["Anti-Virus"]["Enabled"] == 1:
        anti_virus()
    if save_dictionary["Miscellaneous"]["Update Auto Install"]["Enabled"] == 1:
        update_auto_install()
    if save_dictionary["Miscellaneous"]["Update Check Period"]["Enabled"] == 1:
        update_check_period()


load_config()
possible_points = 0
possible_vulnerabilities = 0
total_points = 0
total_vulnerabilities = 0
prePoints = 0
Desktop = save_dictionary["Main Menu"]["Desktop Entry"]
index = '/usr/local/CyberPatriot/'
scoreIndex = index + 'ScoreReport.html'

# --------- Main Loop ---------#
check_runas()
create_shell()
while True:
    possible_points = 0
    possible_vulnerabilities = 0
    total_points = 0
    total_vulnerabilities = 0
    draw_head()
    os.system('sudo ./current_settings.sh')
    user_management()
    security_policies()
    program_management()
    file_management()
    miscellaneous()
    check_score()
    draw_tail()
    time.sleep(60)

# TODO add Functions:
#  updatecheckperiod    ["Miscellaneous"]["Update Check Period"]
#  updateautoinstall    ["Miscellaneous"]["Update Auto Install"]
#  checkhosts           ["File Management"]["Check Hosts"]
#  taskscheduler        ["Miscellaneous"]["Task Scheduler"]
#  checkstartup         ["Miscellaneous"]["Check Startup"]
