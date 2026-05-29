import sys, re, os
mapping = {'aArp': 'aArpBT', 'aMal': 'aArpBT', 'aSno': 'aArpBT',
           'bBar': 'bG1BT',  'bPou': 'bG1BT',  'bRam': 'bG1BT',
           'cGoi': 'cOGBT',  'cRbr': 'cOGBT',  'cWol': 'cOGBT', 'dOpi': 'dOLBT'}
with open(sys.argv[2], "w", encoding="utf8") as outf:
    with open(sys.argv[1], encoding="utf8") as inf:
        if "A9GLO" not in sys.argv[1]:
            # Not the GLO book, so just write out whatever came in
            outf.write(inf.read())
        else:
            thisGLOproj = os.path.basename(sys.argv[1])[5:9]
            othrGLOproj = mapping.get(thisGLOproj, thisGLOproj)
            gloData = inf.read()
            # Step 1: Read counterpart file to create a list of all entries which aren't CAT:name
            print(f"Inserting into {thisGLOproj} GLO headwords from {othrGLOproj}")
            othrGLOpath = sys.argv[1].replace(thisGLOproj, othrGLOproj)
            with open(othrGLOpath, encoding="utf8") as othrGLO:
                entries = re.findall(r"(\\p \\k ([^\\]+)\\k\*)[\r\n\s+]\\v (\d+)[\r\n\s+](?!\\hp .+?CAT:name)",othrGLO.read())
                # print(f"Total entries: {len(entries)}")
                # Step 2: Loop through the entries adding in the \k words\k* from the other GLO book
                for e in entries:
                    # print(f"{e[2]}  {e[1]}")
                    gloData = re.sub(fr"\\v {e[2]}[\r\n]+", fr"[{e[1].strip()}] \\v {e[2]}\r\n", gloData)
            # Step 3: Tidy up identical (unwanted) duplicates
            gloData = re.sub(r"(\\k ([^\\]+)\s*\\k\*[\r\n\s]+)(\[\2\] )", r"\1", gloData)
            outf.write(gloData)
