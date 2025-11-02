
import tkinter as tk
from tkinter import messagebox

# -------------------- Job Scheduling Logic --------------------
def schedule_jobs():
    try:
        # Get input from text box
        raw_data = input_box.get("1.0", tk.END).strip()
        if not raw_data:
            messagebox.showerror("Error", "Please enter some job data!")
            return

        # Parse input lines
        jobs = []
        for line in raw_data.splitlines():
            parts = line.split()
            if len(parts) != 3:
                messagebox.showerror("Error", f"Invalid input line: {line}")
                return
            job_id, deadline, profit = parts[0], int(parts[1]), int(parts[2])
            jobs.append((job_id, deadline, profit))

        # Sort by profit descending
        jobs.sort(key=lambda x: x[2], reverse=True)

        # Find maximum deadline
        max_deadline = max(job[1] for job in jobs)

        # Create slots
        slots = [None] * (max_deadline + 1)

        # Schedule jobs
        for job in jobs:
            job_id, deadline, profit = job
            for t in range(deadline, 0, -1):
                if slots[t] is None:
                    slots[t] = job_id
                    break

        scheduled_jobs = [job for job in slots if job is not None]
        total_profit = sum(job[2] for job in jobs if job[0] in scheduled_jobs)

        # Show output
        output_label.config(
            text=f"Scheduled Jobs: {', '.join(scheduled_jobs)}\nTotal Profit: {total_profit}",
            fg="green"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------- GUI Design --------------------
root = tk.Tk()
root.title("Job Scheduling Problem - Greedy Algorithm")
root.geometry("500x400")
root.config(bg="#F0F4F8")

# Title Label
tk.Label(root, text="Job Scheduling Problem", font=("Helvetica", 18, "bold"), bg="#F0F4F8", fg="#2C3E50").pack(pady=10)

# Instruction Label
tk.Label(
    root,
    text="Enter Jobs (Format: JobID Deadline Profit)\nExample:\nJ1 2 60\nJ2 1 100\nJ3 3 20",
    bg="#F0F4F8",
    fg="#555555",
    font=("Helvetica", 10)
).pack(pady=5)

# Input Text Box
input_box = tk.Text(root, height=8, width=40, font=("Consolas", 11))
input_box.pack(pady=10)
input_box.insert(tk.END, "J1 2 60\nJ2 1 100\nJ3 3 20\nJ4 2 40\nJ5 1 20")

# Submit Button
tk.Button(
    root,
    text="Schedule Jobs",
    font=("Helvetica", 12, "bold"),
    bg="#3498DB",
    fg="white",
    padx=10,
    pady=5,
    relief="raised",
    command=schedule_jobs
).pack(pady=10)

# Output Label
output_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), bg="#F0F4F8")
output_label.pack(pady=20)

# Run the app
root.mainloop()
