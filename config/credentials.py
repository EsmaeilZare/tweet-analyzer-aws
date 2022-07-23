import decouple

ACCESS_KEY = decouple.config("ACCESS_KEY")
SECRET_KEY = decouple.config("SECRET_KEY")
SESSION_TOKEN = decouple.config("SESSION_TOKEN")
BUCKET_NAME = decouple.config("BUCKET_NAME")
SECURITY_GROUP_NAME = decouple.config("SECURITY_GROUP_NAME")
TEMPLATE_NAME = decouple.config("TEMPLATE_NAME")
AUTO_SCALING_GROUP_NAME = decouple.config("AUTO_SCALING_GROUP_NAME")
