import decouple

ACCESS_KEY = decouple.config("ACCESS_KEY")
SECRET_KEY = decouple.config("SECRET_KEY")
SESSION_TOKEN = decouple.config("SESSION_TOKEN")
BUCKET_NAME = decouple.config("BUCKET_NAME")
