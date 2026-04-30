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
          primaryLanguage {
            name
          }
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

data = response.json()
repos = data["data"]["user"]["pinnedItems"]["nodes"]

md_lines = ["## 📌 Pinned Repositories\n"]
for repo in repos:
    lang = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A"
    desc = repo["description"] or ""
    md_lines.append(
        f"- **[{repo['name']}]({repo['url']})** — {desc} "
        f"`{lang}` ⭐{repo['stargazerCount']} 🍴{repo['forkCount']}"
    )

pinned_section = "\n".join(md_lines)

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
