# Memorial Cemetery of St. John's Church (MemCem)

Static site, same approach as stjcsh.org: plain HTML, no framework, nothing to build on the server.
Provisional address: cemetery.stjcsh.org (set as `BASE` in `build.py`).

## Editing
Header, nav and footer are written once in `build.py`. To change a page or the nav, edit `build.py`
and run `python3 build.py`; it rewrites every page. Don't hand-edit the generated HTML.

## Before launch: items marked in yellow on the pages (`<mark class="confirm">`)
- Burial: fees are deliberately not published; the page directs people to the Cemetery Superintendent. Eligibility is settled (members of St. John's and children of those buried here). Confirm "children" is the intended reading of "one generation".
- Staff: the old parish page listed Darlene Gubner as Secretary; Gideon listed Monica Pierce as Administrator. Confirm.
- Motto "Et Audierent Qui Vivent": add an English line if wanted

When all are settled, remove the `C(...)` wrappers and the draft banner in `build.py`, rebuild, and search the output for `confirm`.

## Credits to keep
- Entrance sign photo: Gideon Pollach.
- Photos: David Almeida and Michael Fairchild, used with permission (keep the permission on file).
- Maps: Heritage Landscapes LLC, 2019 landscape guide; historic plans courtesy of the Olmsted Archives, FLONHS.
- Don't post the full 2019 guide PDF without checking its terms.

## Dates to verify
Sources differ on early Olmsted dates (guide: 1918-21 plans; Cultural Landscape Foundation: work by 1915, last plan 1958)
and on acreage (34 vs 36). The History page words these cautiously.
