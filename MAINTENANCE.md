# Profile 2.0 maintenance

This repository contains the Developer Playground profile redesign. The previous assets are retained in Git history and on disk; the README uses `assets/v2/`.

## Original assets

The new header has a native desktop height of 110 pixels instead of the previous 440-pixel banner. It is followed by a profile scan, grouped toolbox, selected work and a public contribution calendar. Mobile variants use larger text and stacked information. SVG CSS provides a cursor, scan line and pixel-satellite movement. `prefers-reduced-motion` stops those animations. There is no JavaScript in the README or its SVG files.

The animation is decorative. It does not erase, fabricate or alter contribution cells. The numeric data and dates come from the unauthenticated GitHub calendar. All contact links go to GitHub. Opero Docs is described only at the general level the owner authorized.

## Refresh manually

Python 3.10+ and its standard library are sufficient:

```sh
python3 scripts/sync_github.py
python3 scripts/render_profile.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

The public-only collector reads neither credentials nor private repositories. It rejects changed or inconsistent calendar markup before replacing data. `data/github.json` and `assets/v2/` are the only files refreshed by the workflow. The capture date remains visible so old snapshots are never represented as live data.

`.github/workflows/public-signals.yml` supports a weekly update and manual dispatch. It uses the repository-scoped token only for its final commit and push. Refresh commits are authored by `github-actions[bot]`, not Emmanuel; they must not be used to inflate the owner's contribution record. A failed data refresh leaves the published assets unchanged.

## Connect the portfolio after it is live

The README links to the verified public portfolio. If that marked integration needs to be restored after a future edit, run:

```sh
python3 scripts/activate_portfolio.py
```

The script first checks the real Pages URL and expected identity. Only then does it replace the marked README section with the portfolio link. It does not commit or push. Review the diff and publish that final integration in the same approved release process.

## Compatibility checks and publication

Check Markdown rendering, responsive variants and animated frames locally before publishing changes. After a release, also check the actual GitHub profile and image CDN. The portfolio is deployed separately at https://gvemmanuel3712-cyber.github.io/.

Publish only the intended branch changes after approval. Do not change the visibility of application repositories, push unrelated branches, or upload local review reports.
