# Lingua — AI-Based Multilingual Language Translation Tool

A student mini-project starter based on the supplied synopsis. It uses a responsive HTML/CSS/JavaScript frontend, a Python Flask API, LibreTranslate for translation and automatic language detection, and browser-local history for the first deployment milestone.

## Current features
- Responsive translator UI
- Source language auto-detection (LibreTranslate `source: auto`)
- Target language selection
- Copy translated output
- Swap languages
- Recent translation history saved in the current browser using `localStorage`
- Flask endpoints: `/api/health`, `/api/languages`, `/api/translate`
- Ready for Vercel's native Python/Flask deployment

## Important note about the synopsis
The synopsis specifies Firebase Firestore for persistent cloud history. This starter currently saves history in the browser, not Firestore. This makes the first milestone easy to deploy and test. Firebase Authentication + Firestore can be added as the next milestone so history can sync across devices and users.

## 1. Configure LibreTranslate
The default provider URL is `https://libretranslate.com`. That managed service requires an API key. Obtain one from https://portal.libretranslate.com and set these environment variables in Vercel:

- `LIBRETRANSLATE_URL` = `https://libretranslate.com`
- `LIBRETRANSLATE_API_KEY` = your private API key

The backend reads the key from the server environment. Do not put the key in `index.html` or commit it to GitHub. You can use a different LibreTranslate-compatible instance by changing `LIBRETRANSLATE_URL`; whether a key is needed depends on that instance.

## 2. Deploy with GitHub + Vercel
1. Create a GitHub account at https://github.com if you do not already have one.
2. Create a new repository named `language-translation-tool`.
3. Upload all files and folders from this project ZIP to the repository's root. Keep `app.py`, `requirements.txt`, `.python-version`, `vercel.json`, and `public/` at the root level.
4. Open https://vercel.com and sign in with GitHub.
5. Choose **Add New → Project**, import `language-translation-tool`, and deploy. Vercel detects the Flask app from the root `app.py` file.
6. In Vercel, open **Project → Settings → Environment Variables**. Add `LIBRETRANSLATE_URL` and `LIBRETRANSLATE_API_KEY` for Production (and Preview if desired).
7. Redeploy after adding the variables.
8. Open the deployment URL and test English → Hindi and English → Spanish.

## 3. Test endpoints
- `https://YOUR-VERCEL-DOMAIN/api/health`
- `https://YOUR-VERCEL-DOMAIN/api/languages`

## 4. Run locally (optional)
Python 3.12+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

## Troubleshooting
- If translation says the provider needs an API key, add `LIBRETRANSLATE_API_KEY` in Vercel and redeploy.
- If `/api/languages` fails, check the provider URL and provider status.
- Browser history is per browser/device and can be cleared from the page. It is not cloud-synced until Firestore is implemented.
