# Contributing to the distrochooser project

Thank you for your interest in contributing to the distrochooser project 🎉!

# General

Distrochooser has a very slow development cycle as this is a "weekend warrior" project. This means that issues might be unanswered for months before being picked up. But don't worry, they will be discussed, but just not that fast as in large projects. 

Please note that there will no discussions with deleted accounts (on PR/ Issues/ Discussions). These threads will be closed.

# Preparations

Following documents are important for any contribution in the distrochooser repository

👉 [Code of conduct](https://github.com/distrochooser/distrochooser/blob/master/CODE_OF_CONDUCT.md)

👉 [License](https://github.com/distrochooser/distrochooser/blob/master/LICENSE)

# Contributing to the code 💻

Basically, the distrochooser project splits into two modules, the frontend (`viisi`, which is a Nuxt.js project) and the backend (`backend`, which is a Django project). 

- 📦 Please use yarn while working with the frontend
- 🐍 The backend is Python3 only

## Viisi

Viisi is a Nuxt.js 2 project. It heavily depends on [https://github.com/christianmalek/vuex-rest-api](https://github.com/christianmalek/vuex-rest-api) for communicating with the JSON backend. The frontend does not load all the required data at startup, it does only load the translations and the data required for the currently displayed data. If you switch a question, the data for the next question gets loaded.

## Backend

As mentioned, the backend is a django application. The majority of logic happens in the `views.py` file, the calculation methods are isolated in the `calculations/` folder.

# Contributing translations 🌍

https://github.com/distrochooser/translations is your starting point for translations. You can either use the Weblate instance (details in the Readme) or use a PR.

For PR users:

You can find the file `en.po` in the repository https://github.com/distrochooser/translations. This file is the english translation. If you don't have a GitHub account and want to download it: [the direct link](https://raw.githubusercontent.com/distrochooser/translations/main/en.po).

Use this file as the boilerplate for your translation.

The file names in `backend/locale` are following the [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) standard, which means they are two letter codes.

E. g. if you want to create a greek translation, use the filename `gr.po`.

The files are structured in key:value pairs, marked  with `msgid` (the key) and `msgstr` (the value).

```
msgid "welcome-text"
msgstr "Welcome! This test will help you choose a suitable Linux distribution."
```

## Warning: Please use no `"` inside of the `""`. This will cause a syntax error ⚠ 

```
msgid "example-text"
msgstr "This example is "quoted"" ⚠ syntax error!
```
You can use `'` inside of the value:
```
msgid "example-text"
msgstr "This example is 'quoted'" ✅ all good
```
Or you can escape the `"`:
```
msgid "example-text"
msgstr "This example is \"quoted\"" ✅ all good
```

## How to submit the translation? 📮

You can either do a pull request into the `distrochooser/translations:main` branch or, if you don't have a GitHub account, send it via mail to `mail@chmr.eu`.


Thank you for your support 😁

