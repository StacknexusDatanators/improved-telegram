# rfiqa


### installation

* install ollama (https://ollama.com/)
* pull the model from the repository using the following command
```
ollama pull mistral:7b
```
* please create a new python environment (preferrably using anaconda)
* activate the environment
* go the the ./app folder
```
cd ./app
```
* install the required libraries
```
pip install -r requirements.txt
```
* install streamlit
```
pip install streamlit
```
* run the application using
```
streamlit run streamlit_chat.py
```
* open the browser and go to http://localhost:8501

## application execution

* in the web application upload all the RFI documents (as pdf)
* wait till the success message in green
* only after ingesting the pdfs and the success message, navigate to the 2nd tab and you can ask any questions to the chatbot