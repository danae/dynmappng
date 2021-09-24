import functools


# Class that defines coordinates
@functools.total_ordering
class Coords:
  # Constructor
  def __init__(self, x, y):
    self.x = x
    self.y = y

  # Return if the coordinates are equal to other coordinates
  def __eq__(self, other):
    return isinstance(other, Coords) and (self.x, self.y) == (other.x, other.y)

  # Return if the coordinates are less than other coordinates
  def __lt__(self, other):
    if not isinstance(other, Coords):
      return NotImplemented
    elif self.y < other.y:
      return True
    elif self.x < other.x:
      return True
    else:
      return False

  # Return the identity of the coordinates
  def __pos__(self):
    return Coords(self.x, self.y)

  # Return the negation of the coordinates
  def __neg__(self):
    return Coords(-self.x, -self.y)

  # Return the absolute value of the coordinates
  def __abs__(self):
    return Coords(abs(self.x), abs(self.y))

  # Return the addition of two coordinates
  def __add__(self, other):
    if isinstance(other, Coords):
      return Coords(self.x + other.x, self.y + other.y)
    else:
      return NotImplemented

  # Return the subtraction of two coordinates
  def __sub__(self, other):
    if isinstance(other, Coords):
      return Coords(self.x - other.x, self.y - other.y)
    else:
      return NotImplemented

  # Return the multiplication of coordinates with other coordinates or a scalar
  def __mul__(self, other):
    if isinstance(other, Coords):
      return Coords(self.x * other.x, self.y * other.y)
    elif isinstance(other, (int, float)):
      return Coords(self.x * other, self.y * other)
    else:
      return NotImplemented

  # Return the division of coordinates with other coordinates or a scalar
  def __truediv__(self, other):
    if isinstance(other, Coords):
      return Coords(self.x / other.x, self.y / other.y)
    elif isinstance(other, (int, float)):
      return Coords(self.x / other, self.y / other)
    else:
      return NotImplemented

  # Return the internal representation of the coordinates
  def __repr__(self):
    return f'{self.__class__.__name__()}({self.x}, {self.y})'

  # Return the string representation of the coordinates
  def __str__(self):
    return f'({self.x}, {self.y})'

  # Iterate over a range of coordinates
  @classmethod
  def range(cls, min_x, min_y, max_x = None, max_y = None, step_x = 1, step_y = 1):
    if max_x is None:
      max_x = min_x
      min_x = 0
    if max_y is None:
      max_y = min_y
      min_y = 0

    for y in range(min_y, max_y, step_y):
      for x in range(min_x, max_y, step_x):
        yield cls(x, y)
