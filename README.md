
# GroupChat Project Setup


1. Create Virtualenv
```shell
  python3 -m venv venv
```

2. Activate venv 

```shell
  source venv/bin/activate
```

3. Install requirements.txt file
```shell
  pip install -r requirement.txt
```

4. Makemigrations
```shell
  python3 manage.py makemigrations
```
5. Migrate
 ```shell
  python3 manage.py migrate
```
7. create super user for accessing admin panel
```shell
  python3 manage.py createsuperuser
```

8. Run this project with following command
```shell
  python3 manage.py runserver
```

```
That's It Now you can access this site.
```

#Features Of This Site

```
- click on login button on ener the website.
- first click on admin panel so that admin can create new user and update those users
- create 3,4 users to test chat bot
- create group with thier name and members
- click on add member to add new member in that group and this can be done only admin of that user
- click delete to delete specific group and this can be done only admin of that user
- you will see list of groups which is created by you or you are member of someone groups.
- click on chat to enter to the chatbot
```

# Thank You
