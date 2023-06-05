A server and website made with flask and vanilla javascript designed to run code in the browser.
To run, run:
```
python3 server.py
```
On the localhost there are two paths:
/sandbox, which allows for any code to be run in the browser 
/problems, which displays a list of coding problems that can be attempted

The problems system has a functioning testcase system and will judge based on whatever language is selected. Problems can be added through the server.py file or can be read in through a json file and converted into a dictionary.

Coderunner can be expanded to run more languages by adding different commandline commands to run the code

I had no considerations for cybersecurity while making this so it's probably not safe to run random people's code on it.