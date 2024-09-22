from flask_frozen import Freezer
from app import app  # Ensure app is imported from app.py

# Set configurations before initializing Freezer
app.config['FREEZER_RUN'] = True
app.config['FREEZER_RELATIVE_URLS'] = True

# Initialize Freezer
freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
