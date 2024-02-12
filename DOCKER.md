# Docker build

1. Use the provided Dockerfile to build an image

> We assume here that this is a production build.

```
docker build -t distrochooser:kuusi
```

2. Prepare following volumes

2.1 Make sure there is a volume to mount static assets (called `dummy-test`) in this example

2.1. A settings.py which prepares the following options

- The `DATABASES` config (add further volumes e.g. for mounting a SQlite3, in the following example we assume working on top of an existing database file for an example sqlite-based configuration)
- `STATICFILES_DIRS` should always include `/kuusi/static-buildtime`
- `LOCALE_PATHS` should always include `/kuusi/locale`
- `STATIC_URL` should point to a second deployment to a CORS-enabled (!) Webserver
- `STATIC_ROOT` should be used by both deployments, so the Webserver can serve the assets also

2.2. Docker run

```
docker run -it -p 8000:8000 --rm  --volume /path_to_the/db.sqlite3:/tmp/db.sqlite3 \
                                  --volume /path_to_the/dummy-settings.py:/kuusi/kuusi/settings.py \
                                  --volume /path_to_the/dummy-test:/kuusi/static test
```

