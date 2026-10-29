# UK Rugby Club Directory — Blog System

## How to publish a new article

### Step 1 — Create a Markdown file

Add a new `.md` file to `/content/blog/` using a URL-friendly slug as the filename:

```
/content/blog/my-article-slug.md
```

The slug becomes the URL: `ukrugbyclubdirectory.co.uk/blog/my-article-slug`

**Allowed characters in slugs:** lowercase letters, numbers, and hyphens only. No spaces, no uppercase, no special characters.

---

### Step 2 — Add frontmatter

Every `.md` file must start with a frontmatter block enclosed in triple dashes `---`:

```markdown
---
title: Your Article Title Here
date: 2026-06-15
metaDescription: A concise 150-160 character summary for Google search results. Write this as a complete sentence.
author: UK Rugby Club Directory
category: Beginners Guide
image: /imgs/rugby-union-hero.jpg
---

Your article content starts here...
```

#### Frontmatter fields

| Field             | Required | Description |
|-------------------|----------|-------------|
| `title`           | ✅ Yes   | The article headline. Shown as H1 and in `<title>` tag. |
| `date`            | ✅ Yes   | Publication date in `YYYY-MM-DD` format. |
| `metaDescription` | ✅ Yes   | 150-160 chars for Google. Used in `<meta name="description">`. |
| `author`          | ✅ Yes   | Author name. Use "UK Rugby Club Directory" for team posts. |
| `category`        | Optional | Displayed as a pill on the hero and card. E.g. "County Guides", "Beginners Guide", "Rugby Explained". |
| `image`           | Optional | Path to a hero image. Use existing site images e.g. `/imgs/rugby-union-hero.jpg`. Leave blank for default. |

---

### Step 3 — Write your content

Use standard Markdown syntax after the frontmatter block:

```markdown
## Section Heading

Regular paragraph text goes here. You can use **bold**, *italic*, and `inline code`.

### Subsection

- Bullet point one
- Bullet point two
- Bullet point three

1. Numbered list item
2. Another item

> This is a blockquote. Use it for key quotes or callouts.

[Link text](https://example.com)

---
```

---

### Step 4 — Update the index.json

Open `/content/blog/index.json` and add your article to the **top** of the array (newest first):

```json
[
  {
    "slug": "my-article-slug",
    "title": "Your Article Title Here",
    "date": "2026-06-15",
    "author": "UK Rugby Club Directory",
    "category": "Beginners Guide",
    "metaDescription": "Your 150-160 char meta description.",
    "excerpt": "Your 150-160 char meta description.",
    "image": "/imgs/rugby-union-hero.jpg"
  },
  ...existing articles...
]
```

The `excerpt` field is what shows on the blog index card. You can copy your `metaDescription` here or write a slightly different version.

---

### Step 5 — Deploy

Commit and push both files to GitHub:
1. `/content/blog/my-article-slug.md`
2. `/content/blog/index.json` (updated)

Netlify will deploy automatically. Your article will be live at:
`ukrugbyclubdirectory.co.uk/blog/my-article-slug`

---

## Available image paths

These images already exist on the site and can be used as article hero images:

| Path | Description |
|------|-------------|
| `/imgs/home-hero.jpg` | General rugby / players |
| `/imgs/rugby-union-hero.jpg` | Rugby Union action |
| `/imgs/rugby-league-hero.jpg` | Rugby League action |
| `/imgs/rugby-joints-hero.jpg` | Rugby business / equipment |
| `/imgs/find-rugby-now.jpg` | Pitch / match day |

To use a custom image, upload it to `/imgs/` and reference the path in frontmatter.

---

## How the system works

- Netlify Edge Functions intercept requests to `/blog` and `/blog/*`
- The edge function reads the `.md` file from `/content/blog/{slug}.md`
- Frontmatter is parsed for title, date, meta, author, category
- Markdown is converted to HTML inline — no build step, no npm
- The full page is rendered with the exact site header, nav, footer and CSS
- The blog index reads `/content/blog/index.json` to build the article grid

No build tools. No Node. No CMS. Just Markdown files and Git.
