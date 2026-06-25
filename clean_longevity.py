"""
Process longevity images:
- Remove participant name labels from laptop/zoom images
- Smart-crop blue cells image to both target sizes
- Output high-res JPEGs at exact dimensions
"""
import cv2
import numpy as np
import os

SRC = "/home/user/workspace/uploaded_attachments/799f6be4884a4ffc851a278405395372"
OUT = "/home/user/workspace/eteacher-images/output/longevity"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# LAPTOP "FINAL_8K_921x945" — 921x945 — Zoom grid with name pills
# ============================================================
img = cv2.imread(f"{SRC}/FINAL_8K_921x945.jpg")
H, W = img.shape[:2]
print(f"FINAL_8K: {W}x{H}")

# The 6 Zoom tiles. Name labels are dark rounded pills in bottom-left of each tile.
# Tiles are roughly:  cols at x≈58, 268 (mid), 478;  3 rows at y≈250, 380, 510 (ish)
# Pill regions visible in screenshot:
#   David Miller:      x 40-110,   y 340-360
#   Sarah Johnson:     x 295-380,  y 340-360
#   Michael Brown:     x 40-115,   y 470-495
#   Jennifer Davis:    x 295-385,  y 470-495
#   Emily Wilson:      x 40-105,   y 595-620
#   James Anderson:    x 295-390,  y 595-620
# These coords are based on a 921x945 image where the laptop screen occupies roughly x=45-650, y=215-625

mask = np.zeros((H, W), dtype=np.uint8)
pills = [
    (38, 340, 118, 365),    # David Miller
    (293, 340, 388, 365),   # Sarah Johnson
    (38, 472, 122, 497),    # Michael Brown
    (293, 472, 388, 497),   # Jennifer Davis
    (38, 600, 118, 624),    # Emily Wilson
    (293, 600, 395, 624),   # James Anderson
]
for x1, y1, x2, y2 in pills:
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
cleaned = cv2.inpaint(img, mask, inpaintRadius=6, flags=cv2.INPAINT_TELEA)
cv2.imwrite("/tmp/laptop_final_clean.jpg", cleaned, [cv2.IMWRITE_JPEG_QUALITY, 96])

# ============================================================
# LAPTOP "hf_20260623" — 1080x1080 - Zoom grid (different dim)
# ============================================================
img = cv2.imread(f"{SRC}/hf_20260623_082621_4d6198e1-65bc-427b-ae92-ba3aabdce7f1.jpg")
H, W = img.shape[:2]
print(f"hf laptop: {W}x{H}")

# Scale pills based on this larger image — screen area: x=85-680, y=255-680
# Each pill is in bottom-left corner of each Zoom tile
mask = np.zeros((H, W), dtype=np.uint8)
pills = [
    (78, 386, 168, 412),    # David Miller
    (335, 386, 425, 412),   # Sarah Johnson
    (78, 526, 168, 552),    # Michael Brown
    (335, 526, 425, 552),   # Jennifer Davis
    (78, 666, 168, 692),    # Emily Wilson
    (335, 666, 435, 692),   # James Anderson
]
for x1, y1, x2, y2 in pills:
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
cleaned = cv2.inpaint(img, mask, inpaintRadius=6, flags=cv2.INPAINT_TELEA)
cv2.imwrite("/tmp/laptop_hf_clean.jpg", cleaned, [cv2.IMWRITE_JPEG_QUALITY, 96])

# ============================================================
# LAPTOP "use-this-image-for-gabi44" — 921x945 same coords
# ============================================================
img = cv2.imread(f"{SRC}/use-this-image-for-gabi44.jpg")
H, W = img.shape[:2]
print(f"gabi44 laptop: {W}x{H}")
mask = np.zeros((H, W), dtype=np.uint8)
# Names appear in WHITE not in pills — these need bigger inpaint
# Names sit roughly bottom-left of each tile, white text:
# David Miller, Sarah Johnson row at y≈340
# Michael Brown, Jennifer Davis row at y≈470
# Emily Wilson, James Anderson row at y≈600
pills = [
    (38, 332, 168, 362),    # David Miller
    (293, 332, 410, 362),   # Sarah Johnson
    (38, 462, 168, 492),    # Michael Brown
    (293, 462, 405, 492),   # Jennifer Davis
    (38, 590, 158, 620),    # Emily Wilson
    (293, 590, 425, 620),   # James Anderson
]
for x1, y1, x2, y2 in pills:
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
cleaned = cv2.inpaint(img, mask, inpaintRadius=6, flags=cv2.INPAINT_TELEA)
cv2.imwrite("/tmp/laptop_gabi_clean.jpg", cleaned, [cv2.IMWRITE_JPEG_QUALITY, 96])

print("All cleaned. Use ImageMagick for final sizing.")
