from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_document(title, category, storage_url):

    data = {
        "title": title,
        "category": category,
        "storage_url": storage_url,
        "indexed": False
    }

    response = supabase.table("legal_documents").insert(data).execute()

    return response


def update_index_status(doc_id):

    response = supabase.table("legal_documents").update(
        {"indexed": True}
    ).eq("id", doc_id).execute()

    return response


def get_all_documents():

    response = supabase.table("legal_documents").select("*").execute()

    return response.data