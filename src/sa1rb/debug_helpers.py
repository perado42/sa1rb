"""
Richard's Submission to SerpApi's Code Challenge:
various helper functions that are useful for debugging
"""

from json import load as json_load



def json_to_html( f_inp_json, f_outp_html ):

    doc = None
    doc = json_load( f_inp_json )

    f_outp_html.write( "<html>\n" )

    for artwork in doc[ "artworks" ]:

        f_outp_html.write( "<h2>{}</h2>\n".format( artwork["name"] ) )

        f_outp_html.write(
            '<a href="{}"><img src="{}"></a>\n'\
                .format(
                    artwork["link"],
                    artwork["image"] ) )

        for ext in artwork.get( "extensions", [] ):
            f_outp_html.write( "<p>{}</p>\n".format( ext ) )

    f_outp_html.write( "</html>\n" )
