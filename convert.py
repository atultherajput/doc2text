''' Important classes to remember
PDFParser - fetches data from pdf file
PDFDocument - stores data parsed by PDFParser
PDFPageInterpreter - processes page contents from PDFDocument
PDFDevice - translates processed information from PDFPageInterpreter to whatever you need
PDFResourceManager - Stores shared resources such as fonts or images used by both PDFPageInterpreter and PDFDevice
LAParams - A layout analyzer returns a LTPage object for each page in the PDF document
PDFPageAggregator - Extract the decive to page aggregator to get LT object elements
'''

import os
import re
import extract
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

''' This is what we are trying to do:
1) Transfer information from PDF file to PDF document object. This is done using parser
2) Open the PDF file
3) Parse the file using PDFParser object
4) Assign the parsed content to PDFDocument object
5) Now the information in this PDFDocumet object has to be processed. For this we need
   PDFPageInterpreter, PDFDevice and PDFResourceManager
 6) Finally process the file page by page 
'''

def convert(filename):
	my_file = filename
	log_file = filename+".txt"

	password = ""
	extracted_text = ""

	# Open and read the pdf file in binary mode
	fp = open(my_file, "rb")

	# Create parser object to parse the pdf content
	parser = PDFParser(fp)

	# Store the parsed content in PDFDocument object
	document = PDFDocument(parser, password)

	# Check if document is extractable, if not abort
	if not document.is_extractable:
		raise PDFTextExtractionNotAllowed

	# Create PDFResourceManager object that stores shared resources such as fonts or images
	rsrcmgr = PDFResourceManager()

	# set parameters for analysis
	laparams = LAParams()

	# Create a PDFDevice object which translates interpreted information into desired format
	# Device needs to be connected to resource manager to store shared resources
	# device = PDFDevice(rsrcmgr)
	# Extract the decive to page aggregator to get LT object elements
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)

	# Create interpreter object to process page content from PDFDocument
	# Interpreter needs to be connected to resource manager for shared resources and device
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	# Ok now that we have everything to process a pdf document, lets process it page by page
	for page in PDFPage.create_pages(document):
		# As the interpreter processes the page stored in PDFDocument object
		interpreter.process_page(page)
		# The device renders the layout from interpreter
		layout = device.get_result()
		# Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
		for lt_obj in layout:
			if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
				extracted_text += lt_obj.get_text()

	#close the pdf file
	fp.close()
	data=process_aadhaar(extracted_text, log_file)
	return data


def process_aadhaar(extracted_text, log_file):
	# print (extracted_text.encode("utf-8"))
	extracted_text = re.sub(r'[^\x00-\x7F]+', ' ', extracted_text)
	extracted_text = re.sub('\(.*?\)', '', extracted_text)
	extracted_text = re.sub('\s{2,}', ' ', extracted_text)
	with open(log_file, "wb") as my_log:
		my_log.write(extracted_text.encode("utf-8"))
	fr = open(log_file, 'r')
	i = 0
	data = []
	info=[]
	for line in fr:
		i += 1
		if i >= 16 and i <= 20:
			data.append(line)
	info.append(extract.get_aadhaar(data))
	info.append(extract.get_name(data))
	info.append(extract.get_address(data))
	return info
