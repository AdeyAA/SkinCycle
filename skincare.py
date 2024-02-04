class SkinCare:
  def __init__(self, name, time_of_day, category):
    self.name = name
    self.time_of_day = time_of_day
    self.category = category

  def __repr__(self):
    return f"<Skincare: {self.name}, {self.time_of_day}, {self.category}>"
