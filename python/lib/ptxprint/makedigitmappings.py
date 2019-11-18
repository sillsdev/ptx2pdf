# Generate the digit mapping files for XeTeX macros in Paratext for all known digits/scripts

# Code	Name	c	d	e	f	g	h	i	j
# 0030	DIGIT ZERO	Nd	0	EN		0	0	0	N
# 0031	DIGIT ONE	Nd	0	EN		1	1	1	N
# 0032	DIGIT TWO	Nd	0	EN		2	2	2	N
# 0033	DIGIT THREE	Nd	0	EN		3	3	3	N
# 0034	DIGIT FOUR	Nd	0	EN		4	4	4	N
# 0660	ARABIC-INDIC DIGIT ZERO	Nd	0	AN		0	0	0	N
# 0661	ARABIC-INDIC DIGIT ONE	Nd	0	AN		1	1	1	N
# 0662	ARABIC-INDIC DIGIT TWO	Nd	0	AN		2	2	2	N
# 0663	ARABIC-INDIC DIGIT THREE	Nd	0	AN		3	3	3	N
# 0664	ARABIC-INDIC DIGIT FOUR	Nd	0	AN		4	4	4	N

# ; FC ... 
# LHSName	"Digits"
# RHSName	"ThaiDigits"

# pass(Unicode)
# U+0030 <> U+0E50 ;
# U+0031 <> U+0E51 ;
# U+0032 <> U+0E52 ;
# U+0033 <> U+0E53 ;
# U+0034 <> U+0E54 ;
# U+0035 <> U+0E55 ;
# U+0036 <> U+0E56 ;
# U+0037 <> U+0E57 ;
# U+0038 <> U+0E58 ;
# U+0039 <> U+0E59 ;

import re, os, subprocess
digifile = r"C:\ptx2pdf\python\lib\ptxprint\UnicodeDigits.lst"
outpath = r"C:\ptx2pdf\python\lib\ptxprint\mappings"
teckitcompiler = r"C:\Program Files (x86)\SIL\TECkit\TECkit_Compile.exe"
diginames = ('ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE')
digicodes = (0,1,2,3,4,5,6,7,8,9)
d2c = dict(zip(diginames, digicodes))
prevscript = ''
with open(digifile, "r", encoding="utf-8") as inf:
    for l in inf.readlines():
        a = l.split("\t")
        code = a[0]
        try:
            script = a[1].split(" DIGIT ")[0]
            RHSName = re.sub("[ -]","",script.title())
            outfname = os.path.join(outpath,RHSName.lower()+"digits.map")
            digit = a[1].split(" DIGIT ")[1]
            if digit in diginames:
                if digit == 'ZERO' or prevscript != script:
                    print('; FC ... \nLHSName\t"Digits"\nRHSName\t"{}Digits"\n\npass(Unicode)'.format(RHSName))
                    digilist = []
                    digilist.append('; FC ... \nLHSName\t"Digits"\nRHSName\t"{}Digits"\n\npass(Unicode)\n'.format(RHSName))
                    prevscript = script
                print("U+003{} <> U+{} ; {} DIGIT {}".format(d2c[digit], code, script, digit))
                digilist.append("U+003{} <> U+{} ;\n".format(d2c[digit], code))
                if digit == 'NINE':
                    print("\n")
                    with open(outfname, "w", encoding="utf-8") as outf:
                        outf.write("".join(digilist)+"\n")
                    subprocess.run([teckitcompiler, outfname])
        except:
            pass

