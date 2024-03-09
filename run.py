import os
from blog import app
from blog import models

models.seed() # popular db with sample data

app.secret_key = os.urandom(24)
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)