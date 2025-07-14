# GUIDE TO USE THE CODE

Tu use this first create a '.env' file and then enter this:

```
SITE="https://yourodoosite.odoo.com"
EMAIL="odoo email"
PASSWORD="odoo password"
```

And then execute the code and install the dependencies. After all edit a crontab job to make the assistance automatically with this code:

```
crontab -e
```
Following you will select a code editor, I recommend to use nano. Then paste this:

```
# Run the code every day in workdays between 8:50 and 9:10
50 8 * * 1-5 yourpathtotheprojectfolder/odoo-assistance/random_runner.sh morning

# Run the code every day in workdays between 13:55 and 14:30
55 13 * * 1-5 yourpathtotheprojectfolder/Projects/odoo-assistance/random_runner.sh afternoon

```
