# Instagram Non-Followers

Find out who you follow on Instagram that doesn't follow you back — runs
entirely on your machine, reads only your own account data, and never
uploads anything anywhere.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-personal--use-lightgrey.svg)

## ⚠️ Before you use this

This project uses [`instagrapi`](https://github.com/subzeroid/instagrapi),
an **unofficial** client for Instagram's private mobile API — not
Instagram's sanctioned developer API. Automated access like this is
against Instagram's Terms of Service.

- Instagram may rate-limit, challenge, or temporarily lock an account that
  triggers its automation detection.
- Use this on an account you're comfortable taking that risk with.
- Built for personal, for-fun, educational use — not for distribution,
  scale, or commercial use.

## What it does

1. Logs into your Instagram account (via session cookies or
   username/password).
2. Fetches your `following` and `followers` lists.
3. Computes the difference: accounts you follow who don't follow you back.
4. Prints the result, one username per line.

## Setup

**1. Clone and install dependencies**

```bash
git clone https://github.com/siveshraajd-stack/-instagram-nonfollowers.git
cd -instagram-nonfollowers
pip3 install -r requirements.txt
```

**2. Configure your credentials**

```bash
cp .env.example .env
```

Edit `.env` and fill in **one** of the two options below.

| Option | Variables | Notes |
|---|---|---|
| **A — Cookies** *(recommended)* | `IG_SESSIONID`, `IG_CSRFTOKEN`, `IG_DS_USER_ID` | More reliable, less likely to trigger a challenge |
| B — Username/password | `IG_USERNAME`, `IG_PASSWORD` | Simpler, but can trigger 2FA/challenge prompts this script doesn't handle |

**How to get your cookies:**

<details>
<summary>Chrome</summary>

1. Log into `instagram.com`
2. Open DevTools (`F12` or right-click → Inspect)
3. Go to **Application** → **Storage** → **Cookies** → `https://www.instagram.com`
4. Copy the values for `sessionid`, `csrftoken`, `ds_user_id`
</details>

<details>
<summary>Safari</summary>

1. `Safari > Settings > Advanced` → enable **Show Develop menu**
2. Log into `instagram.com`
3. `Develop > Show Web Inspector` → **Storage**/**Resources** tab → **Cookies**
4. Copy the values for `sessionid`, `csrftoken`, `ds_user_id`
</details>

**3. Run it**

```bash
python3 nonfollowers.py
```

Output looks like:

```
some_username
another_username
...
Total not following back: 2
```

## Optional config

| Variable | Purpose |
|---|---|
| `IG_SESSION_FILE` | Path to cache session state between runs, reducing login challenges |
| `IG_HTTP_PROXY` | Route requests through a proxy if your IP gets blocked |

## Security

- `.env` holds your real secrets and is **git-ignored** — never commit it.
- Only `.env.example` (blank placeholders) should ever be pushed.
- Your `sessionid`/`csrftoken` are effectively login keys — treat them like
  a password. Don't paste them into chats, issues, or screenshots.
- Before pushing, always run `git status` and confirm `.env` is **not**
  listed.

## Project structure

```
.
├── nonfollowers.py     # main script
├── requirements.txt    # dependencies
├── .env.example        # credential template (safe to commit)
├── .env                # your real credentials (git-ignored, local only)
├── .gitignore
└── README.md
```

## How it works (technical)

- Authenticates with `instagrapi`, injecting cookies directly or logging
  in with credentials.
- Calls the private API's `user_following` / `user_followers` endpoints,
  falling back to the public GraphQL versions if those fail.
- Normalizes usernames (strips `@`, lowercases) and takes a set difference.

## Limitations

- No interactive 2FA/challenge handling — if Instagram blocks the login,
  the script exits with an error rather than prompting you.
- Large accounts (many thousands of follows) may take a while due to
  Instagram's internal pagination/rate limits.

## License

Personal, educational use only. No warranty — use at your own risk, and
at the risk of your Instagram account's standing.