LokasBot website
==========

Deploy on Toolforge
-------------------

-   ```
    webservice --backend=kubernetes python3.9 stop
    rm -fdr $HOME/www/python/src
    mkdir -p $HOME/www/python
    git clone https://github.com/LokasWiki/Username-Classifier-flask-app.git $HOME/www/python/src
    webservice --backend=kubernetes --mem 3Gi --cpu 1 python3.9 shell 
    python3 -m venv $HOME/www/python/venv
    source $HOME/www/python/venv/bin/activate
    pip install --upgrade pip wheel
    python3 -m pip install -U pip setuptools wheel
    python -m pip install requests
    python -m pip install pyyaml
    python -m pip install 'transformers[torch]' --no-cache-dir
    pip install -r $HOME/www/python/src/requirements.txt
    python -c "from transformers import pipeline; print(pipeline(model="lokas/spam-usernames-classifier")('I love you'))"
    exit
    ```
    
-   ```
    webservice --backend=kubernetes  --mem 4Gi --cpu 1 python3.9 start
    ```
    
