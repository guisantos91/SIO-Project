# run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    app.config["organization_db"] = "../organization_db"


