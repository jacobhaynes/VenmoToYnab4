# VenmoToYnab4
This project provides a simple web interface to convert the CSV from Venmo -> Statement -> Download CSV into something that YNAB 4 can understand. 

## Importing Venmo transactions to YNAB4

1. Log into your Venmo Account 
2. Go to Statements and select the range you would like to download, then click the download CSV button. 
3. Visit: [venmotoynab.com](https://www.venmotoynab.com) and select that CSV 
4. Click the Convert. You should see a download for the new CSV that is parsable by YNAB (ending in _ynab4.csv); 
5. In YNAB 4, click "File"->"Import Transcations from your Bank", choose the file and the correct account and it should import. 

## Development

This app is built on django and currently hosted on Google App Engine. The google app engine are pretty good at describing how to setup your environment, run and deploy the service: 

https://cloud.google.com/python/django/appengine

You may need to change out the DATABASES portion to point to a local SQL database if you run locally and don't have access to the GCP project (which you probably don't). 
```Python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
