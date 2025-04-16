# PROJECTS
My personal project hub project 

### LinkedIN summarizer
It is project where the val.jsonl and train.jsonl is bieng used to fine tune the google gemini flash 1.5 for undetectable AI Generated LinkedIn Profile summary based on User Profile data, with the help of GCP and vertex.
geminiapi.py is the app to run through streamlit run <name>.py command to access it on local server.
testcase.py is the direct use case to generate output for the test case data saved in output_summary.csv.

### Explicit Word Detector is being trained with the help of twitter hate speech data set, train.csv file is missing you can get it available on Kaggle.
Bert Model is being saved after being trained.
utils.py save the util function to pre-process data
app.py is the flask app to run with flask run app.py on localhost. 
