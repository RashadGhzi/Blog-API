# dic = {
#     "name": "Huy",
#     "role": "Waiter",
#     "hours": 12,
#     "salary per hour ($)": 0.8, }

# #? updating dic attribute name
# setattr(dic, "name", "Bro") 
# print(dic)


import os
 
dir = os.path.dirname("uploads")
print("dir", os.getcwd())
current_dir = os.getcwd()
file_path = os.path.join(current_dir, "nothing.txt")
os.remove(file_path)