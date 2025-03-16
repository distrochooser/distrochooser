# Building locally

## Base configuration

- Clone the Distrochooser repository https://github.com/distrochooser/distrochooser

## Configuration values

> Django values skipped here
> Django values see https://docs.djangoproject.com/en/4.2/topics/settings/#top

|Value|Description|
|--|--|
|SECRET_KEY|Set to something random|
|DEBUG|Disable in production|
|ALLOWED_HOSTS|Required in case your application runs behind a reverse proxy -> needs accessing domain entry then|
|ENABLE_PROFILING|Enables or disables Silk module. Disable in production|
|AVAILABLE_LANGUAGES|A list of tuples of available languages `(<iso-639-3-code>, Display text)`|
|RTL_LANGUAGES|A list of language codes (iso-639-3) considered right-to-left|
|FRONTEND_URL|The URL without trailing slash representing the frontend URL|
|KUUSI_NAME|The name of the application. Will be used e. g. in OGP tags and the frontend|
|KUUSI_META_TAGS|Meta tags to be rendered client sided
|SESSION_NUMBER_OFFSET|The amount of tests to be added to the current database count|
|WEIGHT_MAP|Factor to give to each weight|
|DEFAULT_LANGUAGE_CODE|The `iso-639-3` code to use from `LANGUAGES` representing the default language|
|KUUSI_LOGO|The logo to add to frontend sessions|
|KUUSI_ICON|The favicon to add to frontend sessions|
|CACHE_TIMEOUT|The default cache timeout to use|
|Imprint|A text to be used as contact (legal imprint info)|
|PRIVACY|Privacy text. Can be HTML|
|DISCORD_HOOK|A URL to use for notifications about text feedback and votes. Is ignored if null or empty|

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
