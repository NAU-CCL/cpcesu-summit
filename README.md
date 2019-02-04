# Summit Project Management System - Repository

The official repository of Summit - the Colorado Plateau Cooperative Ecosystem Studies Unit project management system.

## Dev instructions

After starting up the VM, follow these instructions:

### Checking installed programs

There should be the following programs already installed when you start the VM:

System programs:

* Git 2.19.2
    * git --version
* Java 8 - Oracle JDK/JRE 1.8.0_191
    * java -version
* PostgreSQL 8.4.22
    * psql --version
* Python 3.6.7
    * python3 --version
* Python pip3 9.0.1
    * pip3 --version
* Virtual Environment 16.1.0
    * virtualenv --version

Dev tools:

* Atom 1.26.1
    * atom --version
* pg Admin III - 1.22.2
    * pgadmin3 --version
* Prepros 6.2.3
    * Open Prepros -> 'i' icon at the bottom-left corner -> "About Prepros"
* PyCharm 2018.3.1 (Community Edition), built Dec 4, 2018
    * Open Pycharm -> Help -> About

If any of these are missing, please report it to Joseph Remy - remy@nau.edu .

### Creating PostgreSQL user and DB and adding permissions

```
sudo su postgres
psql
```

If psql errors out for Postgres not running, run the following:

```
sudo service postgresql start
```

Now, create the user and database and add permissions:

```
CREATE DATABASE summit_db;
CREATE USER summit_db_user WITH PASSWORD '$umM1T_DB)';
GRANT ALL PRIVILEGES ON DATABASE summit_db TO summit_db_user;
```

To exit psql and the 'postgres' user:

```
\q
exit
```

### Download repo and update Git config

#### SSH key
Each user needs to have an SSH key for auth. Instead of the classic username and password combo, we use SSH auth. Please talk to Joseph Remy - remy@nau.edu if you do not have an SSH key.

First, download the SSH key from the email Joseph sent you and unlock the id_rsa file with the password he has provided (probably over Discord). I suggest you extract it to the Desktop or Home directory.

Next, after extracting your private key (id_rsa), you will need to move it into the hidden .ssh directory under ~/ (Home directory on Ubuntu for summit, should be /home/summit/.ssh/). Open a Terminal window to do this and navigate to where you extracted your private key. For this example, I've extracted it to the Desktop.

```
cd ~/Desktop
ls # To confirm you extracted it here
mv id_rsa ~/.ssh/
```

Lastly, you will need to change the file permissions for your private key. Otherwise, the BitBucket server/Git will reject your SSH requests. Go to Terminal and type the following:

```
sudo chown summit ~/.ssh/id_rsa
sudo chmod 0700 ~/.ssh/id_rsa
```

If you have multiple private keys, for other things, just copy the contents of the extracted id_rsa into the existing one with an append.

#### Cloning the repo

First, go to the Bitbucket server and get the Clone URL for SSH. Note the dropdown for HTTPS and SSH. The SSH url should start with "ssh://git@...".

Next, open up Terminal and navigate to somewhere to store the repo. I suggest following these instructions.

```
cd ~/Desktop
git clone <URL> ./<REPO-NAME>
```

Lastly, after cloning the repo, go ahead and make sure everything works with a git status.

```
cd <REPO-NAME>/
git status
```

#### Updating the repo config

To make your commits unique to you and have the same template as the rest of the team, please run the following commands inside the repo:

```
git config commit.template _repo/commitTemplate
git config user.email "<YOUR EMAIL>"
git config user.name "<YOUR NAME>"
```

### Starting development environment

First, before you begin coding, you must ALWAYS be in dev virtual environment. This is required so that there are two different views to this application: development and production.

Check if the folder "venv-dev" exists. If it does, skip to the next heading. If it does not, follow these instructions below:

First, make sure you are in the repo root directory. Next, follow this command to make a dev virtual environment.

```
virtualenv ./venv-dev -p /usr/bin/python3
```

#### Activating environment

Call the following commands to start the virtual environment and update it with our current packages:

```
LINUX:
source venv-dev/bin/activate

WINDOWS (CMD ONLY):
.\venv-dev\Scripts\activate

BOTH:
pip install -r requirements/local.txt
```


#### Deactivating environment

When you are done, just deactivate the environment.

```
deactivate
```



### Starting production environment

When you are ready to try running your repo in a production environment, it is similar to the dev environment: it requires a couple of lines of commands and you will be good to go!

Check if the folder "venv-production" exists. If it does, skip to the next heading. If it does not, follow these instructions below:

First, make sure you are in the repo root directory. Next, follow this command to make a production virtual environment.

```
virtualenv ./venv-production -p /usr/bin/python3
```

#### Activating environment

Call the following commands to start the virtual environment and update it with our current packages:

```
LINUX:
source venv-production/bin/activate

WINDOWS (CMD ONLY):
.\venv-production\Scripts\activate

BOTH:
pip install -r requirements/production.txt
```


#### Deactivating environment

When you are done, just deactivate the environment.

```
deactivate
```



### Final Dev Setup

#### Setting up PyCharm

If you don't want to use Terminal and Atom, you can also do everything in PyCharm, which is already installed.

First, open the project directory with PyCharm (the directory containing _repo and the like). Now, go to File --> Settings. Look for "Project: summit" in the left nav bar and open "Project Interpreter."

