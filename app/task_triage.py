app_name = "TaskFlow"

print(f"Starting {app_name} Task Triage Engine...")
print("Loaded 3 sample tasks.")
print("Ready to analyze.")

raw_title = "  fix LOGIN bug  "
clean = raw_title.strip().lower().title()
print(f"Clean title: {clean}")

slug = clean.lower().replace(" ", "-")
print(f"Slug: {slug}")

raw_titles = ["  fix LOGIN bug ", "review   pull request", "Deploy HOTFIX  "]

for raw in raw_titles:
    display = raw.strip().lower().title()
    slug = display.lower().replace(" ", "-")
    print(f"Clean title: {display}")
    print(f"Slug: {slug}")

raw_email = "  ALICE@Example.COM  "
clean_email = raw_email.strip().lower()
print(f"Clean email: {clean_email}")
