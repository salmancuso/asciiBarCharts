# Message Of The Day (MOTD) System Usage ASCII Bar Charts

## What does it do

The purpose of this tool is rather simple, to provide a graphical display of recent system stats when a user logins in (via SSH) to a Linux server.   The tool provides a means to include a custom MOTD above two charts that are dynamically created of CPU usage and Memory Usage.


### Prerequisites

So you want to run this tool... then you need **ROOT**. There I said it, root, root root, root... you need to have root access. Why? Because you will be setting up a cron job to modify the /etc/motd file which... wait for it... is under root control. Yes sure you can change the access of the motd but where is the fun in that? 

Also this script will is written under **Python3**

Lastly the libaries requered for this tool to run are...
- sqlite3
- datetime
- re
- psutil
- calendar
- time

### Deployment

Deployment is straightforward.  After cloning this tool (as root) a cron job needs to be set up. 

```sudo crontab -e```

Add the following row to the bottom of the cron file. Worth noting this cron will execute the motdGrapher.py every minute. 

```* * * * * /usr/bin/python3  /path/to/motdGrapher.py```

To change the message of the day open the "motdMessages.txt" file in your favorate editor (I prefer nano).  By default (and to force you to change it) there is an ASCII of R2D2.  
