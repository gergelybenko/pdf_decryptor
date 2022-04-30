import pdf_decrypt

class __TEST__PdfFileMock:
    def __init__( self, password ):
        self.password = password

    def decrypt( self, word ):
        return word == self.password

def test_get_param( monkeypatch ):
    """
    Get param should return the param if it is not null
    """

    user_input = "Darth Vader"
    monkeypatch.setattr( "builtins.input", lambda _: "Darth Vader" )

    param = "mytestcase"
    assert pdf_decrypt.get_param(param, "") == param 
    assert pdf_decrypt.get_param("", "") == user_input

def test_s_print( capsys, monkeypatch ):
    """
    s_print should only print to screen if g_is_silent is false
    """

    text = "Test1234"
    monkeypatch.setattr( pdf_decrypt, "g_is_silent", True )
    pdf_decrypt.s_print( text )
    captured = capsys.readouterr()
    assert captured.out == ""

    monkeypatch.setattr( pdf_decrypt, "g_is_silent", False )
    pdf_decrypt.s_print( text )
    captured = capsys.readouterr()
    assert captured.out == text + "\n"

def test_crack_password( mocker ):
    ###########################
    # MOCK BEGIN
    ###########################

    mocker.patch( "exrex.generate", return_value=["apple", "pear", "strawberry"] )

    ###########################
    # MOCK END
    ###########################

    assert True  == pdf_decrypt.crack_password( __TEST__PdfFileMock( "strawberry" ), "" )
    assert False == pdf_decrypt.crack_password( __TEST__PdfFileMock( "Impossible" ), "" )