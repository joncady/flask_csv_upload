# Steps

## Download Repo to your computer
- If you don't have Git: [follow](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) for Windows
- Repo: https://github.com/joncady/flask_csv_upload
- `git clone https://github.com/joncady/flask_csv_upload`

## Set up Google Sheets API and download `credentials.json`
-  From the [dashboard](https://console.cloud.google.com/apis/library), choose `Google Sheets API`, enable it, `credentials` -> `create credentials` -> `service account` and fill out w/ random values (somewhat followed [this](https://medium.com/better-programming/integrating-google-sheets-api-with-python-flask-987d48b7674e))
- When account is created, `add key` -> `create key` -> `json`, will download to your computer
- Move it to your project folder and rename it `credentials.json`
- Save your service account email

## Create / link Sheet + set up local testing
- Create / find Sheet ID and replace as `SPREADSHEET_ID`
- Share the sheet with you service account email (found above)
- Change the range to the tab you want (`Sheet2`, etc)
- Run `pip install Flask oauth2client google-api-python-client google-auth-httplib2 google-auth-oauthlib`
- To test locally, you can run `python app.py`
- Change the range to the proper Sheet name in all places

# Prepare to deploy
- Create requirements.txt file that houses required dependencies (can follow [link](https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt))
```
pip install pipreqs

pipreqs .
```
- Make sure `requirements.txt` has `gunicorn==20.0.4` also run `pip install gunicorn`
- Follow first couple steps for Python [set up](https://devcenter.heroku.com/articles/getting-started-with-python)
- `Procfile` set `web: gunicorn app:app`, which looks for `app.py`
- Follow git commands
  - `git init .`
  - `heroku git:remote -a <heroku-project-name>`
  - `git add .`
  - `git commit -m "Commit message"`
  - `git push heroku master`