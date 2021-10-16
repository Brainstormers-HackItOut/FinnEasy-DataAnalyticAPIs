from PIL import Image as im
import cv2
import pytesseract
import numpy as np
from scipy.ndimage import interpolation as inter

def correct_skew(image, delta=1, limit=5):
  def determine_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    histogram = np.sum(data, axis=1)
    score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
    return histogram, score

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

  scores = []
  angles = np.arange(-limit, limit + delta, delta)

  for angle in angles:
    histogram, score = determine_score(thresh, angle)
    scores.append(score)

  best_angle = angles[scores.index(max(scores))]

  (h, w) = image.shape[:2]
  center = (w // 2, h // 2)
  M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
  rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
              borderMode=cv2.BORDER_REPLICATE)

  return best_angle, rotated


def ocr_extraction(image):
    img = im.open(image.file)
    img.thumbnail(size=(2048,2048))
    img_raw = img
    
    raw_image = np.array(img)
    raw_image = raw_image[:, :, ::-1].copy()

    angle, skew_image = correct_skew(raw_image)
    skew_image_raw = skew_image

    orig_image = np.array(img_raw)
    orig_image = orig_image[:,:,::-1].copy()
    orig_image_raw = orig_image

    extracted_info_from_skew = pytesseract.image_to_string(cv2.medianBlur(skew_image_raw,3))

    extracted_info_from_orig = pytesseract.image_to_string(cv2.medianBlur(orig_image_raw,1))
    
    extracted_info = extracted_info_from_skew + " string_separation_between_two_extraction " + extracted_info_from_orig
    #print(extracted_info)

    return extracted_info

def aadhar_card_info(aadhar_card):
    info = ocr_extraction(aadhar_card)
    n = len(info)
    aadhar_len = 12 + 2
    aadhaar = 0
    start = -1
    for i in range(n - aadhar_len):
        current = 0
        for j in range(aadhar_len):
            char = info[i + j]
            if j == 4 and char >= ' ':
                current += 1
            elif j == 9 and char >= ' ':
                current += 1
            elif j != 4 and j != 9 and char.isdigit():
                current += 1
        if i > 0 and (info[i - 1] == ' ' or info[i - 1] == '\n'):
            current += 1
        elif not i:
            current += 1
        if i + aadhar_len < n and info[i + aadhar_len] == ' ' or info[i + aadhar_len] == '\n':
            current += 1
        elif i == n-aadhar_len:
            current += 1
        if current >= 14:
            aadhaar = 1
            start = i
            break
    if aadhaar:
        aadhar_number = ''.join(info[start : start+aadhar_len].split())
        return aadhar_number
    return "Not found!"