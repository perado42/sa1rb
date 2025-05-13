"""Richard's Submission to SerpApi's Code Challenge: Reusable Function."""

from pprint import pprint
from json import dump as json_dump

from bs4 import BeautifulSoup




def paintings_html_to_json( fn_inp_html, fn_outp_json ):
    """Extract Van Gogh Paintings from HTML to JSON"""

    soup = None
    with open( fn_inp_html, "rb" ) as f_in:
        soup = BeautifulSoup( f_in.read(), features="html.parser" )
    
    pprint( soup )

    with open( fn_outp_json, "wt", encoding="utf-8" ) as f_out:
        json_dump( { "foo": "bar" }, f_out )
