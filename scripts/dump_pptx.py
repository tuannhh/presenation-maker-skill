import sys
from pptx import Presentation
from pptx.util import Emu
p=Presentation(sys.argv[1])
print("size",p.slide_width,p.slide_height)
for i,s in enumerate(p.slides,1):
    print(f"\n===== SLIDE {i} =====")
    def walk(shapes,ind=0):
        for sh in shapes:
            t=sh.shape_type
            pos=f"[{sh.left//12700 if sh.left is not None else '?'},{sh.top//12700 if sh.top is not None else '?'} {sh.width//12700 if sh.width else '?'}x{sh.height//12700 if sh.height else '?'}]"
            if sh.shape_type==6:
                walk(sh.shapes,ind+1);continue
            txt=""
            if sh.has_text_frame:
                txt=" | ".join(par.text for par in sh.text_frame.paragraphs if par.text.strip())
            if getattr(sh,'has_table',False) and sh.has_table:
                txt="TABLE: "+" || ".join(" ; ".join(c.text for c in r.cells) for r in sh.table.rows)
            img=""
            if t==13: img=" IMG:"+sh.image.filename if hasattr(sh,'image') else " IMG"
            if txt or img:
                print("  "*ind+pos+img+" "+txt)
    walk(s.shapes)
    if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
        print("  NOTES:",s.notes_slide.notes_text_frame.text.strip()[:600])
