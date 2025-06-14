import os
import shutil
import sys


CATEGORIES = {
    "IMAGES":   [".jpeg", ".jpg", ".png", ".gif", ".svg"],
    "DOCUMENTS":[".pdf", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "AUDIO":    [".mp3", ".wav", ".aac"],
    "VIDEO":    [".mp4", ".mov", ".avi", ".mkv"],
    "ARCHIVES": [".zip", ".rar", ".tar", ".gz"],
}

def organize_directory(path):

    if not os.path.isdir(path):
        print(f"Error: The directory '{path}' was not found.")
        return

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            continue

        file_extension = os.path.splitext(item)[1].lower()

        found_category = None
        for category, extensions in CATEGORIES.items():
            if file_extension in extensions:
                found_category = category
                break 

        if found_category is None:
            found_category = "OTHERS"

        category_path = os.path.join(path, found_category)
        os.makedirs(category_path, exist_ok=True)


        destination_path = os.path.join(category_path, item)
        shutil.move(item_path, destination_path)
        
        print(f"Moved '{item}' to '{found_category}' folder.")

    print("Organization complete!")



if __name__ == "__main__":
    
    if len(sys.argv) < 2 :
        # target_directory = 'E:/sort' 
        target_directory = input("Enter the path: ")
        organize_directory(target_directory)
    else :
        target_directory = sys.argv[1]
        organize_directory(target_directory)