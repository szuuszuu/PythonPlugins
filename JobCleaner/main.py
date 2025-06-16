import os


def parse_job_file(job_name, base_folder, visited=None):
    """
    Recursively parses a job file and builds a nested dictionary
    representing all job calls starting from the given job_name.
    """
    if visited is None:
        visited = set()
    
    # Avoid circular job calls
    if job_name in visited:
        return {}

    visited.add(job_name)

    # Construct the full path to the job file
    job_path = os.path.join("JobCleaner", base_folder, job_name + ".JBI")
    job_tree = {}

    try:
        with open(job_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if line.startswith("CALL JOB:"):
                # Extract the called job name after "CALL JOB:"
                called_job = line.split("CALL JOB:")[-1].strip()
                # Recursively parse the called job
                job_tree[called_job] = parse_job_file(called_job, base_folder, visited)

    except FileNotFoundError:
        print(f"[ERROR] File '{job_name}.JBI' not found in folder: {base_folder}")

    return job_tree


def collect_all_jobs(job_tree):
    """
    Recursively collects all job names from the nested job tree.
    """
    jobs = set()
    for job, sub_tree in job_tree.items():
        jobs.add(job)
        jobs.update(collect_all_jobs(sub_tree))
    return jobs


def print_job_tree(tree, prefix=""):
    """
    Recursively prints the nested job call tree in a visually structured format.
    """
    last_key = list(tree.keys())[-1] if tree else None

    for job, sub_tree in tree.items():
        is_last = (job == last_key)
        branch = "└── " if is_last else "├── "
        print(prefix + branch + job)

        # Extend the prefix for nested jobs
        extension = "    " if is_last else "│   "
        print_job_tree(sub_tree, prefix + extension)


def main():
    """
    Main function to:
    - Prompt user for a job name
    - Build the job call tree
    - Print it nicely
    - Delete unused .JBI files from the folder
    """
    job_name = input("Please enter the starting JOB name: ").strip()
    if not job_name:
        print("[ERROR] No job name provided.")
        return

    jobs_folder = "BACKUP1"  # Fixed input folder
    job_folder_path = os.path.join("JobCleaner", jobs_folder)
    job_file_path = os.path.join(job_folder_path, job_name + ".JBI")

    # Safety check: starting job must exist
    if not os.path.exists(job_file_path):
        print(f"[ERROR] Starting job file not found: {job_file_path}")
        print("[ABORTED] No files will be deleted.")
        return

    print(f"\nStarting from job: {job_name}")

    job_tree = {job_name: parse_job_file(job_name, jobs_folder)}

    print("\nJob Call Tree:")
    print_job_tree(job_tree)

    # Get all job names used in the tree
    used_jobs = collect_all_jobs(job_tree[job_name])
    used_jobs.add(job_name)

    if not os.path.exists(job_folder_path):
        print(f"[ERROR] Folder '{job_folder_path}' does not exist.")
        return

    all_files = [f for f in os.listdir(job_folder_path) if f.endswith(".JBI")]

    print("\nCleaning up unused .JBI files...")
    for filename in all_files:
        job_base = os.path.splitext(filename)[0]
        if job_base not in used_jobs:
            full_path = os.path.join(job_folder_path, filename)
            try:
                os.remove(full_path)
                print(f"[DELETED] {filename}")
            except Exception as e:
                print(f"[ERROR] Could not delete {filename}: {e}")
        else:
            print(f"[KEPT] {filename}")

if __name__ == "__main__":
    main()