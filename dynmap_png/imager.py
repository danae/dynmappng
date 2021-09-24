import os
import progressbar
import re

from PIL import Image

from .coords import Coords


# Constant that holds the tiles per chunk
TILES_PER_CHUNK = 32

# Class that defines a tile
class Tile:
  # Constructor
  def __init__(self, chunk_coords, tile_coords, zoom_level):
    if zoom_level < 0 or zoom_level > 5:
      raise ValueError("zoom_level must be between 0 and 5")

    self.chunk_coords = chunk_coords
    self.tile_coords = tile_coords
    self.zoom_level = zoom_level

  # Return the path of the tile
  def path(self, extension = "png"):
    # Determine the chunk path
    chunk_path = f'{self.chunk_coords.x}_{self.chunk_coords.y}'

    # Determine the tile path
    tile_prefix = 'z' * self.zoom_level
    tile_prefix = tile_prefix + ('_' if tile_prefix else '')
    tile_coords = self.chunk_coords * TILES_PER_CHUNK + self.tile_coords * 2 ** self.zoom_level
    tile_path = f"{tile_prefix}{tile_coords.x}_{tile_coords.y}.{extension}"

    # Return the path
    return os.path.join(chunk_path, tile_path)

  # Return the string representation of the tile
  def __str__(self):
    return self.path()


# Class that defines a chunk
class Chunk:
  # Constructor
  def __init__(self, chunk_coords, zoom_level):
    if zoom_level < 0 or zoom_level > 5:
      raise ValueError("zoom_level must be between 0 and 5")

    self.chunk_coords = chunk_coords
    self.zoom_level = zoom_level

  # Return the amount of tiles in one dimension in the chunk
  def size(self):
    return TILES_PER_CHUNK // 2 ** self.zoom_level

  # Return the amount of tiles in the chunk
  def __len__(self):
    return self.size() ** 2

  # Iterate over the tiles in the array
  def __iter__(self):
    for tile_coords in Coords.range(self.size(), self.size()):
      yield Tile(self.chunk_coords, tile_coords, self.zoom_level)



# Class that defines the imager functionality
class Imager:
  # Constructor
  def __init__(self, path, zoom_level, tile_size = 128):
    self.path = path
    self.zoom_level = zoom_level
    self.tile_size = tile_size

  # Create an image from a single chunk
  def create_image_chunk(self, x, y):
    # Create a chunk
    chunk = Chunk(Coords(x, y), self.zoom_level)

    # Create an image
    image = Image.new('RGB', (chunk.size() * self.tile_size, chunk.size() * self.tile_size))

    # Iterate over the tiles
    widgets = [f'Processing chunk {chunk.chunk_coords}', progressbar.Bar(marker = '█', left = ' |', right = '| '), progressbar.Percentage()]
    bar = progressbar.ProgressBar(max_value = len(chunk), widgets = widgets)
    bar.start()

    for i, tile in enumerate(chunk):
      bar.update(i)

      # Open the tile image
      tilePath = tile.path()
      try:
        tileImagePath = os.path.join(self.path, tilePath)
        tileImage = Image.open(tileImagePath)
      except OSError as ex:
        continue

      # Calculate the image coordinates
      image_coords = Coords(tile.tile_coords.x, chunk.size() - (tile.tile_coords.y + 1)) * self.tile_size

      # Place the tile image on the image
      image.paste(tileImage, (image_coords.x, image_coords.y))

    bar.finish()

    # Return the image
    return image

  # Save an image of a single chunk
  def save_image_chunk(self, x, y, output_path = None):
    # Determine the output path and create it if it doesn't exist
    output_path = output_path or os.getcwd()
    if not os.path.isdir(output_path):
      os.makedirs(output_path)

   # Determine the output file
    output_file = os.path.join(output_path, f"{x}_{y}.png")

    # Create and save the image
    image = self.create_image_chunk(x, y)
    image.save(output_file)

  # Get all chunks in the path
  def get_chunks(self):
    for path in os.listdir(self.path):
      if match := re.fullmatch('(-?[\d+])_(-?[\d+])', path):
        yield (int(match.group(1)), int(match.group(2)))
