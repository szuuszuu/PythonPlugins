# 🧹 JobCleaner

**JobCleaner** is a Python utility that parses `.JBI` job files, builds a call tree from a starting job, and safely deletes unused job files from a folder.

---

## ⚠️ Important Setup

> **Before running the script, make sure to place all your `.JBI` job files into the folder:**
>
> ```
> JobCleaner/JOBS_FOLDER/
> ```
> This is the default job folder used by the program.

---

## 📌 What It Does

- ✅ Starts from a specified job file (e.g., `MAIN.JBI`)
- 🔁 Recursively parses all `CALL JOB:` references to build a full job call tree
- 🧼 Deletes any `.JBI` files in the folder that are **not used** in the job call tree
- 🔐 Does **not delete anything** if the starting job is missing

---

## 📁 Folder Structure (Expected)

your_project/
- JobCleaner/
    - JOBS_FOLDER/
        - MAIN.JBI
        - SUB1.JBI
        - unused_job.JBI
    - job_cleaner.py

---

## ▶️ How to Use

1. **Run the script:**
   ```bash
   python job_cleaner.py

2. **When prompted:**
    Please enter the starting JOB name: MAIN

3. **The script will:**
    - Build the job call tree starting from MAIN.JBI
    - Print the tree in a visual format
    - Delete .JBI files in the folder that are not part of the call tree
