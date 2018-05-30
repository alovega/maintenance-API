import os

from maintenance import create_app

config_name = os.getenv('APP_settings')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
