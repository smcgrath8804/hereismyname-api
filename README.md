# HereIsMy.Name

A Django project that lets users keep one profile and choose which details and links other people can see. Users assign their incoming connections to Public, Personal, Professional or General.

The project has a website and a REST API. Both use the same profile-field filtering functions. The website also shows links according to the viewer's category.

## Live demonstration

The live site is available at https://hereismy.name/.

The live site has demo accounts. Login details and examples to try are included separately in the assessment submission. These accounts will not exist in a new local installation.

## Requirements

Tested locally on Windows with Python 3.12.1. Dependencies are listed in `requirements.txt`.

The project uses SQLite, so no separate database server is required. Internet access is needed to install dependencies and load Bootstrap and Swagger UI.

## Download the project

Download the repository using GitHub's **Code > Download ZIP** option and extract it, or clone it using Git:

```bash
git clone https://github.com/smcgrath8804/hereismyname-api.git
cd hereismyname-api
```

Run the following setup commands from the folder containing `manage.py`.

## Windows setup

Open PowerShell and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. Keep PowerShell open while using the application. Press Ctrl+C to stop the server.

## macOS / Linux setup

With Python 3.12 installed, open a terminal and run:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py check
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

These commands follow the [Python virtual environment documentation](https://docs.python.org/3.12/library/venv.html). The macOS/Linux setup steps have not been tested with this project. Local testing was on Windows.

Open http://127.0.0.1:8000/ in your browser. Keep the terminal open while using the application. Press Ctrl+C to stop the server.

## Local database and accounts

The database is not included. The `manage.py migrate` command above creates a new local database. You will need to register accounts and set up their profiles and visibility rules.

Use the browser registration page to create accounts. Sign in using the account's email address. Each registered account automatically receives a profile.

To try the visibility settings locally:

1. Register two accounts: a profile owner and a viewer. Use different usernames and email addresses.
2. Sign in as the owner, edit the profile and fill in a few fields, such as a display name, biography and job title.
3. Open **Visibility Rules**. Set the display name to Public and the job title to Professional. Leave Public unchecked for the job title.
4. You can also add links through **Manage Links** and choose who can see them in the link visibility settings.
5. In a separate browser session, sign in as the viewer. Search for the owner's username and send a connection request.
6. As the owner, review the incoming request and accept it as Professional.
7. As the viewer, open the owner's profile. Compare it with the same profile in a logged-out session. The Professional viewer should receive both Public and Professional information; the logged-out viewer should receive only Public information.

Accepting a request lets the requester see information shared with their assigned category. It does not give the owner the same access to the requester's profile; that needs a separate request in the other direction.

Use separate browsers or a normal and private browsing session to keep accounts signed in independently.

## API demonstration

Open the interactive API documentation at http://127.0.0.1:8000/api/docs/.

The API uses a token rather than your website login session. Set up the two accounts above first.

1. In Swagger, expand `POST /api/login/` and select **Try it out**.
2. Enter the viewer account's email address and password.
3. Execute the request and copy the returned token.
4. In **Authorize**, enter `Token ` followed by that token, including the space.
5. Execute `GET /api/profile/{username}/` using the owner's username. The viewer should receive Public and Professional fields if the owner classified that viewer as Professional.
6. Remove the authorization and repeat the request to compare the Public-only response.

The profile response contains the fields the viewer is allowed to see. It does not include external links. Separate API endpoints let users manage their own links and visibility rules.

Do not publish API tokens or account passwords in screenshots or repository files.

## Automated tests

From the folder containing `manage.py`, run:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

On macOS/Linux, use:

```bash
.venv/bin/python manage.py test
```

There are 27 tests. They create their own data in a separate test database, which Django removes afterwards. You do not need to set up demo accounts to run them.
