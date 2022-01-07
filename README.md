# JSE Scraper & Charting App

## INTRODUCTION

This is a web scraper app that gets data about the Jamaica Stock Exchange using the [mymoneyja.com](http://mymoneyja.com) website. The data is then transformed and loaded into an AWS S3 and MongoDB. 

At present the data sent to MongoDB isn’t being used but I decided to store it there because I might use it to add some addition features to the app in the future. 

## The Scraper

The web scraper is started by running the `etl-sel.py` file. A `.env` file should be created with the environment variables as shown below:-

```python
EMAIL=""
PASSWORD=""
S3_BUCKET = ""
DB_URL=""
```

A **mymoneyja**  account is required to successfully access the data on the site. Once your account is created add the email and password for your account in the `.env` file.

To store the data in your own S3 bucket you must have the **AWS CLI** tool installed on your machine. Put the name of the S3 Bucket that you will use int the `.env` file.

To store the data in MongoDB put the **DB URI** provide by MongoDB in the `.env` DB_URL variable.

## The Chart

The use the chart html file with the data you scraped replace the url found on line 313 in the `chart.html` file with your own S3 url.

https://s3.ap-northeast-1.amazonaws.com/romallen.com/json/${selectedComp}-data.json

You should only replace the part shown in red.