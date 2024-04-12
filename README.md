------------------------------------------------------
docker
------------------------------------------------------
docker build -t angel-algo-streamlit .
docker compose up -d --build




------------------------------------------------------
direct
------------------------------------------------------
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py