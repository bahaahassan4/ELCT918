# ELCT918 Course — Lab Assignments

This repository is the **README and shared workspace for the ELCT918 course**.

We will use this repository to collect and organize **all lab assignments** for the course.

Each lab assignment should be added to the repository in its own folder, for example:

```text
ELCT918/
├── README.md
├── Lab 1/
│   ├── ...
│   └── README.md
├── Lab 2/
│   ├── ...
│   └── README.md
├── Lab 3/
│   ├── ...
│   └── README.md
└── ...
```

The repository is shared between the course collaborators, so we will use Git branches and Pull Requests when working on assignments.

---

# Git Collaboration Workflow

## 1. What does `nothing to commit, working tree clean` mean?

If you run:

```bash
git commit -m "Adding folder Lab 1 assignment"
```

and Git shows:

```text
On branch main
nothing to commit, working tree clean
```

this is **not an error**.

It means Git currently does not see any new or modified files that need to be committed.

There are several possible reasons.

---

## 2. The files are already committed

Check the Git history:

```bash
git log --oneline --all
```

You may see something like:

```text
a83f21c Initial commit
```

This means the files may already be included in an earlier commit.

You can also check:

```bash
git status
```

---

## 3. The folder is empty

Git does **not track empty folders**.

For example:

```text
task1/
└── Lab 1 assignment/
```

If `Lab 1 assignment` contains no files, Git will ignore the folder.

Add a file inside it, for example:

```text
Lab 1 assignment/
└── README.md
```

Then run:

```bash
git status
git add .
git commit -m "Add Lab 1 assignment"
```

---

## 4. The files are ignored by `.gitignore`

A `.gitignore` file can tell Git not to track certain files or folders.

Check ignored files with:

```bash
git status --ignored
```

If your files appear under:

```text
Ignored files:
```

then `.gitignore` is preventing Git from tracking them.

---

## 5. The files were already committed

For example, if you previously ran:

```bash
git add .
git commit -m "Initial commit"
```

and then added your Lab 1 files afterward, Git should normally show them as untracked:

```text
Untracked files:
  Lab 1 assignment/
```

Then run:

```bash
git add .
git commit -m "Add Lab 1 assignment"
```

---

## 6. What to do when Git does not see your files

Run these two commands:

```bash
git status
```

and:

```bash
git log --oneline --all --decorate -5
```

### `git status`

Shows:

- Current branch
- Modified files
- New/untracked files
- Staged files
- Whether the working tree is clean

### `git log`

Shows recent commits in your repository.

For example:

```text
a83f21c Initial commit
```

---

# Basic Git Workflow for the Project

If you and your colleague are working on the same project, use this workflow.

## Start working

First update your local `main` branch:

```bash
git checkout main
git pull origin main
```

Then create your own branch:

```bash
git checkout -b bahaa-task1
```

Now make your changes.

---

## Save your work

Check what changed:

```bash
git status
```

Add your changes:

```bash
git add .
```

Commit them:

```bash
git commit -m "Implement task 1"
```

Push your branch:

```bash
git push -u origin bahaa-task1
```

Then create a **Pull Request** on GitHub:

```text
bahaa-task1 -> main
```

After review, the Pull Request can be merged into `main`.

---

## Start your next task

After your previous branch has been merged:

```bash
git checkout main
git pull origin main
git checkout -b bahaa-task2
```

Then continue working.

---

# Recommended Collaboration Structure

Do not normally work directly on `main`.

Use separate branches:

```text
                  GitHub
                    |
                   main
                  /    \
                 /      \
        bahaa-task1   colleague-task1
             |              |
            work           work
             |              |
           push           push
             |              |
            PR             PR
             \              /
              \            /
                   main
```

This allows both people to work simultaneously while reducing the risk of overwriting each other's changes.

---

# Daily Git Cheat Sheet

```bash
# Start working
git checkout main
git pull origin main
git checkout -b my-feature

# Work on the project...

# Save your changes
git status
git add .
git commit -m "Describe my changes"
git push -u origin my-feature

# Create a Pull Request on GitHub

# After the Pull Request is merged
git checkout main
git pull origin main

# Create a new branch for the next task
git checkout -b my-next-feature
```

## Important Rule

**Avoid working directly on `main`.**

Use a separate branch for each task or feature, push the branch to GitHub, and use a Pull Request to merge your work into `main`.
