> [!CAUTION]
> **CRITICAL WARNING & DISCLAIMER**
> 
> This project contains deliberate, severe security flaws (including rce and sqli). It is built strictly for isolated, local educational use. do not deploy, host, or expose this application on a public server, company network, or any internet-facing environment. 
> 
> I assume zero legal responsibility for any damages, data breaches, or misuse that may occur if you run or host this code. By downloading and running this project, you accept full responsibility for your own actions. Use it only on localhost (127.0.0.1).

## about

this is a simple, intentionally vulnerable web application i built to learn about vulnerabilities and how they work. it is designed to practice and demonstrate common web vulnerabilities in a safe, local environment.

## vulnerabilities included

the marketplace contains the following intentional flaws:

* **sql injection (sqli):** login bypass via raw string formatting in the database query.
* **stored xss:** lack of input sanitization on product descriptions allows script injection.
* **idor:** deleting products without checking if the user actually owns them.
* **broken authentication:** plaintext password storage and lack of proper admin session validation.
* **unrestricted file upload:** no extension or content checks on product images, allowing malicious html/script uploads.
* **os command injection (rce):** unsanitized input in the admin ping tool allows executing system commands.

## tech stack

* python 3
* flask
* sqlite3
* basic html/css (no external dependencies)

## how to run locally

1. clone the repo and go to the project folder:

2. install flask (if you haven't already):

```bash
pip install flask

```

3. run the application:

```bash
python3 app.py

```

4. open your browser and go to:

```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

the database (market.db) will be created automatically when you run the app for the first time. you don't need to configure anything else.
