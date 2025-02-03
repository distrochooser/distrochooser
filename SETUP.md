# Building locally

## Base configuration

- Clone the Distrochooser repository https://github.com/distrochooser/distrochooser **important: branch main**
- Clone the translation repository https://github.com/distrochooser/translations **important: branch 6-new-baseline** INTO the folder `locale`, e. g. with `git clone https://github.com/distrochooser/translations.git -b 6-new-baseline ./locale`

**Important**: Make sure you've cloned the contents of the https://github.com/distrochooser/translations repository **directly** into the `locale` folder. You can verify this if after the cloning your `locale` folder should contain files like `ui-en.json`, without having a new subdirectory "translations".

You should now see following folder structure:

```
[...]
code/
doc/
locale/ <-- this folder is from the translation repo and should contain JSON-files
HOW-TO-Map.md
[...]
```

## Install

> We assume you use a venv-like approach here. If you use another approach, replace this step with the tool of your choice.

Create the venv:

`python -m venv ./venv` while `./venv` is the path where you want to put the virtual environment folder into.

Activate the venv (this step depends on your operating system, see https://docs.python.org/3/tutorial/venv.html for details):

`source ./venv/bin/activate` for unix-like Systems and `.\venv\Scripts\activate` for Windows systems

Switch into the folder `code/kuusi` and executing following command

```
pip install -r requirements.txt
# Create database (sqlite per default here) and migrate the structure
python manage.py migrate
# to get a user and password for the admin panel on /admin
python manage.py createsuperuser
# Import the base questionaire structure
python manage.py parse ../../doc/matrix/toml/matrix.toml --wipe 
# Add static files
python manage.py collectstatic
```

At this point, you have a filled database and basically can start the application using `python manage.py runserver`. This starts the webserver, which is accessible at http://localhost:8000, e. g. the Swagger UI should be accessible on http://localhost:8000/rest/swagger-ui/.

# Frontend requirement

The frontend is a Nuxt (https://nuxt.com/) powered application. It requires Node.js to run.

To set up this part of the project, switch into the folder `code/frontend`:

Execute `yarn install`.

> Remark: The `sdk-build` command is based upon openapi-generator-cli. Furthermore, this task requires a Java Environment 11 (can be OpenJDK/ Adoptium aswell). You can find more information on https://www.npmjs.com/package/@openapitools/openapi-generator-cli

Execute `yarn sdk-build` (this step is required each time something is changed on the RESTful API and once initially)

Execute `yarn run dev`. You will now be able to open `http://localhost:3000`. The app defaults currently to `http://localhost:8000` as the backend.

# Further reading

See CONCEPTS.md for details about application structure.
