"""Lightweight Supabase client wrapper.

Provides `is_configured()`, `save_report()` and `fetch_report()` helpers.
Requires the environment variables `SUPABASE_URL` and `SUPABASE_KEY`.

Install the Python client with: `pip install supabase` (or add to requirements).
"""
import os
import logging
from typing import Optional, Any

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

_client = None


def is_configured() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)


def _init_client():
    global _client
    if _client is not None:
        return _client
    if not is_configured():
        return None
    try:
        # import here so package is optional at runtime
        from supabase import create_client

        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return _client
    except Exception as e:
        logging.exception("Failed to initialize Supabase client: %s", e)
        return None


def save_report(report_id: str, report: Any) -> bool:
    """Save or upsert a JSON report into the `reports` table.

    Table schema expected:
      id text primary key,
      report jsonb,
      created_at timestamptz default now()
    """
    client = _init_client()
    if not client:
        return False
    try:
        # upsert using RPC via client.table().upsert
        client.table("reports").upsert({"id": report_id, "report": report}).execute()
        return True
    except Exception:
        logging.exception("Failed to save report to Supabase")
        return False


def fetch_report(report_id: str) -> Optional[Any]:
    client = _init_client()
    if not client:
        return None
    try:
        res = client.table("reports").select("report").eq("id", report_id).maybe_single().execute()
        # supabase-py returns dict-like result with `data`
        data = getattr(res, "data", None) or res
        # data may be a dict {'report': {...}}
        if isinstance(data, dict) and data.get("report") is not None:
            return data.get("report")
        # sometimes res.data is list
        if isinstance(data, list) and data:
            return data[0].get("report")
        return None
    except Exception:
        logging.exception("Failed to fetch report from Supabase")
        return None


def upload_file(bucket: str, dest_path: str, file_bytes: bytes, upsert: bool = True) -> Optional[str]:
    """Upload raw bytes to Supabase Storage and return a public URL (if available).

    Note: The bucket must exist in Supabase Storage. Creating buckets is
    typically done via the Supabase dashboard or admin API.
    """
    client = _init_client()
    if not client:
        return None
    try:
        storage = client.storage.from_(bucket)
        # upload API: upload(path, file) - provide bytes directly
        # use upsert behaviour when available
        try:
            storage.upload(dest_path, file_bytes, {"upsert": upsert})
        except TypeError:
            # some client versions may not accept options dict; try without
            storage.upload(dest_path, file_bytes)

        # get public URL
        try:
            public = storage.get_public_url(dest_path)
            # supabase-py returns a dict {'publicURL': url}
            if isinstance(public, dict):
                return public.get("publicURL")
            # some versions return a string
            if isinstance(public, str):
                return public
        except Exception:
            logging.exception("Could not get public URL for %s/%s", bucket, dest_path)

        return None
    except Exception:
        logging.exception("Failed to upload file to Supabase storage")
        return None