On the Project Interpreter screen, click on the gear icon on the right of the Project Interpreter dropdown and click "Add..." (might say "Python 3.6"). Here we will add our two virtual environments.

Click on the "Existing environment" option if it isn't already selected. Now, in the dropdown to the right of the radio button, select the "venv-dev" environment and hit "Ok" at the bottom of the window.

Now you've added the dev environment to PyCharm. If you want to rename it so that it makes more sense, go back to the "Project Interpreter" window and click on the gear icon then "Show All..." Then select the dev environment (might be called "Python 3.6 (summit)" and click on the edit button / pencil icon. Here you can rename the environment. I called it "Summit Dev."

Repeat this process with the production environment.

Now we have the virtual environments added to PyCharm, we need to set the right branch then initialize the project.


#### Git Setup

First, if you haven't already, you will need to create the branch [using the Jira board](http://jira.remy.network) if you are making an entirely new feature. Make sure to branch off of "develop" and select the "Feature" branch type. Lastly, name the branch after the issue ID i.e. "EC-123" or a shorthand version of the issue such as "site-auth-app". You can also create branches [using the Bitbucket server](http://bitbucket.remy.network:7990/plugins/servlet/create-branch).

After creating your branch, go back to PyCharm and go to the bottom righthand corner of the window, which should said "Git: master" and click on the up and down arrows. You should see your branch name under "Remote Branches."

*If the branch appears in the list:*

Click on your branch name then click "Checkout As..." and hit "Ok."

*If the branch does NOT appear:*

Click on "Checkout Tag or Revision" and use the autocomplete to find your branch. Be sure to add the appropriate prefix. For example, the above branch would be at "origin/feature/EC-123."

Now you have set the virtual environment and checked out your branch. Be sure to check these every time you start PyCharm.

#### Update branch with Dev

Whenever the development version of the software has a new change, you should pull it in and deal with the conflicts right away. Otherwise, you will be in conflict hell when you try to do your pull request.

*For PyCharm:*

To update your branch, click on the Git dropdown at the bottom righthand corner of the screen and click on "origin/develop" and "Merge Into Current".

*For Terminal:*

To update your branch, get to the root directory of the project with the "_repo" folder. Next, follow these steps:

```
git status
git checkout develop
git pull
git checkout <YOUR_BRANCH_NAME>
git merge develop
```

#### Init project (if not done prior)

Now, either using Terminal and activating the dev virtual environment OR opening PyCharm and going to "Terminal" at the bottom lefthand corner of the screen, call the following commands. 

Not required if done previously.

```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

#### Setting up the Prepros compiler

If you are working on any of the static files, namely the CSS and JavaScript in summit/static, you will need to run Prepros to compile them. This helps allow us the break down our files in a tiered way that helps with the overall organization and maintainability of the project.

To run Prepros, just click on the icon in the dock. Next, if the project doesn't appear, open the repo in Files and navigate to the project root (where manage.py exists). Next, open "summit" and you should see the "static" folder. Drag and drop this into Prepros and it'll automatically start running and compiling files.

*Presently, this system is only for global CSS and JS. We are working on a way to do per-app that overrides the global files.*

If you have changed the global static, added/removed/modified any app's static, etc., call the following command before using the production version of the application:
```
python manage.py collectstatic
``` 

#### Running the server in development mode

First, make sure that you are using the venv-dev environment. In Terminal (both Ubuntu shell and PyCharm), it will have the prefix "(venv-dev)".

Next, call this command to run the server.

```
python manage.py runserver
```

To exit, do Control-C.


#### Running the server in production mode


First, make sure you change the virtual environment to "venv-production". See the Terminal (Ubunutu shell or PyCharm) prefix "(venv-production)".

Now that are you are ready to try out the production side, go ahead and run Gunicorn, the WSGI software for this Django project:

For local host testing:

```
gunicorn config.wsgi:application
```

For allowing all connections (testing with external devices):

```
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

To connect with an external device, just open Terminal and type:

```
ifconfig
```

Next, grab that IP address and put it into the browser and add ":8000" to the end. Example:

```
http://192.168.0.2:8000
```

This will only work on a local network unless you have done all of the necessary things to make it WAN accessible such as port forwarding.

To exit Gunicorn, just press Control-C.


#### Committing changes to remote Git repo

*For PyCharm:*

Now that you have made changes, go ahead and open the "Version Control" tab at the bottom of the window to view the change list. If you are ready to review and commit, click on the green check mark in the VC window.

A window will pop up. Go ahead and review your changes and make the commit message. Lastly, hit the triangle inside of the "Commit" button and click "Commit And Push".

_Reminder:_ Please make sure to pull in the most recent version of the "develop" branch when possible so that you do not get conflicts.

*For Terminal:*

Make sure you are in the same folder as "_repo". Next, do the following series of commands:

```
git status # to view changes
git branch # Chaeck the branch name

# You can commit one file/folder at a time or chain all of them together. Using '.' works to grab everything too!
git add <FILE/FOLDER NAME> [<ANOTHER FILE> <ANOTHER FOLDER> ...]
# Examples
git add file.py folder/folder/file.py another_file.css
git add .


# Create a commit message via the template
git commit
# OR use the in-line arg
git commit -m "Commit message here"

git push
```
