from PIL import Image
import pytesseract
import cv2
import os
import re
import glob

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
re13 = '[\d]{1,2}.[\d]{1,2}.[\d]{4}'
re14 = '(\d{2}-\d{2}-\d{2})'
re15 = '(\d{2}/[\d]{2}/[\d]{2})'

dateRegex = re.compile("(r%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s)" % (re1, re2, re3, re4, re5, re8, re6, re7, re9, re10, re11,re12,re13,re14,re15))

successList = []
failureList = []

file_names = os.listdir('/home/kamal/practiceML/practiceML/Receipts/')
# images = [file_name for file_name in file_names]
# print(images)
try:
    for file_name in file_names:
        # construct the argument parse and parse the arguments
        # image contains the path to the image from home but if the image in same directory
        # then write only file name.
        args = {
            "image": "Receipts/" + str(file_name),
            "preprocess": "thresh"
        }

        # load the example image and convert it to grayscale
        print(args["image"])
        print(args["preprocess"])
        image = cv2.imread(args["image"])
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # check to see if we should apply thresholding to preprocess the image
        if args["preprocess"] == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # make a check to see if median blurring should be done to remove noise
        elif args["preprocess"] == 'adaptive':
            gray = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # write the grayscale image to disk as a temporary file so we can apply OCR to it
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        # load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        print(text)
        stat_file = open('receipts text.txt', 'w')
        stat_file.write((text).encode('utf-8').strip())


        dateString = dateRegex.findall((text).encode('utf-8').strip())
        print("Matched Regex:::::::::")
        # print(dateString)
        if dateString:
            try:
                if dateString:
                    print(dateString)
                    successList.append({
                        "file_name": file_name,
                        "date_fetched": str(dateString)
                    })
            except Exception as ex:
                failureList.append({
                    "file_name": file_name,
                    "message": str(ex)
                })
        else:
            failureList.append({
                "file_name": file_name,
                "message": "No string found."
            })
except Exception as ex:
    print("Exception occured, error msg: " + str(ex))
finally:
    print("\n\nSuccess List " + str(successList))
    print("\n\nFailur List " + str(failureList))
    print("\n\nSuccess List count " + str(len(successList)))
    print("\n\nFailur List count " + str(len(failureList)))
    print("\n\nTask Completed....")


# # show the output images
# #cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)

