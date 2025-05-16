"""Richard's Submission to SerpApi's Code Challenge: reusable html_with_artwork_to_json function."""

from json import dump as json_dump

from bs4 import BeautifulSoup
from py_mini_racer import MiniRacer, JSEvalException

ARTWORK_KCs \
  = [ "kc:/visual_art/visual_artist:works",
      "kc:/architecture/architect:designed" ]


def html_with_artwork_to_json( fn_inp_html, fn_outp_json ):
    """Extract Van Gogh Paintings from HTML to JSON"""


    soup = None
    with open( fn_inp_html, "rb" ) as f_in:
        soup = BeautifulSoup( f_in.read(), features="html.parser" )


    image_by_id = {}

    for script_ in soup.find_all( "script" ):

        script = script_.string
        if not script:
            continue
        if "_setImagesSrc" not in script:
            continue

        script = script.strip()

        jsctx = MiniRacer()
        jsctx.eval( r"""
            CAPTURED_II = null;
            CAPTURED_S = null;
            function _setImagesSrc( ii, s, r ) {
                CAPTURED_II = ii;
                CAPTURED_S = s;
            }
            """ )

        ii = None
        s = None

        try:
            jsctx.eval( script )
        except JSEvalException:
            pass

        ii = jsctx.eval( "CAPTURED_II" )
        s = jsctx.eval( "CAPTURED_S" )

        if ii and isinstance( s, str ):
            if isinstance( ii, str ):
                ii = [ ii ]
            for image_id in ii:
                image_by_id[ image_id ] = s


    artworks = []
    
    for kc in ARTWORK_KCs:

        for container in soup.find_all( attrs = { "data-attrid": kc } ):

            for record in container.find_all( "div" ):

                links = record.find_all( "a", limit=2 )
                imgs = record.find_all( "img", limit=2 )
                strings = []
                for div in record.find_all( "div" ):
                    if div.string:
                        strings.append( div.string )
                
                if not len(links) == 1:
                    continue
                if not len(imgs) == 1:
                    continue
                if not len(strings) >= 1:
                    continue

                link_href = links[0].get( "href" )
                if not link_href:
                    continue

                img_id = imgs[0].get( "id" )

                new_artwork \
                = { "name": strings[ 0 ],
                    "link": "https://www.google.com" + link_href }
                
                image = None
                if img_id in image_by_id:
                    image = image_by_id.get( img_id, None )
                if not image:
                    image = imgs[0].get( "data-src", None )

                if image:
                    new_artwork[ "image" ] = image

                if len( strings ) > 1:
                    new_artwork[ "extensions" ] = strings[ 1: ]

                artworks.append( new_artwork )


    with open( fn_outp_json, "wt", encoding="utf-8" ) as f_out:
        json_dump( { "artworks": artworks }, f_out, indent=2, ensure_ascii=False )
