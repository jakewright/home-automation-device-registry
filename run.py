# Import the application
from app import app

# Run the application in debug mode
app.run(host='0.0.0.0', port=int(app.config['PORT']), debug=True)
