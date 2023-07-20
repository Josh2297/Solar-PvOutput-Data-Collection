# Solar-PvOutput-Data-Collection
## Solar PV Data Hub: Harness the Sun's Power :sun_with_face:

*This Project presents a script written in the python language that can be used to scrape data from the pvoutput.org site. It uses the selenium webdriver to log in the user and navigate pages it uses the beautiful soup package to scrape required data. This Scripts gets the date of upload and power generated columns only as only these were required when writing the script, to get other columns, the user is expected to extend the functionality.*

## Features

- **Easy to use:** Easy to use, clear codes, customizable and easily extensible.

- **High-Quality Data:** ONLY healthy(having health greater than or equals 98%) solar PV installations will be scraped by the script.

- **Open Access:** The data in this repository is open to the public, fostering collaboration, knowledge sharing, and innovation in the field of solar energy.

## How to Use

1.  Have the python programming language environment. A virtual env is recommended but not compulsory.
2.  Install neccessary dependencies, from the command line navigate to folder with the requirements.txt file and run `pip install -r requirements.txt` to install the dependencies.
3.  Register and obtain a username and password on the pvoutput.org site.
4.  Open the python file (selenium_pv_output_scrapping.py), navigate to line 163 and input your unsername from the pvoutput.org site in between the single quotes, do same for password on line 164
    Example:
    login_username = 'OkJosh'
    password = 'seleniumscript12'
5. The script gets the first 10 pages of different ladders by default, and for each specific ladder it gets the earliest 12 pages of data. This spans approximately a year of data for each pages.
6. The scripts gets the dat and generated_power_colum only for each ladder and saves them as csv files to a folder named  `pv_output`
7. To get more parameters for each ladder the user is required to extend the extract_date_generated_power function.
8. More pages for each ladder can be gotten by increasing the > range value from 12 in `line 49`, and more laddder pages can be scrapped by increasing the range value from 10 in `line 149`.

## Contributors.
1. Okechukwu Joshua Ifeanyi
2. Anuka Ifeanyi Stanley
