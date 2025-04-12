# PostgreSQL setup instruction

Install PostgreSQL in your local machine, if not already installed (version should be 17 or above). Start PostgreSQL service (In case it is not running). To start PostgreSQL service instructions as follows below.

**If you are on Windows:**

- Press (Window button + R), then type services.msc, and hit Enter.
- Look for a service like postgresql-x64-17 (or whatever version you installed).
- Right-click on it -> click Start (or Restart).

**If you are on Mac/Ubuntu, run:**

```bash
sudo service postgresql start
```

Check PostgreSQL version to confirm that PostgreSQL is started, run:

```bash
psql --version
```

If the PostgreSQL service is running, then open a Command prompt/terminal and login to PostgreSQL with the superuser like postgres(or whatever your superuser name), run:

**If you are on Windows ->**

```bash
psql -U postgres
```

**If you are on Mac/Ubuntu ->**

```bash
sudo -u postgres psql
```

Run the following commands one by one:

```bash
CREATE DATABASE tmp_database;
```

```bash
CREATE USER tmp_user WITH PASSWORD 'yourpassword';
```

```bash
ALTER ROLE tmp_user SET client_encoding TO 'utf8';
```

```bash
ALTER ROLE tmp_user SET default_transaction_isolation TO 'read committed';
```

```bash
ALTER ROLE tmp_user SET timezone TO 'UTC';
```

```bash
GRANT ALL PRIVILEGES ON DATABASE tmp_database TO tmp_user;
```

```bash
\q
```

Apply permissions to the newly created database. For that, login to PostgreSQL again using a superuser like postgres(or whatever your superuser name) and run:

```bash
psql -U postgres -d tmp_database;
```

```bash
GRANT ALL ON SCHEMA public TO tmp_user;
```

```bash
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tmp_user;
```

```bash
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tmp_user;
```

# Project setup instruction

- Create a folder and open command prompt in the folder.
- Then run the following command to clone the repository:

```bash
git clone https://github.com/Hadayetullah/Healthx-Ventures.git
```

**Note: Make sure, you are in the directory where the requirements.txt file exists.**

### Virtual environment setup:

**If the virtual environment already not installed, please visit ->**

```bash
https://virtualenv.pypa.io/en/latest/installation.html
```

Create virtual environment, run:

**If you are on Windows ->**

```bash
py -m venv .venv
```

**If you are on Mac/Ubuntu ->**

```bash
python3 -m venv .venv
```

Activate virtual environment, run:

**If you are on Windows ->**

```bash
.venv\Scripts\activate
```

**If you are on Mac/Ubuntu ->**

```bash
source .venv/bin/activate
```

Check if the virtual environment is activated and shows python location, run:

**If you are on Windows ->**

```bash
where python
```

**If you are on Mac/Ubuntu ->**

```bash
which python
```

Install necessary packages, run:

```bash
pip install -r requirements.txt
```

### Edit .env.local file:

Open the .env.local file in a code editor, update code and save.

### Finally

- Start the local server, run:

```bash
uvicorn app.main:app --reload
```

- After starting the local server copy the below url and paste it in a browser.

```bash
http://127.0.0.1:8000/docs
```

**The Swagger UI should be displayed. API routes can be used by the platform like Postman but for the each tasks routes operation you have to explicitly provide Authorization header and value 'Bearer access_token'. If you want to continue with the Swagger UI, you will get the access_token by login and find the 'Authorize' button at the top of the right side, click on it then paste the access_token value and click on 'Authorize' button and close the modal. Now you are ready for the tasks routes operation without explicitly providing Authorization header.**
