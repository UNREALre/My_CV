##Personal CV/Portfolio project

### Installation
1. $ pip install -r requirements.txt

2. >$ set FLASK_APP=run.py  # for windows
$ export FLASK_APP=run.py  # for nix

>$ set FLASK_DEBUG=0  # for windows if you are done with development
$ export FLASK_DEBUG=0  # for nix

OR
>$ set FLASK_DEBUG=1  # if you want to debug something
$ export FLASK_DEBUG=1

3. $ flask db migrate
$ flask db upgrade

4. Create admin user via flask shell
>$ flask shell
u = User(username='admin', email='admin@gmail.com')
u.set_password('mypassword123')
db.session.add(u)
db.session.commit()

5. 