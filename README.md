docker
---------------
docker build -t angel-algo-streamlit .
docker run -d -p 8501:8501 angel-algo-streamlit



direct
------------
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py