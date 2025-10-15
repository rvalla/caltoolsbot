import random as rd

class Util():
  "Some useful functions."

  #Rolling a dice...
  def dice(self, size, faces):
    s = []
    for n in range(size):
      s.append(rd.randint(1,abs(faces)))
    return s

  #The minor of two dice...
  def minor_of_a_pair(self, size, faces):
    s = []
    for n in range(size):
      s.append(self.get_minor_dice(faces))
    return s

  def get_minor_dice(self, faces):
    a = rd.randint(1,abs(faces))
    b = rd.randint(1,abs(faces))
    if b < a:
      a = b
    return a

  #The sum of several dice...
  def sum_of_dice(self, size, faces, n_dice):
    s = []
    for n in range(size):
      s.append(self.get_added_up_dice(faces, n_dice))
    return s

  def get_added_up_dice(self, faces, n_dice):
    a = 0
    for d in range(n_dice):
      a += rd.randint(1,abs(faces))
    return a
  
  #Returning a string shuffled...
  def shuffle_string(self, message):
    words = message.split(" ")
    rd.shuffle(words)
    m = ""
    for w in words:
      m += w
      m += " "
    return m[:-1]

  #Building a random list from list...
  def controlled_random(self, size, list):
    m = ""
    for w in range(size):
      m += rd.choice(list)
      m += " "
    return m[:-1]
    
  #Printing Util()...
  def __str__(self):
    return "- musiCal Bot\n" + \
            "  I am the class full of useful functions...\n" + \
            "  gitlab.com/musicaltools/caltoolsbot\n" + \
            "  rodrigovalla@protonmail.ch"
