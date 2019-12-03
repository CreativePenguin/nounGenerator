# World Star by nounGenerator  
It's a trivia game. Get the high score to own a country.
You will need to know at least basic info about the country that you're
conquering.  
Real life results will vary. Visiting the actual country that you own,
and verifying whether or not it belongs to you is not recommended.
Please do not refer to the people in that country as your subjects.

## Install  
Pip is required https://pip.pypa.io/en/stable/installing/  

Clone the repo:  
```sh
git clone https://github.com/CreativePenguin/nounGenerator.git
```
Master will always contain most updated code, and thus has the possibility of not working  

Install pre-requisites with
```sh
pip install -r requirements.txt
```
Run the code with
```sh
python3 app.py
```
Then go to the link http://127.0.0.1:5000/ (listed in terminal)


## API's
### [Countries API](https://docs.google.com/document/d/1C-umxnBAIUzQI9kLDaXG4-YbFsiOwwRTJ5c-DXAHTRM/edit)  
Used to pick a country, as well as get extra info about them to use in trivia questions

### [Open Trivia API](https://docs.google.com/document/d/1yp2nicOExDYlrEfdvqspD17Kz5c-xMSWHudfmNjJgQ4/edit)  
Used to get general trivia questions that we will use in website

### [Wikipedia API](https://docs.google.com/document/d/1KNf_h_Rysiftc88uZNZO4LMpAyQprUTSj-eg5CMz9a8/edit)  
Used to get extra info about our specific countries as well as display trivia while waiting in the challenge pages.

## Contributing
Fork repo, edit master branch and request a pull
### Maintainters  
Flask App Creator -- Buford/Derek  
Person will create a Python Flask application that will have each of the routes we need (mentioned above)  
Person will make sure that the pages that require you to be logged in cannot be accessed by just typing the extension into the URL if you have not logged in
Person will make sure to flash messages when appropriate to do so (i.e. flashing a login error when submitting a wrong username or password on the login page)  

HTML/Jinja Template Creator -- Ahmed  
Person will create the HTML templates for each of the routes  
Person will use forms when appropriate (i.e. login page => username and password inputs, submit button)  
Person will use Jinja to take in and display variables when necessary (i.e. for the blog post template, use Jinja to display a blog post pulled from the database table)
Person will pay attention to aesthetic details  

Database Creator -- Winston  
Person will write a Python application to create appropriate databases and tables, making sure to only add them if they don’t already exist  
Person will facilitate adding to, editing contents in, and potentially removing from tables
