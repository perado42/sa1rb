"""Richard's Submission to SerpApi's Code Challenge: reusable html_with_carousel_to_json function."""

from json import dump as json_dump

from bs4 import BeautifulSoup
from py_mini_racer import MiniRacer, JSEvalException


def html_with_carousel_to_json( fn_inp_html, fn_outp_json ):
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

    search_divs = soup.find_all( "div", id="search", limit=2 )
    assert len(search_divs) == 1
    search_div = search_divs[ 0 ]

    headings = search_div.find_all( "div", role="heading" )
    artwork_heading = None
    for heading in headings:
        heading_text_content = heading.get_text( strip=True, separator=' ' )
        if heading_text_content == "Artworks":
            assert artwork_heading is None
            artwork_heading = heading
    assert artwork_heading is not None

    artwork_links = None
    current = artwork_heading
    while current is not None:
        current_links = current.find_all( "a" )
        if current_links:
            assert artwork_links is None
            artwork_links = current_links
            break
        current = current.parent
    assert artwork_links

    artworks = []

    for link in artwork_links:

        link_href = link.get( "href" )
        assert link_href

        imgs = link.find_all( "img", limit=2 )
        assert len(imgs) == 1
        img = imgs[0]
        img_id = img.get( "id" )

        divs = link.find_all( "div" )
        div_texts = []
        for div in divs:
            if div.string:
                div_texts.append( div.string )
        assert len( div_texts ) >= 1

        new_artwork \
          = { "name": div_texts[ 0 ],
              "link": "https://www.google.com" + link_href }
        
        image = None
        if img_id in image_by_id:
            image = image_by_id.get( img_id, None )
        if not image:
            image = img.get( "data-src", None )

        if image:
            new_artwork[ "image" ] = image

        if len( div_texts ) > 1:
            new_artwork[ "extensions" ] = div_texts[ 1: ]

        artworks.append( new_artwork )

    with open( fn_outp_json, "wt", encoding="utf-8" ) as f_out:
        json_dump( { "artworks": artworks }, f_out, indent=2, ensure_ascii=False )
