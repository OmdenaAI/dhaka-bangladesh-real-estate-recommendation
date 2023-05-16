# streamlit
Streamlit Project with ML and Docker Integration

Step 1- Open the project in Pycham or VS code

source venv/bin/activate

Step 2- Open Terminal and run the following commands 

pip install -r requirements.txt

streamlit run app/Home.py

Optional - Alternative way to run the application
Docker commands -

docker build -t appimage .

docker run -d --name appcontainer -p 8501:8501 appimage

