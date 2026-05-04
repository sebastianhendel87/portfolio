# Portfolio (static HTML)

**Repo:** [github.com/sebastianhendel87/portfolio](https://github.com/sebastianhendel87/portfolio)

## Preview on your Mac

In Terminal, **only** run:

```bash
python3 serve.py
```

The script prints the **exact** `http://localhost:…` URL (it tries **8888** first, or the next free port if that one is busy). Open that link in Chrome. If `npm run dev` fails with a lock error, run `npm run dev:unlock` and try again (see `PORTFOLIO_FLOW.txt`).

## Preview on the web

**GitHub Pages** (only after you turn it on): repo **Settings → Pages → Build and deployment → Source: Deploy from a branch** → branch **`main`**, folder **`/` (root)** → Save. After a minute or two the site should be at:

**https://sebastianhendel87.github.io/portfolio/**

If that URL **404s**, Pages is not enabled for this repo yet, or the deploy is still running—check the same Settings page for a green status or error.

**Vercel:** this repo includes `vercel.json` (static build). If you already connected the repo on [vercel.com](https://vercel.com), your live URL is under that project’s **Deployments** (e.g. `something.vercel.app`), not necessarily GitHub Pages.

---

*There is a Next.js app under `src/` from the template; the portfolio is the `.html` files in the repo root.*
