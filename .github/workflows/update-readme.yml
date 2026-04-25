name: Update README with Pinned Repos

on:
  schedule:
    - cron: "0 */6 * * *"   # 6 saatte bir güncelle
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install requests

      - name: Run update script
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python update_readme.py

      - name: Commit and push if changed
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --cached --quiet || git commit -m "chore: auto-update pinned repos [skip ci]"
          git push
