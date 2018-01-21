# Section 3, Lecture 22

MostPopularSuperhero.py:19
- mapper_count_friends_per_line(self, _, line):  
  could unpack with python 3 unpacking and change from:
  ```
    fields = line.split()
    heroID = fields[0]
    numFriends = len(fields) - 1
    yield int(heroID), int(numFriends)
  ```
  To a more compact and easier to read (no -1 anywhere):
  ```
    (id, *friends) = line.split()
    yield int(heroID), len(friends)
  ```


# PyCharm note:

For PyCharm users, like me, if you run the codes inside PyCharm, you can set the run configuration to "[ ] Single Instance Only", on the right of the run configuration "Name".

