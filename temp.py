import os

for folder in os.listdir("output_0"):
    for dirr in os.listdir(os.path.join("output_0",folder)):
        print(f"folder: {os.path.join('output_0', folder, dirr)}")
        for file in os.listdir(os.path.join("output_0",folder, dirr)):
            file_path = os.path.join('output_0', folder, dirr, file)
            print(f"file: {file_path}")
            os.path.join(os.getcwd(), "output_1", folder, dirr)
            if folder == "cursive" and len(os.listdir(os.path.join("output_0",folder, dirr))) == 4000:
                break
            elif folder != "cursive" and len(os.listdir(os.path.join("output_0",folder, dirr))) == 2000:
                break
            if not os.path.exists(os.path.join(os.getcwd(), "output_1", folder, dirr)):
                os.makedirs(os.path.join(os.getcwd(), "output_1", folder, dirr))
            os.rename(file_path, os.path.join(os.getcwd(), "output_1", folder, dirr, file))