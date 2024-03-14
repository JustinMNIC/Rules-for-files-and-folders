import random 
import os


def create_random_dirs_and_files(target_dir_for_test):
    for i in range(100):
        random_choice = random.choice(["file", "dir"])
        if random_choice == "file":
            file_name = "file" + str(i) + random.choice([".txt",".pdf", ".py", ".js", ".html", ".jpg", ".img"])
            with open(os.path.join(target_dir_for_test, file_name), "w") as f:
                f.write("This is a test file")

        else:
            dir_name = "dir" + str(i)
            os.mkdir(os.path.join(target_dir_for_test, dir_name))
            for j in range(5):
                file_name = "file" + str(j) + random.choice([".txt",".pdf", ".py", ".js", ".html", ".jpg", ".img"])
                with open(os.path.join(target_dir_for_test, dir_name, file_name), "w") as f:
                    f.write("This is a test file")
                    
create_random_dirs_and_files(r"C:\Users\iusti\Desktop\tests")