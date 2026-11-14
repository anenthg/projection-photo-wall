/* Your wall. Edit the JSON below (keep it strict JSON: double quotes, no trailing commas, no comments inside;
   tools/prepare-album.py reads it too). See docs/configuration.md.

   title      shown in the desktop editor and the browser tab
   wallPhoto  optional photo of the wall, for the desktop mock-up: {"src": "wall.jpg", "width": W, "height": H}
              (put the file in site/; width/height are its pixel size)
   frames     one entry per frame:
                name   anything that helps you recognise it ("Left tall frame")
                size   optional label ("8x10 frame")
                ratio  width / height of the visible picture area (portrait < 1, landscape > 1);
                       optional when quad is given
                quad   optional: the 4 inner corners on the wall photo, normalised 0-1, in the order
                       top-left, top-right, bottom-right, bottom-left (tools/mark-frames.html writes these)
   route      optional: the order (0-based frame numbers) travelling scenes visit the frames;
              default = a loop around the middle of the wall

   This example is 6 frames without a wall photo: the page lays them out in a grid, and you then align each one
   on the real wall with the projector (docs/alignment.md). */
window.WALL_CONFIG =
{
  "title": "Photo Wall",
  "wallPhoto": null,
  "frames": [
    { "name": "Left tall", "size": "8x10 frame", "ratio": 0.8 },
    { "name": "Top middle", "size": "6x4 frame", "ratio": 1.5 },
    { "name": "Right tall", "size": "8x10 frame", "ratio": 0.8 },
    { "name": "Bottom left", "size": "6x6 frame", "ratio": 1.0 },
    { "name": "Bottom middle", "size": "6x4 frame", "ratio": 1.5 },
    { "name": "Bottom right", "size": "5x8 frame", "ratio": 0.62 }
  ],
  "route": null
};
