import argparse
import exrex
from PyPDF2 import PdfFileReader
from os import path

parser = argparse.ArgumentParser( description = "Brute-force pdf decryptor." )
parser.add_argument("-f, --file, ", dest="file_loc",
                                    action="store",
                                    help="PDF file location" )
parser.add_argument("-r, --regexp", dest="language",
                                    action="store",
                                    help="Regular expression that generates the language used for brute forcing the PDF password.")
parser.add_argument("-s, --silent", dest="is_silent",
                                    action="store_true",
                                    help="If set the only output will be the found password or exists with 1 if not found")

args = parser.parse_args()

if args.file_loc:
    pdf_file_loc = args.file_loc
else:
    pdf_file_loc = input( "File name:" )

if args.language:
    language = args.language
else:
    language = input( "Regexp: " )

is_silent = args.is_silent

if path.exists( pdf_file_loc ):
    pdf_file = PdfFileReader( pdf_file_loc )
else:
    if not is_silent:
        print( f'Cannot find PDF file at location {pdf_file_loc}' )
    exit( 1 )

password = ""

if pdf_file.isEncrypted:
    for word in exrex.generate( language ):
        r = pdf_file.decrypt( word )
        if not is_silent:
            print( f'Trying {word}: {r}' )
        if r == 1:
            password = word
            if is_silent:
                print( word )
            else:
                print( f'Password found: {word}' )
            break
else:
    print( "PDF file is not encrypted." )

if not password:
    if is_silent:
        exit( 1 )
    else:
        print( "Password not found..." )
        exit( 1 )