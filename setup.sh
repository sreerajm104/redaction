mkdir -p ~/.streamlit

echo "[server]
headless = true
port = $PORT
enableCORS = false
[browser]
gatherUsageStats = false
" > ~/.streamlit/config.toml