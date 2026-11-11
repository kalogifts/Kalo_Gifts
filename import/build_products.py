"""Builds products.csv for Shopify's product importer from the KALO catalogue.

Run:  python import/build_products.py
Edit the lists below (names, prices, colours, copy), re-run, then import the CSV in
Shopify admin > Products > Import. Everything marked PLACEHOLDER is a guess: replace
it with your real products before launch (you can also edit in Shopify after import).

Tags the theme understands:
  badge:Bestseller   shows a badge on the product card
  christmas-edition  puts the product in the Christmas edition section
  customisable       shows a "Customise on WhatsApp" button next to Add to bag
  whatsapp-only      no Add to bag, orders go through WhatsApp only
  no-gift-card       hides the handwritten gift card option
"""
import csv, itertools, os

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = ["S", "M", "L", "XL", "XXL"]

COLS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value",
    "Variant SKU", "Variant Grams", "Variant Inventory Tracker",
    "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price",
    "Variant Requires Shipping", "Variant Taxable", "Image Src", "Image Position",
    "Image Alt Text", "SEO Title", "SEO Description", "Variant Weight Unit", "Status",
]

# ---------------------------------------------------------------- oversized tees: 6 designs, 2 for Christmas
# PLACEHOLDER names, colours and price until the real photos and list arrive
TEE_PRICE = 799
TEES = [
    ("its-him-oversized-tee", "It's Him Oversized Tee", ["White", "Black"], "badge:Bestseller", False),
    ("loud-faith-oversized-tee", "Loud Faith Oversized Tee", ["Black", "Oat"], "", False),
    ("rent-free-oversized-tee", "Rent Free Oversized Tee", ["White", "Oat"], "", False),
    ("still-seek-him-oversized-tee", "Still Seek Him Oversized Tee", ["Black", "Bottle green"], "", False),
    ("merry-and-bright-oversized-tee", "Merry & Bright Oversized Tee", ["White", "Bottle green"], "badge:Christmas", True),
    ("let-it-snow-oversized-tee", "Let It Snow Oversized Tee", ["Black", "Sky blue"], "badge:Christmas", True),
]


def tee(h, title, colors, badge, xmas):
    tags = ", ".join(t for t in [badge, "tee", "oversized", "apparel", "christmas-edition" if xmas else ""] if t)
    return dict(
        handle=h, title=title, type="T-shirt", price=TEE_PRICE, grams=260,
        options=[("Colour", colors), ("Size", SIZES)], tags=tags,
        body="<p>Oversized fit with a printed design. Soft cotton that drapes well and wears in.</p>"
             "<p>Measured flat in inches. See the size guide for chest, length and shoulder.</p>",
        seo_title=f"{title} | Printed Oversized T-shirt | KALO Gifts Chennai",
        seo_desc=f"{title}: printed oversized tee in soft cotton. A faith-inspired gift from KALO Gifts, Chennai. Shipped across India.")


# ---------------------------------------------------------------- hoodie (1)
HOODIE = dict(
    handle="oversized-hoodie", title="Oversized Hoodie", type="Hoodie", price=1299, grams=650,
    options=[("Colour", ["Black", "Bottle green", "Oat"]), ("Size", SIZES)],
    tags="badge:Most gifted, hoodie, oversized, apparel",
    body="<p>Oversized hoodie in brushed fleece with a printed design. Cosy to wear, easy to gift.</p>"
         "<p>Measured flat in inches. See the size guide for chest, length and sleeve.</p>",
    seo_title="Printed Oversized Hoodie | KALO Gifts Chennai",
    seo_desc="Printed oversized hoodie in brushed fleece from KALO Gifts, Chennai. Shipped across India.")

