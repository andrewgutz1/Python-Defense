import os

# Function to load subjects and activities from a plain text file
def load_subjects(filename):
    subjects = {}
    if os.path.exists(filename):
        with open(filename, "r") as file:
            current_subject = None
            for line in file:
                line = line.strip()
                if line.endswith(":"):  # Line indicates a subject
                    current_subject = line[:-1]
                    subjects[current_subject] = []
                elif current_subject and line:  # Line indicates an activity
                    activity, status = line.rsplit(" - ", 1)
                    subjects[current_subject].append([activity, status == "Done"])
    return subjects

# Function to save subjects and activities to a plain text file
def save_subjects(subjects, filename):
    with open(filename, "w") as file:
        for subject, activities in subjects.items():
            file.write(f"{subject}:\n")
            for activity, status in activities:
                status_text = "Done" if status else "Pending"
                file.write(f"{activity} - {status_text}\n")
            file.write("\n")

# Function to display subjects and activities
def display_subjects(subjects, user_name):
    print("Your Subjects and Activities:")
    if not subjects:
        print("No subjects added yet.")
    else:
        for subject, activities in subjects.items():
            print(f"\n• {subject}:")
            for idx, (activity, status) in enumerate(activities, 1):
                status_text = "Done" if status else "Pending"
                print(f"  {idx}. {activity} - {status_text}")
    print()

# Function to manage subjects and activities
def manage_subjects(subjects, filename):
    while True:
        print("\nSubject Management:")
        print("1. Add a subject")
        print("2. Add an activity to a subject")
        print("3. Remove a subject")
        print("4. Remove an activity from a subject")
        print("5. Mark an activity as done")
        print("6. Back to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":  # Add a subject
            while True:
                subject = input("Enter the new subject name (or type 'back' to return): ")
                if subject.lower() == "back":
                    break
                elif subject in subjects:
                    print("Subject already exists.")
                else:
                    subjects[subject] = []
                    print(f"Subject '{subject}' added.")
                    break

        elif choice == "2":  # Add an activity
            while True:
                print("\nAvailable Subjects:")
                for idx, subject in enumerate(subjects.keys(), 1):
                    print(f"  {idx}. {subject}")
                subject_index = input("Enter the subject number or name (or type 'back' to return): ").strip()
                if subject_index.lower() == "back":
                    break
                elif subject_index.isdigit():
                    subject_index = int(subject_index) - 1
                    if 0 <= subject_index < len(subjects):
                        subject = list(subjects.keys())[subject_index]
                        activity = input(f"Enter the activity for {subject}: ")
                        subjects[subject].append([activity, False])
                        print(f"Activity added to {subject}.")
                        break
                    else:
                        print("Invalid subject number.")
                elif subject_index in subjects:
                    subject = subject_index
                    activity = input(f"Enter the activity for {subject}: ")
                    subjects[subject].append([activity, False])
                    print(f"Activity added to {subject}.")
                    break
                else:
                    print(f"Subject '{subject_index}' does not exist.")

        elif choice == "3":  # Remove a subject
            while True:
                print("\nAvailable Subjects:")
                for idx, subject in enumerate(subjects.keys(), 1):
                    print(f"  {idx}. {subject}")
                subject_index = input("Enter the subject number or name to remove (or type 'back' to return): ").strip()
                if subject_index.lower() == "back":
                    break
                elif subject_index.isdigit():
                    subject_index = int(subject_index) - 1
                    if 0 <= subject_index < len(subjects):
                        subject = list(subjects.keys())[subject_index]
                        del subjects[subject]
                        print(f"Subject '{subject}' removed.")
                        break
                    else:
                        print("Invalid subject number.")
                elif subject_index in subjects:
                    del subjects[subject_index]
                    print(f"Subject '{subject_index}' removed.")
                    break
                else:
                    print(f"Subject '{subject_index}' does not exist.")

        elif choice == "4":  # Remove an activity
            while True:
                print("\nAvailable Subjects:")
                for idx, subject in enumerate(subjects.keys(), 1):
                    print(f"  {idx}. {subject}")
                subject = input("Enter the subject name (or type 'back' to return): ").strip()
                if subject.lower() == "back":
                    break
                if subject in subjects and subjects[subject]:
                    display_subjects({subject: subjects[subject]}, "")
                    try:
                        activity_number = input("Enter the activity number to remove (or type 'back' to return): ")
                        if activity_number.lower() == "back":
                            break
                        activity_number = int(activity_number) - 1
                        if 0 <= activity_number < len(subjects[subject]):
                            removed_activity = subjects[subject].pop(activity_number)
                            print(f"Activity '{removed_activity[0]}' removed from {subject}.")
                            break
                        else:
                            print("Invalid activity number.")
                    except ValueError:
                        print("Please enter a valid number.")
                else:
                    print(f"No activities found for '{subject}'.")

        elif choice == "5":  # Mark an activity as done
            while True:
                print("\nAvailable Subjects:")
                for idx, subject in enumerate(subjects.keys(), 1):
                    print(f"  {idx}. {subject}")
                subject = input("Enter the subject name (or type 'back' to return): ").strip()
                if subject.lower() == "back":
                    break
                if subject in subjects and subjects[subject]:
                    display_subjects({subject: subjects[subject]}, "")
                    try:
                        activity_number = input("Enter the activity number to mark as done (or type 'back' to return): ")
                        if activity_number.lower() == "back":
                            break
                        activity_number = int(activity_number) - 1
                        if 0 <= activity_number < len(subjects[subject]):
                            subjects[subject][activity_number][1] = True
                            print("Activity marked as done.")
                            break
                        else:
                            print("Invalid activity number.")
                    except ValueError:
                        print("Please enter a valid number.")
                else:
                    print(f"No activities found for '{subject}'.")

        elif choice == "6":  # Back to main menu
            break
        else:
            print("Invalid choice. Please try again.")
        
        # Save changes to file after every modification
        save_subjects(subjects, filename)

# Main function
def main():
    print("Welcome to the Student Task Manager!")
    user_name = input("Enter your name: ").strip()

    # File to store subjects and their activities
    filename = "store.txt"

    # Load existing subjects and activities from file
    subjects = load_subjects(filename)

    while True:
        print(f"\nHello, {user_name}! What would you like to do?")
        print("1. View all subjects and activities")
        print("2. Manage subjects and activities")
        print("3. Clear all data")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":  # View all subjects and activities
            display_subjects(subjects, user_name)
        elif choice == "2":  # Manage subjects and activities
            manage_subjects(subjects, filename)
        elif choice == "3":  # Clear all data
            confirm = input("Are you sure you want to clear all data? (yes/no): ").strip().lower()
            if confirm == "yes":
                subjects.clear()
                save_subjects(subjects, filename)  # Ensure file is also cleared
                print("All data cleared.")
            else:
                print("Operation canceled.")
        elif choice == "4":  # Exit
            print(f"Goodbye, {user_name}!")
            save_subjects(subjects, filename)  # Save before exiting
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
