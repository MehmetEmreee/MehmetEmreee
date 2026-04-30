import os
import re
import requests

USERNAME = "MehmetEmreee"
TOKEN = os.environ.get("GH_TOKEN")

headers = {
    "Authorization": f"bearer {TOKEN}",
    "Content-Type": "application/json"
}

query = """
{
  user(login: "%s") {
    pinnedItems(first: 6, types: REPOSITORY) {
      nodes {
        ... on Repository {
          name
          description
          url
          stargazerCount
          forkCount
          primaryLanguage { name color }
        }
      }
    }
  }
}
""" % USERNAME

response = requests.post(
    "https://api.github.com/graphql",
    json={"query": query},
    headers=headers
)

repos = response.json()["data"]["user"]["pinnedItems"]["nodes"]

LANG_BADGE = {
    "C++":    "C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white",
    "Python": "Python-3776AB?style=flat-square&logo=python&logoColor=white",
    "C":      "C-A8B9CC?style=flat-square&logo=c&logoColor=black",
    "Swift":  "Swift-FA7343?style=flat-square&logo=swift&logoColor=white",
    "Dart":   "Dart-0175C2?style=flat-square&logo=dart&logoColor=white",
}

def lang_badge(lang):
    if not lang:
        return ""
    badge = LANG_BADGE.get(lang, f"{lang}-555555?style=flat-square")
    return f'<img src="https://img.shields.io/badge/{badge}" alt="{lang}" />'

rows = []
for i in range(0, len(repos), 2):
    pair = repos[i:i+2]
    cells = ""
    for repo in pair:
        lang = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else None
        desc = repo.get("description") or ""
        stars = repo["stargazerCount"]
        forks = repo["forkCount"]
        cells += f"""
    <td width="50%" valign="top">
      <h3 align="center"><a href="{repo['url']}">{repo['name']}</a></h3>
      <p align="center">{desc}</p>
      <p align="center">
        {lang_badge(lang)}
        <img src="https://img.shields.io/badge/⭐-{stars}-FFD700?style=flat-square" alt="stars" />
        <img src="https://img.shields.io/badge/🍴-{forks}-lightgrey?style=flat-square" alt="forks" />
      </p>
    </td>"""
    rows.append(f"  <tr>{cells}\n  </tr>")

pinned_section = "<table>\n" + "\n".join(rows) + "\n</table>"

with open("README.md", "r") as f:
    content = f.read()

new_content = re.sub(
    r"<!-- PINNED_REPOS_START -->.*?<!-- PINNED_REPOS_END -->",
    f"<!-- PINNED_REPOS_START -->\n{pinned_section}\n<!-- PINNED_REPOS_END -->",
    content,
    flags=re.DOTALL
)

with open("README.md", "w") as f:
    f.write(new_content)

print("README.md updated!")