# ---------------------------------------------------------------- bottles: 15 designs, 2 for Christmas (mostly thermo flasks)
# First 6 use your existing lines. 7 to 15 are PLACEHOLDERS until the printed bottles are ready.
BOTTLE_PRICE = 599
KNOWN = [
    ("its-him-bottle", "It's Him", "The reason for the season? It's Him.", "Isaiah 9:6", "badge:Bestseller", False),
    ("loud-faith-bottle", "Loud Faith", "Silent night, loud faith. No off season.", "John 1:5", "", False),
    ("the-manger-bottle", "The Manger", "The King of kings picked a manger.", "Luke 2:7", "badge:Christmas", True),
    ("rent-free-bottle", "Rent Free", "Jesus lives rent free in my heart.", "Ephesians 3:17", "badge:New", False),
    ("let-him-reign-bottle", "Let Him Reign", "Let it snow, let Him reign.", "Revelation 11:15", "badge:Christmas", True),
    ("still-seek-him-bottle", "Still Seek Him", "Wise men still seek Him.", "Matthew 2:2", "", False),
]
BOTTLES = KNOWN + [(f"bottle-design-{n:02d}", f"Bottle Design {n:02d}", "", "", "", False) for n in range(7, 16)]


def bottle(h, name, line, verse, badge, xmas):
    tags = ", ".join(t for t in [badge, "bottle", "christmas-edition" if xmas else ""] if t)
    if line:
        body = f"<p><em>“{line}”</em></p><p>{verse} (ESV). Printed thermo flask.</p>"
        seo_desc = f"Printed thermo flask with the line “{line}” and {verse}. From KALO Gifts, Chennai. Shipped across India."
    else:
        body = "<p>Printed thermo flask. Design details coming soon.</p>"
        seo_desc = "Printed thermo flask from KALO Gifts, Chennai. Shipped across India."
    return dict(
        handle=h, title=f"{name} Thermo Flask", type="Bottle", price=BOTTLE_PRICE, grams=420, options=None, tags=tags,
        body=body, seo_title=f"{name} Printed Thermo Flask | KALO Gifts", seo_desc=seo_desc)


# ---------------------------------------------------------------- photo frames (MOCK until the printed frames are ready)
FRAME_DESIGNS = [
    ("its-him-frame", "It's Him Photo Frame", "badge:New", False),
    ("the-manger-frame", "The Manger Photo Frame", "badge:Christmas", True),
    ("still-seek-him-frame", "Still Seek Him Photo Frame", "", False),
]
FRAME_PRICES = {"A5": 599, "A4": 899}  # PLACEHOLDER sizes and prices


def frame(h, title, badge, xmas):
    tags = ", ".join(t for t in [badge, "frame", "photo-frame", "christmas-edition" if xmas else ""] if t)
    return dict(
        handle=h, title=title, type="Frame", price=FRAME_PRICES["A5"], grams=500,
        options=[("Size", list(FRAME_PRICES))], tags=tags,
        body="<p>A printed photo frame with a message, with a photo inside. Ready to hang or stand, ready to gift.</p>",
        seo_title=f"{title} | Printed Photo Frame Gift | KALO Gifts Chennai",
        seo_desc=f"{title}: printed photo frame with a message. From KALO Gifts, Chennai. Shipped across India.")


# ---------------------------------------------------------------- hampers: tee + bottle + photo frame
HAMPERS = [
    dict(handle="the-christmas-hamper", title="The Christmas Hamper", type="Hamper", price=1899, grams=1500,
         options=[("Tee", ["Merry & Bright", "Let It Snow"]), ("Size", SIZES), ("Bottle", ["The Manger", "Let Him Reign"])],
         tags="badge:Christmas, hamper, christmas-edition, customisable",
         body="<p>A ready-to-gift box with a Christmas edition tee, a Christmas edition thermo flask and a printed photo frame.</p>"
              "<p>Choose your tee, size and bottle above. Want to swap a design or change what's in the box? Tap <b>Customise on WhatsApp</b>.</p>",
         seo_title="The Christmas Hamper | Tee, Bottle and Photo Frame Gift Box | KALO Gifts",
         seo_desc="A Christmas gift hamper with an oversized tee, a thermo flask and a photo frame, from KALO Gifts, Chennai. Shipped across India."),
    dict(handle="build-your-own-hamper", title="Build Your Own Hamper", type="Hamper", price=1499, grams=1500,
         options=None, tags="hamper, whatsapp-only, no-gift-card",
         body="<p>Pick any tee, any bottle and any photo frame, and we'll box them as a gift hamper.</p>"
              "<p>Tap <b>Customise on WhatsApp</b>, tell us what you'd like in the box, and we'll confirm the price and details with you.</p>",
         seo_title="Build Your Own Gift Hamper | KALO Gifts Chennai",
         seo_desc="Build a custom gift hamper with an oversized tee, a thermo flask and a photo frame. Order on WhatsApp. KALO Gifts, Chennai."),
]

