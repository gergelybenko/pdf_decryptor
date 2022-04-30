import argparse
import exrex
from PyPDF2 import PdfFileReader
from os import path

# FIXME: No global variables
g_is_silent = False

def parse_command_line_arguments():
    parser = argparse.ArgumentParser( description = "Brute-force pdf decryptor." )
    parser.add_argument("-f", "--file",     dest="file_loc",
                                            action="store",
                                            help="PDF file location" )
    parser.add_argument("-r", "--regexp",   dest="language",
                                            action="store",
                                            help="Regular expression that generates the language used for brute forcing the PDF password.")
    parser.add_argument("-s", "--silent",   dest="is_silent",
                                            action="store_true",
                                            help="If set the only output will be the found password or exists with 1 if not found")
    return parser.parse_args()

def get_param( p, input_text ):
    if p:
        return p
    else:
        return input( input_text )

def s_print( *args, **kwargs ):
    if not g_is_silent:
        print( *args, **kwargs )

def crack_password( pdf_file, language ):
    for word in exrex.generate( language ):
        r = pdf_file.decrypt( word )
        s_print( f'Trying {word}: {r}' )
        if r == 1:
            if g_is_silent:
                print( word )
            else:
                print( f'Password found: {word}' )
            return True
    
    return False


def main():
    args            = parse_command_line_arguments()
    pdf_file_loc    = get_param( args.file_loc, "File location:" )
    language        = get_param( args.language, "Regexp:" )
    g_is_silent     = args.is_silent

    if path.exists( pdf_file_loc ):
        pdf_file = PdfFileReader( pdf_file_loc )
    else:
        s_print( f'Cannot find PDF file at location {pdf_file_loc}' )
        exit( 1 )

    password = "" # Assume PDF with empty password can't be encrypted...

    if pdf_file.isEncrypted:
        if crack_password( pdf_file, language ):
            exit( 0 )
        else:
            s_print( "Password not found..." )
            exit( 1 )
    else:
        print( "PDF file is not encrypted." )
        exit( 0 )

if __name__ == "__main__":
    main()
