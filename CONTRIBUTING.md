# Contributing to the distrochooser project

Thank you for your interest in contributing to the distrochoooser project 🎉!

# Preparations

Following documents are important for any contribution in the distrochooser repository

👉 [Code of conduct](https://github.com/distrochooser/distrochooser/blob/master/CODE_OF_CONDUCT.md)

👉 [License](https://github.com/distrochooser/distrochooser/blob/master/LICENSE)

# Contributing to the code 💻

Basically, the distrochooser project splits into two modules, the frontend (`viisi`, which is a Nuxt.js project) and the backend (`backend`, wich is a Django project). 

- 📦 Please use yarn while working with the frontend
- 🐍 The backend is Python3 only

# Contributing translations 🌍

You can find the file `backend/locale/en.po` in this repository. This file is the english translation. If you don't have a GitHub account and want to download it: (the direct link)[https://raw.githubusercontent.com/distrochooser/distrochooser/master/backend/locale/en.po]. 

The file names in `backend/locale` are following the [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) standard, wich means they are two letter codes.

E. g. if you want to create a greece translation, use the filename `gr.po`.

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

You can either do a pull request into the `distrochooser/distrochooser:master` branch or, if you don't have a GitHub account, send it via mail to `mail@chmr.eu`.


Thank you for your support 😁

