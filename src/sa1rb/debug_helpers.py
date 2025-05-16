"""
Richard's Submission to SerpApi's Code Challenge:
various helper functions that are useful for debugging
"""

from json import load as json_load



def json_to_html( fn_inp_json, fn_outp_html ):

    doc = None
    with open( fn_inp_json, "rt", encoding="utf-8" ) as inp_f:
        doc = json_load( inp_f )

    with open( fn_outp_html, "wt", encoding="utf-8" ) as outp_f:

        outp_f.write( "<html>\n" )

        outp_f.write( "<h1>{}</h1>\n".format( fn_inp_json ) )

        for artwork in doc[ "artworks" ]:

            outp_f.write( "<h2>{}</h2>\n".format( artwork["name"] ) )

            outp_f.write(
                '<a href="{}"><img src="{}"></a>\n'\
                   .format(
                        artwork["link"],
                        artwork["image"] ) )

            for ext in artwork.get( "extensions", [] ):
                outp_f.write( "<p>{}</p>\n".format( ext ) )

        outp_f.write( "</html>\n" )
