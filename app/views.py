from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from PIL import Image
import pytesseract
import cv2
import os
import re
import glob
from django.conf import settings
import dateutil.parser as dparser
from .forms import *
from django.core.files.storage import default_storage


@csrf_exempt
def health_check_api(request):
    data = {
        "info": "Health checked successfully.",
        "status": True,
        "status_code": 200,
        "success": "SUCCESS",
        "msg": "Health checked successfully."
    }
    return JsonResponse(data)


@csrf_exempt
def image_to_text(request):
    data = {
        "date": None
    }
    try:
        if request.method == 'POST':
            file = request.FILES['image']
            fName = default_storage.save(file.name, file)
            args = {
                "image": fName,
                "preprocess": "thresh"
            }
            print(args["image"])
            print(args["preprocess"])
            image = cv2.imread(args["image"])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            if args["preprocess"] == "thresh":
                gray = cv2.threshold(gray, 0, 255,
                                     cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            elif args["preprocess"] == 'adaptive':
                gray = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

            filename = "{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)
            text = pytesseract.image_to_string(Image.open(filename))
            os.remove(filename)
            re1 = '[\d]{1,2}/[\d]{1,2}/[\d]{4}'
            re2 = '[\d]{1,2}-[\d]{1,2}-[\d]{2}'
            re3 = '[\d]{1,2} [ADFJMNOS]\w* [\d]{4}'
            re4 = '(\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4})'
            re5 = '[\d]{1,2}/[ADFJMNOS]\w*/[\d]{4}'
            re8 = '[\d]{1,2}-[ADFJMNOS]\w*-[\d]{4}'
            re6 = '(\d{1,2}/(?:January|February|March|April|May|June|July|August|September|October|November|December)/[\d]{4})'
            re7 = '(\d{1,2}-(?:January|February|March|April|May|June|July|August|September|October|November|December)-[\d]{4})'
            re9 = '([\d]{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s[\d]{4})'
            re10 = '([\d]{1,2}\s(?:JAN|NOV|OCT|DEC)\s[\d]{4})'
            re11 = '([\d]{2})[/.-]([\d]{2})[/.-]([\d]{4})'
            re12 = '[\d]{1,2}\s[ADFJMNOS]\w*[,][\s][\d]{4}'
            # re13 = '[\d]{1,2}.[\d]{1,2}.[\d]{4}'
            # re14 = '(\d{2}-\d{2}-\d{2})'
            # re15 = '(\d{2}/[\d]{2}/[\d]{2})'

            dateRegex = re.compile("(r%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s)" % (
                re1, re2, re3, re4, re5, re8, re6, re7, re9, re10, re11, re12))
            dateString = dateRegex.search(str(text))
            if dateString:
                try:
                    data['date'] = dparser.parse(
                        str(dateString.group()), fuzzy=True).date()
                except Exception as exc:
                    print("Exception occured while parsing, Error msg: " + str(exc))
        else:
            print("Only POST with form-data allowed.")
    except Exception as exception:
        print("Exception occured while retrive request, Error msg: " + str(exception))
    finally:
        return JsonResponse(data)
