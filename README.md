Pretty simple webscraper for PA liquor stores. 


# TO RUN FROM TERMINAL

1. Create a virtual environment. To do so run the command python -m venv venv in your terminal/cmd line

2. 
## If on Windows
venv\scripts\activate

## If on Mac
source venv/bin/activate

3. Run the command in your terminal/cmd line pip install -r requirements.txt

4. Add all things you want to search to the input_liquors.txt file. Treat each line as an entry into the search function

5. Run the command python scraping.py

6. deactivate the virtual environment using deactivate

7. Open the file generated with today's date


# TO RUN FROM FINDER

1. Open your terminal to the directory (file) that the project is stored in

2. Type chmod +x run_mac.command (This changes the permissions around the file to allow this file to run as a script)

3. Double click run_mac.command


# ADJUSTMENTS

## Distance From You
Currently it enters a zipcode. If that zipcode changes just change the global variable. If you go to line 92 you can change how many miles away you want the stores it's recording to be

## How Many Runs A Day
Currently it's configured to run once a day. If you wish to run it multiple times a day I recommend going to line 10 and removing the .date(). This will change the filename to be the date and current time, allowing you to not write over previous runs. 


# AUTOMATIC SCHEDULING
Refer to this website: https://phoenixnap.com/kb/cron-job-mac