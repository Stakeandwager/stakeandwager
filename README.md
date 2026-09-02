# Stake + Wager — Wager 001

Static site. No build step, no dependencies, no server code.

```
index.html            root page, links to the open wager
wager/001/index.html  the wager brief
assets/style.css      shared styles
404.html
robots.txt            noindex while the experiment runs
```

## Before it goes live

Four edits, all in `wager/001/index.html`:

1. Replace the bio placeholder (search `One sentence`) with one line about who you are.
2. Replace `REPLACE@EXAMPLE.COM` — it appears twice.
3. Confirm the dates and the six-of-fifteen milestone, and make them match your outreach message.
4. Delete the footer line telling you to replace the email.

Search for `class="fill"` to find every remaining placeholder. If any bronze
highlight is still visible on the page, it is not ready to send.

## Deploy

Any static host. Drag the folder in.

- Netlify Drop: netlify.com/drop, then add the custom domain
- Cloudflare Pages: connect a repo or upload direct
- GitHub Pages: push, enable Pages on the branch
- Vercel: `vercel deploy`

At GoDaddy, point DNS at the host. Two records for an apex domain:
an A record on `@` and a CNAME on `www`. Values come from whichever host
you pick. Allow up to 48 hours to propagate globally, though it is usually
under an hour.

Note: GoDaddy keeps showing the for-sale lander even after a listing is
deleted. Changing the nameservers is what removes it.

## Checks before sending anyone the link

- Open it on a phone. Half of them will.
- Click the wager button, confirm the mail draft opens with the right address.
- Click the pass link too.
- View it in a private window, so you see it the way a stranger will.
