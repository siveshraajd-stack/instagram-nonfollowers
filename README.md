# Instagram Non-Followers

Find who you follow that doesn't follow you back. Runs locally, reads only
your own account's data, and nothing is uploaded anywhere.

> ⚠️ **Heads up:** this uses [`instagrapi`](https://github.com/subzeroid/instagrapi),
> an unofficial client for Instagram's private API. This isn't Instagram's
> official API, and automated access like this is against Instagram's Terms
> of Service. Use it on an account you're not worried about losing temporary
> or permanent access to — Instagram may rate-limit, challenge, or lock
> accounts that trigger its automation detection. Built for personal,
> for-fun use only, not for distribution or commercial use.

## Install

```bash
pip3 install -r requirements.txt
```

## Configure

```bash
cp .env.example .env
```

Then edit `.env` and fill in **one** of these two options:

**Option A — cookies (recommended, more reliable)**

1. Log into `instagram.com` in your browser.
2. Open DevTools:
   - **Chrome:** `View > Developer > Developer Tools` → `Application` tab → `Storage > Cookies > https://www.instagram.com`
   - **Safari:** `Safari > Settings > Advanced` → enable "Show Develop menu" → `Develop > Show Web Inspector` → `Storage`/`Resources` tab → `Cookies`
3. Copy the values for `sessionid`, `csrftoken`, and `ds_user_id` into `IG_SESSIONID`, `IG_CSRFTOKEN`, `IG_DS_USER_ID` in `.env`.

**Option B — username/password**

Fill in `IG_USERNAME` and `IG_PASSWORD`. Note: this is more likely to trigger
a login challenge or 2FA prompt, which this script doesn't handle interactively.

**Optional:**
- `IG_SESSION_FILE` — path to cache session state between runs (reduces challenges)
- `IG_HTTP_PROXY` — route requests through a proxy if your IP gets blocked

## Run

```bash
python3 nonfollowers.py
```

Prints one username per line (accounts you follow that don't follow you
back), plus a summary count on stderr.

## Security notes

- `.env` is git-ignored — never commit it.
- Don't share your `sessionid`/`csrftoken` with anyone; they grant account access.
- If you fork or publish this repo, double check `.gitignore` is catching your
  real `.env` and any `IG_SESSION_FILE` output before pushing.

## How it works

1. Logs in via cookies or credentials using `instagrapi`.
2. Fetches your `following` and `followers` lists.
3. Computes the set difference (`following - followers`).
4. Prints the result.

## License

For personal, educational use. No warranty — use at your own risk,
and at the risk of your Instagram account's standing.
