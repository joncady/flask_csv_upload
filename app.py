from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
from oauth2client.service_account import ServiceAccountCredentials

# Allows us to access Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Change to your own spreadsheet ID
SPREADSHEET_ID = '<add-spreadsheet-id>'
# Change Sheet range here and it will change everywhere
# Change sheet name here for different tabs 
RANGE_NAME = "'Sheet1'!A:B"

# Download credentials.json file and add it to this directory
credential = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes=SCOPES) 

app=Flask(__name__)

# enable debugging mode, turn off 
app.config["DEBUG"]=True

# Upload folder
UPLOAD_FOLDER='static/files'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


# Root URL
@ app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'  
    return render_template('index.html')

# Root URL
@ app.route('/success')
def success():
    # Set The upload HTML template '\templates\index.html'  
    return render_template('success.html')

# Get the uploaded files
@ app.route("/upload", methods=['POST'])
def uploadFiles():
    # get the uploaded file from the request
    uploaded_file=request.files['file']

    if uploaded_file is None:
        return "No file included"
    file_path = ""
    if uploaded_file.filename != '':
        file_path=os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        #   set the file path
        uploaded_file.save(file_path)
        # save the file
    else:
        return "No file included"
    # builds service 
    service=build('sheets', 'v4', credentials=credential)

    try:
        # prepping data object for upload
        to_upload=[]
        print(uploaded_file)
        # finds local file
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            # skip first row (you can also keep it if you want to use it)
            next(reader)

            # iterate the rest of the rows
            # row is a list of all the values in the row, in list format
            for row in reader:
                # we choose which cols to pull
                to_upload.append([row[0], row[2], row[4]])
        print(to_upload)

        # in the shape of https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
        body_data={
            "range": RANGE_NAME,
            # list of the the rows to add
            "values": to_upload
        }

        # documentation: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
        api_request=service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME, valueInputOption="RAW", insertDataOption="INSERT_ROWS", body=body_data)
        response=api_request.execute()
        # deletes file to clean up
        os.remove(file_path)
    except Exception as err:
        print(err)
        return "Error"
    return redirect(url_for("success"))

if (__name__ == "__main__"):
    app.run(port=5000)
