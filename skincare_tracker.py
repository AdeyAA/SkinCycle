from skincare import SkinCare
def main():
  print(f"Running Skincare Tracker!")
  skincare_file_path = "skincare.csv"
  #Get user to input skincare product.
  skincare_info = get_user_skincare_info()
  #Write product to a file.
  save_skincare_to_file(skincare_info, skincare_file_path)
  #Read file and summarize.
  summarize_skinare(skincare_file_path)

 

def get_user_skincare_info():
  skincare_name = input("Enter skincare product: ")
  time_of_day_selection = [
    " Morning Routine", " NightTime Routine"
  ]
  skincare_category = [
    " Cleanser", " Toner", " Serum", " Treatment", " Exfoliator", " Moisturizer", " Sunscreen",
  ]

  while True:
    print("Select a Routine: ")
    for i, routine_name in enumerate(time_of_day_selection):
      print(f"{i + 1}. {routine_name}")
    
    selected_routine = int(input("Enter a routine number [1-2]: ")) - 1

    if selected_routine in range(len(time_of_day_selection)):
      selected_day = time_of_day_selection[selected_routine]
      break
    else:
      print("Invalid routine. Please try again!")

  
    
  while True:
    print("Select a category: ")
    for i, category_name in enumerate(skincare_category):
      print(f"{i + 1}. {category_name}")
    
    value_range = f"[1 - {len(skincare_category)}]"
    selected_category = int(input(f"Enter a category number {value_range}: ")) - 1

    if selected_category in range(len(skincare_category)):
      selected = skincare_category[selected_category]
      new_skincare_info = SkinCare(name=skincare_name, time_of_day=selected_day,category=selected)

      return new_skincare_info
    else:
      print("Invalid category. Please try again!")
  
  


def save_skincare_to_file(skincare_info,skincare_file_path):
  print(f"Saving User Skincare: {skincare_info} to {skincare_file_path}")
  with open(skincare_file_path, "a") as f:
    f.write(f"{skincare_info.name},{skincare_info.time_of_day},{skincare_info.category}\n")

def summarize_skinare(skincare_file_path):
  print(f"Summarizing User Skincare")
  skincare = []
  with open(skincare_file_path, "r") as f:

    lines = f.readlines()
    for line in lines:
      skincare_info_name, skincare_info_time_of_day, skincare_info_category = line.strip().split(",")
      line_skincare = SkinCare(name=skincare_info_name,time_of_day=skincare_info_time_of_day,category=skincare_info_category)
      skincare.append(line_skincare)
  
  skincare_by_routine = {}
  for product in skincare:
    key = product.time_of_day
    info_to_include = f"{product.name}: {product.category}"
    if key in skincare_by_routine:
      skincare_by_routine[key].append(info_to_include)
    else:
      skincare_by_routine[key] = [info_to_include]
  print("Skincare by Routine: ")
  for key, info_to_include in skincare_by_routine.items():
    print(f"-{key}:")
    for info in info_to_include:
      print(f"{info}")


  





if __name__ == "__main__":
  main()