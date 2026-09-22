# ELCT918 — Lab Assignments Repository

Welcome to the **ELCT918 course lab repository**.

This repository is used to collect, organize, and submit all lab assignments for the course.

Each lab assignment should have its own folder containing:
- Assignment files
- Source code (if applicable)
- Reports
- Screenshots/results
- A `README.md` explaining the work

---

# Course Lab Progress Tracker

| Task | Assignment Title | Status | Submission Folder | Notes |
|------|------------------|--------|-------------------|-------|
| Lab 1 | Multi-Objective Design Space Exploration of Neural Network Hyperparameters | ✅ Completed | `Lab 1 assignment/` | |
| Lab 2 | TBD | ⬜ Not Completed | `Lab 2/` | |
| Lab 3 | TBD | ⬜ Not Completed | `Lab 3/` | |
| Lab 4 | TBD | ⬜ Not Completed | `Lab 4/` | |
| Lab 5 | TBD | ⬜ Not Completed | `Lab 5/` | |

### Status Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Completed |
| 🔄 | In Progress |
| ⬜ | Not Started |

---

# Repository Structure

The repository should follow this structure:

```

ELCT918/
│
├── README.md
│
├── Lab 1/
│   ├── README.md
│   ├── source_files/
│   └── report.pdf
│
├── Lab 2/
│   ├── README.md
│   ├── source_files/
│   └── report.pdf
│
├── Lab 3/
│   ├── README.md
│   └── ...
│
└── ...

```

---

# Lab Submission Guidelines

For every lab:

1. Create a new folder:

```

Lab X/

```

2. Add your assignment files.

3. Add a `README.md` inside the lab folder containing:

- Lab objective
- Tools/software used
- Implementation steps
- Results
- Screenshots (if needed)

Example:

```

Lab 1 assignment/
│
├── README.md
├── code/
├── results/
└── report.pdf

````

---

# GitHub Collaboration Workflow

## 1. Clone the Repository

First time only:

```bash
git clone <repository-link>
cd ELCT918
````

---

## 2. Update Your Local Repository

Before starting any work:

```bash
git checkout main
git pull origin main
```

This downloads the latest changes.

---

## 3. Create Your Own Branch

Do not work directly on `main`.

Create a branch:

```bash
git checkout -b your-name-task
```

Example:

```bash
git checkout -b mahmoud-lab1
```

---

## 4. Add Your Changes

After finishing your work:

Check changes:

```bash
git status
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Add Lab 1 submission"
```

---

## 5. Push Your Branch

Upload your branch:

```bash
git push -u origin your-name-task
```

Example:

```bash
git push -u origin mahmoud-lab1
```

---

## 6. Create Pull Request

On GitHub:

```
your-branch  →  main
```

Create a Pull Request.

After review, the changes can be merged into `main`.

---

# Useful Git Commands

Check repository status:

```bash
git status
```

View commit history:

```bash
git log --oneline
```

Update repository:

```bash
git pull origin main
```

Create a new branch:

```bash
git checkout -b branch-name
```

Switch branch:

```bash
git checkout branch-name
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "message"
```

Push changes:

```bash
git push
```

---

# Important Rules

✅ Create a separate branch for every lab/task.

✅ Commit changes with clear messages.

✅ Pull the latest `main` before starting new work.

✅ Use Pull Requests to merge changes.

❌ Do not directly modify the `main` branch.

---

# Contributors

| Name | Role |
| ---- | ---- |
| Bahaa ElDin Hassan     |      |
| Shrouq Mohamed     |      |
