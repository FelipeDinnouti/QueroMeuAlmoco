![Check out this site if you need more help](https://realpython.com/python-virtual-environments-a-primer/)

![Documentation for fastHTML (important)](https://docs.fastht.ml/tutorials/quickstart_for_web_devs.html)

Using a venv isn't obligatory, it's just convenient

Using the venv (linux)

activate the venv
``` shell
$ source bin/activate
```
and 
``` shell
$ deactivate
```
to exit

Using the venv (windows)

Make a venv in a folder and add it to .gitignore, works the same as on linux 

# Usefull tips

If you create a new webpage, remeber to add it in the beforeware whitelist (or else the user is only able to access it if it is authenticated)
I recomend use a redirect response with status code 303 after handling a post request 