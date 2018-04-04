import convert
import ocr

def getText():
    docType=input("1. Aadhaar Card\n2. PAN Card\nEnter Document Type: ")
    filename = input("File Name: ")
    if docType == "1":
        aadhaar=convert.convert(filename)
        return {'file': filename, 'aadhaar': aadhaar[0], 'name': aadhaar[1], 'address': aadhaar[2]}
    elif docType=="2":
        name, f_name, dob, pan = ocr.get_pan(filename)
        return {'file': filename, 'pan': pan, 'name': name, 'f_name': f_name, 'dob':dob}
    else:
        print("Wrong Option! Try again.")

if __name__ == '__main__':
    result = getText()
    print(result)