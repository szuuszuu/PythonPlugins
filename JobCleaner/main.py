import os

def parse_job_file(job_name, base_folder, visited=None):
    """
    Recursively parses a job file and builds a nested dictionary
    representing all job calls starting from the given job_name.

    Args:
        job_name (str): Name of the starting job.
        base_folder (str): Folder where job files are located.
        visited (set): Keeps track of visited jobs to prevent infinite recursion.

    Returns:
        dict: A nested dictionary representing the job call tree.
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


def print_job_tree(tree, prefix=""):
    """
    Recursively prints the nested job call tree in a visually structured format.

    Args:
        tree (dict): Nested dictionary representing the job call tree.
        prefix (str): Visual prefix used for formatting branches.
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
    Main function that prompts the user for a job name, builds the call tree,
    and prints it in a structured format.
    """
    job_name = input("Please enter the starting JOB name: ").strip()
    if not job_name:
        print("[ERROR] No job name provided.")
        return

    print(f"\nStarting from job: {job_name}")

    jobs_folder = "BACKUP1"  # Fixed folder name for job files
    job_tree = {job_name: parse_job_file(job_name, jobs_folder)}

    print("\nJob Call Tree:")
    print_job_tree(job_tree)


if __name__ == "__main__":
    main()
