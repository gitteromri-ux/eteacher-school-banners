"""
Inpaint text overlays out of the FA banner frame using OpenCV's
content-aware inpainting (Telea algorithm). Then produce final sized assets.
"""
import cv2
import numpy as np
import os

SRC = "/tmp/fa_end.jpg"  # 1080x1080 best-composition frame
img = cv2.imread(SRC)
H, W = img.shape[:2]
print(f"Source: {W}x{H}")

# Build a mask covering all the text regions in the 1080x1080 frame.
# Coordinates measured visually:
#   @livefrenchatelier · Instagram & Meta  →  y 30-78,  x 260-810
#   FRENCH ATELIER PRESENTS                →  y 560-595, x 280-790
#   Win a Free Flight                      →  y 610-700, x 220-880
#   to Paris                               →  y 700-790, x 340-740
#   for Bastille Day 2026                  →  y 790-845, x 280-810
#   Share with 10+ friends · 3 winners…    →  y 855-905, x 200-870
#   ENTER NOW — LINK IN BIO (yellow pill)  →  y 925-1020, x 270-810

mask = np.zeros((H, W), dtype=np.uint8)
rects = [
    (255, 25, 815, 82),     # @livefrenchatelier
    (275, 555, 795, 600),   # FRENCH ATELIER PRESENTS
    (215, 605, 885, 705),   # Win a Free Flight (line 1)
    (335, 700, 745, 795),   # to Paris (line 2)
    (275, 785, 815, 850),   # for Bastille Day 2026
    (195, 850, 875, 910),   # Share with…
    (260, 920, 815, 1025),  # yellow CTA pill
]
for x1, y1, x2, y2 in rects:
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

# Dilate the mask a bit so we capture anti-aliased edges
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)

# Inpaint using Telea — fast & good for thin/medium text on smooth backgrounds
cleaned = cv2.inpaint(img, mask, inpaintRadius=8, flags=cv2.INPAINT_TELEA)
# Run Navier-Stokes pass on top for the larger blocks (sky / road)
cleaned = cv2.inpaint(cleaned, mask, inpaintRadius=12, flags=cv2.INPAINT_NS)

cv2.imwrite("/tmp/fa_cleaned.jpg", cleaned, [cv2.IMWRITE_JPEG_QUALITY, 96])
print("Wrote /tmp/fa_cleaned.jpg")
