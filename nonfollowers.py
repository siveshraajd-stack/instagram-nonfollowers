#!/usr/bin/env python3

"""
Instagram Non-Followers

Find accounts you follow that don't follow you back. Runs locally,
reads your own account data only, and prints the results to stdout.

Setup:
    1. pip3 install -r requirements.txt
    2. cp .env.example .env
    3. Fill in .env with your username/password OR browser cookies
    4. python3 nonfollowers.py

See README.md for how to get the cookie values from Chrome/Safari.
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path
from typing import Set, Optional, Iterable, Any

from dotenv import load_dotenv

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ChallengeRequired, TwoFactorRequired, ClientError
except Exception:
    sys.stderr.write(
        "Missing dependency: instagrapi. Install it with: pip3 install -r requirements.txt\n"
    )
    raise

load_dotenv()

USERNAME: Optional[str] = os.getenv("IG_USERNAME") or None
PASSWORD: Optional[str] = os.getenv("IG_PASSWORD") or None
SESSIONID: Optional[str] = os.getenv("IG_SESSIONID") or None
CSRFTOKEN: Optional[str] = os.getenv("IG_CSRFTOKEN") or None
DS_USER_ID: Optional[str] = os.getenv("IG_DS_USER_ID") or None
SESSION_FILE: Optional[str] = os.getenv("IG_SESSION_FILE") or None
HTTP_PROXY: Optional[str] = os.getenv("IG_HTTP_PROXY") or None


def normalize_username(username: str) -> str:
    return username.strip().lstrip("@").lower()


def collect_usernames(container: Any) -> Set[str]:
    """Collect usernames from a dict[int, UserShort] or list[UserShort]."""
    usernames: Set[str] = set()
    if isinstance(container, dict):
        iterable: Iterable[Any] = container.values()
    elif isinstance(container, list):
        iterable = container
    else:
        iterable = []
    for user in iterable:
        try:
            usernames.add(normalize_username(getattr(user, "username")))
        except Exception:
            continue
    return usernames


def main() -> int:
    if not SESSIONID and (not USERNAME or not PASSWORD):
        sys.stderr.write(
            "Missing credentials. Copy .env.example to .env and fill in either:\n"
            "  IG_USERNAME + IG_PASSWORD, or\n"
            "  IG_SESSIONID (+ IG_CSRFTOKEN, IG_DS_USER_ID)\n"
        )
        return 1

    client = Client()

    if SESSION_FILE:
        path = Path(SESSION_FILE).expanduser()
        if path.is_file():
            try:
                client.load_settings(json.loads(path.read_text(encoding="utf-8")))
            except Exception:
                pass

    if HTTP_PROXY:
        try:
            client.set_proxy(HTTP_PROXY)
        except Exception:
            pass

    try:
        if SESSIONID:
            for jar in (client.public.cookies, client.private.cookies):
                try:
                    jar.set("sessionid", SESSIONID, domain=".instagram.com", path="/")
                    if CSRFTOKEN:
                        jar.set("csrftoken", CSRFTOKEN, domain=".instagram.com", path="/")
                    if DS_USER_ID:
                        jar.set("ds_user_id", DS_USER_ID, domain=".instagram.com", path="/")
                except Exception:
                    pass
            client.login_by_sessionid(SESSIONID)
        else:
            client.login(USERNAME, PASSWORD)
    except TwoFactorRequired:
        sys.stderr.write("Login failed: two-factor authentication required (not handled by this script).\n")
        return 2
    except ChallengeRequired:
        sys.stderr.write("Login failed: Instagram requested additional verification (challenge).\n")
        return 2
    except LoginRequired:
        sys.stderr.write("Login failed: invalid credentials or login required.\n")
        return 2
    except ClientError as exc:
        sys.stderr.write(f"Login failed: {exc}\n")
        return 2

    if SESSION_FILE:
        try:
            Path(SESSION_FILE).expanduser().write_text(json.dumps(client.get_settings()), encoding="utf-8")
        except Exception:
            pass

    # Resolve the logged-in account's own user id
    try:
        me = client.account_info()
        my_user_id = me.pk
    except Exception:
        try:
            my_user_id = client.user_id_from_username(USERNAME or "")
        except Exception as exc:
            sys.stderr.write(f"Failed to resolve your user id: {exc}\n")
            return 3

    try:
        try:
            following_container = client.user_following_v1(my_user_id)
        except Exception:
            following_container = client.user_following(my_user_id)

        try:
            followers_container = client.user_followers_v1(my_user_id)
        except Exception:
            followers_container = client.user_followers(my_user_id)
    except ClientError as exc:
        sys.stderr.write(f"Failed to fetch followers/following: {exc}\n")
        return 4
    except Exception as exc:
        sys.stderr.write(f"Unexpected error while fetching: {exc}\n")
        return 4

    following_usernames = collect_usernames(following_container)
    followers_usernames = collect_usernames(followers_container)
    not_following_back = sorted(following_usernames - followers_usernames)

    for username in not_following_back:
        print(username)

    sys.stderr.write(f"Total not following back: {len(not_following_back)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
