// Resume layout. Content lives in resume.json; build with build.py.
#let data = json("resume.json")
#let phone = sys.inputs.at("phone", default: "")
#let ink = rgb("#050505")

#set document(title: "Brandon Russell - Resume", author: "Brandon Russell")
#set page(paper: "us-letter", margin: (x: 54pt, top: 44pt, bottom: 44pt))
// Ligatures are off so "ti"/"ft" stay as plain letters for copy, search, and resume parsers.
#set text(font: "Calibri", size: 10pt, fill: ink, hyphenate: false, ligatures: false)
#set par(leading: 0.5em, spacing: 0.7em)
#set list(indent: 18pt, body-indent: 12pt, spacing: 0.75em, marker: text(size: 9pt)[•])

// "**bold**" is web-only emphasis and is dropped here; "*italic*" is kept.
#let md(s) = {
  for (i, part) in s.replace("**", "").split("*").enumerate() {
    if calc.odd(i) { emph(part) } else { part }
  }
}
#let strong-md(s) = if s.starts-with("**") { strong(s.replace("**", "")) } else { md(s) }
#let rule = line(length: 100%, stroke: 0.6pt + black)

#let section(title) = block(above: 16pt, below: 9pt, breakable: false, sticky: true,
  stack(dir: ttb, spacing: 4pt, text(size: 12pt, weight: "bold", upper(title)), rule))

#let two-columns(cols) = grid(
  columns: (1fr, 1fr), column-gutter: 12pt,
  ..cols.map(col => list(..col.map(strong-md))),
)

// A title line with a right-aligned date, an italic line under it, then optional bullets.
#let entry(title, date, sub, bullets: ()) = block(breakable: false, above: 11pt, below: 0pt, {
  block(above: 0pt, below: 4.5pt, grid(columns: (1fr, auto), strong(title), date))
  block(above: 0pt, below: 0pt, emph(sub))
  if bullets.len() > 0 { block(above: 6pt, below: 0pt, list(..bullets.map(md))) }
})

// ---- header ----------------------------------------------------------------
#align(center, stack(dir: ttb, spacing: 9pt,
  text(size: 24pt, fill: black, data.name),
  rule,
  text(size: 12pt, fill: black,
    (phone, link("mailto:" + data.email, data.email), data.location).filter(x => x != "").join(h(18pt))),
  text(size: 11pt, link("https://" + data.website, data.website)),
  rule,
  block(width: 96%, text(size: 11pt, style: "italic", data.summary)),
))

#section("Certifications")
#two-columns(data.certifications)

#section("Skills")
#two-columns(data.skills)

#section("Education")
#for e in data.education { entry(e.degree, e.date, e.school) }

#section("Publications")
#list(..data.publications.map(p => {
  md(p.text)
  if "url" in p { [ ] + link(p.url, text(fill: rgb("#467886"), underline(p.url))) }
}))

// Experience gets page 2 to itself.
#pagebreak()
#section("Professional Experience")
#for r in data.experience { entry(r.title, r.dates, r.org + ", " + r.location, bullets: r.bullets) }
