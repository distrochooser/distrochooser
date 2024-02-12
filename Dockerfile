FROM alpine:latest as sass_builder
RUN apk add --no-cache npm \
    && npm install -g sass@1.55.0 yarn

# TODO: .dockerignore node_modules
ADD /design/ /sass_builder/

# The custom.scss' paths are configured for /static being served in dev mode -> Get rid of the static path within custom.css
RUN  cd /sass_builder/ && yarn install && \
     sed -i 's/\/static\///g' ./scss/custom.scss && \
     sass ./scss/custom.scss ./custom.css   --style compressed

RUN cd /sass_builder/ && mkdir ../static/ && yarn run build-js && ls -la ../static

# pgsql is recommended for production use
FROM python:3.11
ADD code/kuusi /kuusi
RUN apt-get update && \
    apt-get install -y gcc libpq-dev python3-psycopg2 && \
    cd /kuusi && \
    pip install -r requirements.txt

RUN adduser --disabled-password --gecos '' kuusi

# Add the static assets
RUN mkdir /kuusi/static-buildtime
COPY --from=sass_builder /sass_builder/node_modules/bootstrap-icons/font/fonts/ /kuusi/static-buildtime/bi-fonts/
COPY --from=sass_builder /sass_builder/node_modules/flag-icons/flags/ /kuusi/static-buildtime/flags/
COPY --from=sass_builder /sass_builder/custom.css /kuusi/static-buildtime/custom.css
COPY --from=sass_builder /sass_builder/custom.css.map /kuusi/static-buildtime/custom.css.map

# TODO: Add proper webpack-ish pipeline
COPY --from=sass_builder /static/bundle.js /kuusi/static-buildtime/bundle.js
COPY --from=sass_builder /static/turbo.es2017-umd.js /kuusi/static-buildtime/turbo.es2017-umd.js


ADD static/logo.svg /kuusi/static-buildtime/logo.svg
ADD static/icon.svg /kuusi/static-buildtime/icon.svg

RUN chown kuusi:kuusi -R /kuusi/static-buildtime
# Add locales
ADD locale /kuusi/locale


USER kuusi
EXPOSE 8000
WORKDIR /kuusi
CMD ["gunicorn", "kuusi.wsgi", "--timeout", "600", "-b", "0.0.0.0"]