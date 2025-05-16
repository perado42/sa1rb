# Extract Van Gogh Paintings

## About Richard's Submission

### Setup

```
$ git clone https://github.com/serpapi/code-challenge.git
$ git clone https://github.com/perado42/sa1rb.git
$ cd sa1rb
$ python3 -mvenv .venv
$ source .venv/bin/activate
$ pip3 install --upgrade pip
$ pip3 install -e .
```

### Simple Usage: Generate JSON output from HTML input

You can generate the `*-artwork.json` files from the corresponding `.html`
files as follows.
```
$ mv files files.richard
$ cp -a ../code-challenge/files ./files
$ python3 -m sa1rb
```

The output produced from `van-gogh-paintings.html` will be found in
`van-gogh-paintings-artwork.json` in the `files` subdirectory.

### Manual Checks, Step 1: Recompose HTML from JSON for Inspection & Diffing

Having done that, you can use the following to convert the `*-artwork.json`
files to `*-recomposed.html` files.  These are useful for diffing and
visual inspection in a browser.

```
$ python3 -m sa1rb recompose
$ diff files/expected-array-recomposed.html files/van-gogh-paintings-artwork-recomposed.html 
2c2
< <h1>files/expected-array.json</h1>
---
> <h1>files/van-gogh-paintings-artwork.json</h1>
```

The above output in the diff would indicate that everything worked fine,
i.e. the mention of the filename in the heading is the only difference
between the html file recomposed from the reference
`expected-array.json` file, and the html file recomposed from the
`van-gogh-paintings-artwork.json` file generated in Step 1.

Diffing the JSON files themselves presents the difficulty that
textual diffs aren't necessarily significant w.r.t. the semantics
of these JSON objects.  Field order and syntactic variance in JSON
notation get in the way of that.  The recomposed HTML, however, is
always in a textually canonical representation.

### Manual Checks, Step 2: Do Visual Inspection

The HTML format presents a second opportunity for doing an ad-hoc
inspection: You can just fire up two browser windows side-by-side, and load
the original `van-gogh-paintings.html` in one and
`van-gogh-paintings-artwork-recomposed.html` in the other, to visually
inspect if the pictures, titles, and extra information were
reproduced correctly (disregarding the differences in formatting etc).

### Manual Checks, Step 3: Get Adventurous

1. Go to Google, run a search that will return artwork, such as
   "Andreas Gursky", and save as HTML.  (Hit `Ctrl+S` and select
   `Web Page, HTML only` in the file format, then save to the `files/`
   folder underneath where you've checked out this repo).
2. Repeat this a bunch of times to obtain several HTML files.  Try artists
   who produce different kinds of media (Van Gogh does paintings, Gursky does
   photography, Buonarotti does sculpture, Norman Foster does architecture,
   etc.)  Try with different browsers (When I tested, I used Firefox,
   but for the Andreas Gursky example, I used Chromium).  Try with IPs based
   in different countries.  (When I tested, I ran out of Germany and got
   German localization).
3. For a less adventurous version, instead of doing the above two steps,
   just revert to the `files/` directory from my repo, i.e.
   `rm -rf files && mv files.richard files`
4. Re-run `python3 -m sa1rb && python3 -m sa1rb recompose`
5. Load each `.html` file and corresponding
   `-artwork-recomposed.html` file side-by-side in browser windows
   and inspect visually.

### Automated Testing

```
$ python3 -m sa1rb test
```


## About the Challenge

Goal is to extract a list of Van Gogh paintings from the attached Google search results page.

![Van Gogh paintings](https://github.com/serpapi/code-challenge/blob/master/files/van-gogh-paintings.png?raw=true "Van Gogh paintings")

### Instructions

This is already fully supported on SerpApi. ([relevant test], [html file], [sample json], and [expected array].)
Try to come up with your own solution and your own test.
Extract the painting `name`, `extensions` array (date), and Google `link` in an array.

Fork this repository and make a PR when ready.

Programming language wise, Ruby (with RSpec tests) is strongly suggested but feel free to use whatever you feel like.

Parse directly the HTML result page ([html file]) in this repository. No extra HTTP requests should be needed for anything.

[relevant test]: https://github.com/serpapi/test-knowledge-graph-desktop/blob/master/spec/knowledge_graph_claude_monet_paintings_spec.rb
[sample json]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/van-gogh-paintings.json
[html file]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/van-gogh-paintings.html
[expected array]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/expected-array.json

Add also to your array the painting thumbnails present in the result page file (not the ones where extra requests are needed). 

Test against 2 other similar result pages to make sure it works against different layouts. (Pages that contain the same kind of carrousel. Don't necessarily have to be paintings.)

The suggested time for this challenge is 4 hours. But, you can take your time and work more on it if you want.
