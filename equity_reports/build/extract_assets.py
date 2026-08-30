"""Extract board/management headshots, product pack shots and the plant map from the
supplied earlier combined report, which sourced them from the companies' FY2025-26
annual reports and company pages.

Images are extracted programmatically rather than fetched (the network egress policy
blocks the company domains) or generated (synthesising images of real, named people
would not be acceptable). Run from the equity_reports/ directory.
"""
import pymupdf, numpy as np, PIL.Image as Image, os, shutil

SRC = ("/root/.claude/uploads/350cbc54-173b-5963-864b-e79e1b7aa719/"
       "8df5d3f5-Cement_Sector_UltraTech_Ambuja_Combined_Report.pdf")
OUT = "assets_extracted"

def composite_on_white(doc, xref, path):
    """Extract preserving the soft mask, then flatten onto white."""
    img = doc.extract_image(xref)
    pix = pymupdf.Pixmap(doc, xref)
    if img.get("smask", 0):
        try: pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(doc, img["smask"]))
        except Exception: pass
    if pix.n - pix.alpha >= 4:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    if pix.alpha:
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)
        rgb, al = a[..., :3].astype(np.float32), a[..., 3:4].astype(np.float32) / 255
        Image.fromarray((rgb * al + 255 * (1 - al)).clip(0, 255).astype(np.uint8)).save(path)
    else:
        pix.save(path)

def crop_grid(src, y0, y1, xs, names, prefix):
    im = Image.open(src).convert("RGB")
    for (x0, x1), nm in zip(xs, names):
        im.crop((x0, y0, x1, y1)).save(f"fig/people/{prefix}_{nm}.png")

def shrink(path, cap=460):
    im = Image.open(path).convert("RGB")
    if max(im.size) > cap:
        r = cap / max(im.size)
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    im.save(path, optimize=True)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs("fig/people", exist_ok=True); os.makedirs("fig/products", exist_ok=True)
    d = pymupdf.open(SRC)
    # page -> tag for the pages carrying the assets we want
    for pno, tag in {3: "utcl_bod", 21: "amb_prod", 22: "amb_bodpage",
                     23: "amb_ldrpage", 19: "amb_map"}.items():
        for idx, info in enumerate(d[pno - 1].get_images(full=True)):
            if pymupdf.Pixmap(d, info[0]).width < 40: continue
            composite_on_white(d, info[0], f"{OUT}/{tag}_{idx:02d}.png")

    utcl = ["km_birla","rajashree_birla","ak_agrawal","vikas_balia","vikram_bhalla",
            "v_chandrasekaran","anita_ramachandran","kk_maheshwari","kc_jhanwar",
            "vivek_agrawal","raj_narayanan","atul_daga","cs_chavan","anand_l",
            "ashok_kumar","ashish_dwivedi"]
    for i, nm in enumerate(utcl):
        shutil.copy(f"{OUT}/utcl_bod_{i:02d}.png", f"fig/people/utcl_{nm}.png")

    # Ambuja board: 8 cards on a regular 266px pitch, 212px wide
    bod_xs = [(101,313),(367,579),(632,844),(898,1110),
              (1370,1582),(1636,1848),(1902,2114),(2168,2380)]
    crop_grid(f"{OUT}/amb_bodpage_00.png", 448, 716, bod_xs,
              ["gautam_adani","karan_adani","vinod_bahety","rajnish_kumar",
               "maheswar_sahu","purvi_sheth","ameet_desai","praveen_garg"], "amb")

    # Ambuja leadership: 5 cards per row on a 354px pitch, 301px wide, two rows
    ldr_xs = [(101,402),(455,756),(809,1110),(1370,1671),(1724,2025)]
    crop_grid(f"{OUT}/amb_ldrpage_00.png", 458, 795, ldr_xs,
              ["l_vinod_bahety","rohit_soni","sanjay_gupta","praveen_k_garg",
               "bhimsi_kachhot"], "amb")
    crop_grid(f"{OUT}/amb_ldrpage_00.png", 1008, 1345, ldr_xs,
              ["sanjay_behl","john_varghese","madhavi_isanaka","vineet_bose",
               "vaibhav_dixit"], "amb")

    for i, nm in enumerate(["core","plus","kawach","compocem","coolwalls"]):
        shutil.copy(f"{OUT}/amb_prod_{i:02d}.png", f"fig/products/amb_{nm}.png")
    shutil.copy(f"{OUT}/amb_map_01.png", "fig/amb_plantmap.png")

    for p in (list(map(lambda f: f"fig/people/{f}", os.listdir("fig/people")))
              + list(map(lambda f: f"fig/products/{f}", os.listdir("fig/products")))
              + ["fig/amb_plantmap.png"]):
        shrink(p)
    print("assets extracted and downsized")
