from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET_NAME = "legal-documents"


def upload_pdf(file_path, file_name):

    with open(file_path, "rb") as f:

        response = supabase.storage.from_(BUCKET_NAME).upload(
            file_name,
            f
        )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_name)

    return public_url