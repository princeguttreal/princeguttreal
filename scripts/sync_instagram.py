#!/usr/bin/env python3
"""Sync the latest five posts from the connected Instagram professional account."""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
API_VERSION = os.environ.get("IG_API_VERSION", "v27.0").strip()
EXPECTED_USERNAME = "princeguttreal"
OUTPUT = Path(__file__).resolve().parents[1] / "instagram-feed.json"
BASE_URL = f"https://graph.instagram.com/{API_VERSION}"


def get_json(url: str, params: dict | None = None) -> dict:
    if params:
        url = f"{url}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "PrinceGuttInstagramFeed/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        try:
            payload = json.loads(error.read().decode("utf-8"))
            detail = payload.get("error", {}).get("message", "Erro HTTP na API do Instagram")
        except Exception:
            detail = f"Erro HTTP {error.code} na API do Instagram"
        raise RuntimeError(detail) from None
    except (URLError, TimeoutError) as error:
        raise RuntimeError(f"Falha de conexão com a API do Instagram: {error}") from None

    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError(payload["error"].get("message", "A API do Instagram retornou um erro"))
    return payload


def main() -> None:
    if not TOKEN:
        raise RuntimeError("Configure o secret INSTAGRAM_ACCESS_TOKEN no GitHub.")

    profile = get_json(f"{BASE_URL}/me", {"fields": "id,username", "access_token": TOKEN})
    username = str(profile.get("username", "")).lower()
    if username != EXPECTED_USERNAME:
        raise RuntimeError(
            f"O token conectado pertence a @{username or 'conta não identificada'}, "
            f"mas este site espera @{EXPECTED_USERNAME}."
        )

    media_url = f"{BASE_URL}/{profile['id']}/media"
    params = {
        "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp",
        "limit": "25",
        "access_token": TOKEN,
    }
    items = []
    while media_url and len(items) < 25:
        page = get_json(media_url, params)
        items.extend(page.get("data", []))
        media_url = page.get("paging", {}).get("next")
        params = None

    posts = []
    for item in items:
        image_url = item.get("thumbnail_url") or item.get("media_url")
        permalink = item.get("permalink")
        if not image_url or not permalink:
            continue
        posts.append({
            "id": item.get("id"),
            "caption": item.get("caption", ""),
            "media_type": item.get("media_type", "IMAGE"),
            "media_url": item.get("media_url"),
            "thumbnail_url": item.get("thumbnail_url"),
            "permalink": permalink,
            "timestamp": item.get("timestamp"),
        })

    posts.sort(key=lambda post: post.get("timestamp") or "", reverse=True)
    feed = {
        "username": EXPECTED_USERNAME,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "posts": posts[:5],
    }
    OUTPUT.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Feed atualizado: {len(feed['posts'])} publicação(ões) de @{EXPECTED_USERNAME}.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(f"ERRO: {error}", file=sys.stderr)
        sys.exit(1)
