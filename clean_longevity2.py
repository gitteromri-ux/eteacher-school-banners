"""Second pass: fix remaining name labels with better coords + bigger masks."""
import cv2
import numpy as np

SRC = "/home/user/workspace/uploaded_attachments/799f6be4884a4ffc851a278405395372"

# === FINAL_8K (921x945) — fix bottom-row names + any remaining artifacts ===
img = cv2.imread(f"{SRC}/FINAL_8K_921x945.jpg")
H, W = img.shape[:2]
mask = np.zeros((H, W), dtype=np.uint8)
# Cover ALL 6 name positions with bigger boxes to catch anti-aliasing & missed labels
pills = [
    (35, 332, 125, 372),    # David Miller
    (290, 332, 395, 372),   # Sarah Johnson
    (35, 462, 130, 502),    # Michael Brown
    (290, 462, 395, 502),   # Jennifer Davis
    (33, 590, 122, 632),    # Emily Wilson (bottom-left tile)
    (290, 590, 405, 632),   # James Anderson (bottom-right tile)
]
for x1, y1, x2, y2 in pills:
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
cleaned = cv2.inpaint(img, mask, inpaintRadius=10, flags=cv2.INPAINT_TELEA)
cleaned = cv2.inpaint(cleaned, mask, inpaintRadius=8, flags=cv2.INPAINT_NS)
cv2.imwrite("/tmp/laptop_final_clean.jpg", cleaned, [cv2.IMWRITE_JPEG_QUALITY, 96])

# === hf 1080x1080 — scale coords ===
img = cv2.imread(f"{SRC}/hf_20260623_082621_4d6198e1-65bc-427b-ae92-ba3aabdce7f1.jpg")
H, W = img.shape[:2]
mask = np.zeros((H, W), dtype=np.uint8)
# In 1080x1080 the screen area is approximately x=80-690, y=255-680 (6 tiles)
pills = [
    (75, 380, 175, 415),    # David Miller
    (330, 380, 435, 415),   # Sarah Johnson
    (75, 520, 175, 555),    # Michael Brown
    (330, 520, 440, 555),   # Jennifer Davis
    (75, 660, 175, 695),    # Emily Wilson
    (330, 660, 445, 695),   # James Anderson
]
for x1, y1, x2, y2 in pills:
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
cleaned = cv2.inpaint(img, mask, inpaintRadius=10, flags=cv2.INPAINT_TELEA)
cleaned = cv2.inpaint(cleaned, mask, inpaintRadius=8, flags=cv2.INPAINT_NS)
cv2.imwrite("/tmp/laptop_hf_clean.jpg", cleaned, [cv2.IMWRITE_JPEG_QUALITY, 96])

# === gabi44 (921x945) — white text variant ===
img = cv2.imread(f"{SRC}/use-this-image-for-gabi44.jpg")
H, W = img.shape[:2]
mask = np.zeros((H, W), dtype=np.uint8)
# White text labels are bigger/wider — expand boxes
pills = [
    (30, 322, 180, 372),    # David Miller
    (285, 322, 425, 372),   # Sarah Johnson
    (30, 452, 180, 502),    # Michael Brown
    (285, 452, 415, 502),   # Jennifer Davis
    (30, 582, 175, 632),    # Emily Wilson
    (285, 582, 435, 632),   # James Anderson
]
for x1, y1, x2, y2 in pills:
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
cleaned = cv2.inpaint(img, mask, inpaintRadius=10, flags=cv2.INPAINT_TELEA)
cleaned = cv2.inpaint(cleaned, mask, inpaintRadius=8, flags=cv2.INPAINT_NS)
cv2.imwrite("/tmp/laptop_gabi_clean.jpg", cleaned, [cv2.IMWRITE_JPEG_QUALITY, 96])

print("Pass 2 complete")