# ---------------------------------------------------------------- handwritten gift card add-on (Rs. 50, added to the bag from product pages)
GIFT_CARD = dict(
    handle="handwritten-gift-card", title="Handwritten Gift Card", type="Add-on", price=50, grams=10, options=None,
    tags="add-on, no-gift-card",
    body="<p>A card with your message handwritten by us, tucked into the box. Up to 300 characters.</p>",
    seo_title="Handwritten Gift Card Add-on | KALO Gifts", seo_desc="Add a handwritten gift card with your message to any KALO gift for Rs. 50.")


def rows_for(p):
    base = {
        "Vendor": "KALO Gifts", "Type": p["type"], "Tags": p["tags"], "Published": "TRUE", "Status": "active",
        "Variant Inventory Tracker": "", "Variant Inventory Policy": "continue",
        "Variant Fulfillment Service": "manual", "Variant Taxable": "TRUE",
        "Variant Weight Unit": "g", "Variant Grams": p["grams"], "Variant Requires Shipping": "TRUE",
    }
    opts = p.get("options")
    combos = list(itertools.product(*[vals for _, vals in opts])) if opts else [("Default Title",)]
    out = []
    for i, combo in enumerate(combos):
        r = {k: "" for k in COLS}
        r.update(base)
        r["Handle"] = p["handle"]
        price = FRAME_PRICES[combo[0]] if p["type"] == "Frame" else p["price"]
        r["Variant Price"] = f"{price:.2f}"
        if opts:
            for n, ((oname, _), val) in enumerate(zip(opts, combo), start=1):
                r[f"Option{n} Name"] = oname if i == 0 else ""
                r[f"Option{n} Value"] = val
        else:
            r["Option1 Name"] = "Title" if i == 0 else ""
            r["Option1 Value"] = "Default Title"
        parts = [p["handle"].upper().replace("-", "")[:18]] + [c.upper().replace(" ", "").replace("&", "")[:5] for c in combo if c != "Default Title"]
        r["Variant SKU"] = "-".join(parts)
        if i == 0:
            r["Title"], r["Body (HTML)"] = p["title"], p["body"]
            r["SEO Title"], r["SEO Description"] = p["seo_title"], p["seo_desc"]
        else:
            for k in ("Vendor", "Type", "Tags", "Published", "Status"):
                r[k] = ""
        out.append(r)
    return out


def catalogue():
    items = [tee(*t) for t in TEES] + [HOODIE] + [bottle(*b) for b in BOTTLES]
    items += [frame(*f) for f in FRAME_DESIGNS] + HAMPERS + [GIFT_CARD]
    return items


if __name__ == "__main__":
    items = catalogue()
    path = os.path.join(HERE, "products.csv")
    seen = set()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        n = 0
        for p in items:
            assert len(p["options"] or []) <= 3 and len(rows_for(p)) <= 100, p["handle"]
            for r in rows_for(p):
                assert r["Variant SKU"] not in seen, r["Variant SKU"]
                seen.add(r["Variant SKU"])
                w.writerow(r)
                n += 1
    print(f"{len(items)} products, {n} variants -> {path}")
