import sys, os, uuid, difflib
from shutil import copyfile

merge_extensions = set(["", ".adj", ".cfg", ".piclist", ".sfm", ".sty", ".tex", ".triggers", ".txt"])

def merge(ui, repo, args, **kwargs):
    global fullNameMine
    global fullNameParent
    global fullNameTheirs
    global hgRelativeDirName
    global mergeListFile
    global mergeRelativeDir
    global mergeToken
    if len(kwargs) != 1:
        return True
    hgRelativeDirName = '.hg'
    mergeRelativeDir = 'merge'
    mergeListFile = 'Merges.txt'
    mergeToken = '#Merge'
    fullNameMine = os.path.abspath(args[0])
    fullNameParent = os.path.abspath(args[1])
    fullNameTheirs = os.path.abspath(args[2])
    if not FindRepositoryRoot(ui):
        return True
    PrintInfo(ui)
    Run(ui)

def FindRepositoryRoot(ui):
    global mergeDir
    global repositoryDir
    d = os.path.dirname(fullNameMine)
    while d and d != '/':
        if os.path.isdir(os.path.join(d, hgRelativeDirName)):
            repositoryDir = d
            mergeDir = os.path.join(repositoryDir, mergeRelativeDir)
            return True
        d = os.path.abspath(os.path.join(d, os.pardir))

    ui.warn('File ' + fullNameMine + ' is not in a repository. No .hg found.')
    return False


def PrintInfo(ui):
    ui.write('Mine : ' + fullNameMine + '\nParent: ' + fullNameParent + '\nTheirs:' + fullNameTheirs + '\nRoot : ' + repositoryDir + '\nMerge: ' + mergeDir)


def Run(ui):
    if not os.path.isdir(mergeDir):
        os.makedirs(mergeDir)
    relativePathMine = fullNameMine[len(repositoryDir) + 1:]
    if 'ptxprint/' in relativePathMine.lower() and os.path.splitext(relativePathMine)[1].lower() in merge_extensions:
        merge3txt(fullNameMine, fullNameTheirs, fullNameParent, fullNameMine, [clash_keep_inserts, clash_keep_deletes, clash_keep_b])
        return
    mergePathParent = os.path.join(mergeRelativeDir, str(uuid.uuid4()))
    mergePathTheirs = os.path.join(mergeRelativeDir, str(uuid.uuid4()))
    ui.debug('Relative File Names\nMine :' + relativePathMine + '\nParent: ' + mergePathParent + '\nTheirs: ' + mergePathTheirs + '\n')
    ui.debug('Moving parent.\n')
    copyfile(fullNameParent, os.path.join(repositoryDir, mergePathParent))
    ui.debug('Moving Theirs.\n')
    copyfile(fullNameTheirs, os.path.join(repositoryDir, mergePathTheirs))
    ui.debug('Done moving.\n')
    with open(os.path.join(mergeDir, mergeListFile), 'a', 0) as (text_file):
        text_file.write(mergeToken + '\n')
        text_file.write(relativePathMine + '\n')
        text_file.write(mergePathParent + '\n')
        text_file.write(mergePathTheirs + '\n')
        os.fsync(text_file)

def theywin(a, b, base):
    return b

def merge3(a, b, parent, conflicts=[]):
    """ Returns a 3 way merge of the input sequences.
        Conflicts is a list of conflict resolution routines to call in order.
        Each is called with a return value from iter3_() and returns the output
        lines. """
    sa = difflib.SequenceMatcher(None, parent, a)
    sb = difflib.SequenceMatcher(None, parent, b)
    res = []
    for op in iter3_(sa.get_opcodes(), sb.get_opcodes()):
        if op[0] == "equal":        # take b
            res.extend(b[op[4]:op[5]])
        elif op[1] == "equal":      # take a
            res.extend(a[op[2]:op[3]])      # no conflict
        elif op[0] == "remove" and op[1] == "remove":
            pass
        elif len(conflicts):        # resolve conflict
            res.extend(conflicts[0](a, b, op, conflicts[1:]))
    return res

### Conflict resolution routines to be passed to merge3

def clash_mark(a, b, op, conflicts):
    """ Output conflict markers """
    res = ["<<<<<<< a\n"]
    res.extend(a[op[2]:op[3]])
    res.append("=======\n")
    res.extend(b[op[4]:op[5]])
    res.append(">>>>>>> b\n")
    return res

def clash_keep_inserts(a, b, op, conflicts):
    """ Keep all inserts: a then b. If lines are in both, only include them once """
    if op[1] == "insert":
        if op[0] == "insert":
            fa = a[op[2]:op[3]]
            fb = [x for x in b[op[4]:op[5]] if x not in fa]
            return fa + fb
        return b[op[4]:op[5]]
    elif op[0] == "insert":
        return a[op[2]:op[3]]
    elif len(conflicts):
        return conflicts[0](a, b, op, conflicts[1:])
    return []

def clash_keep_deletes(a, b, op, conflicts):
    """ If something deletes, ignore the other """
    if len(conflicts) and op[0] != "delete" and op[1] != "delete":
        return conflicts[0](a, b, op, conflicts[1:])
    return []

def clash_keep_a(a, b, op, conflicts):
    """ Keep a's edits """
    return a[op[2]:op[3]]

def clash_keep_b(a, b, op, conflicts):
    """ Keep b's edits """
    return b[op[4]:op[5]]

def getop_(a, ia):
    return a[ia] if ia < len(a) else ["equal", a[-1][2], a[-1][2], a[-1][2], a[-1][2]]

def iter3_(a, b):
    """ Yields (aaction, baction, astart, aend, bstart, bend, pstart, pend)
        from integrating two sequences of difference opcodes """
    ia = 0
    ib = 0
    pa = getop_(a, ia)
    pb = getop_(b, ib)
    pend = 0
    while ia < len(a) or ib < len(b):
        pstart = pend
        if pstart >= pa[2]:
            ia += 1
            pa = getop_(a, ia)
        if pstart >= pb[2]:
            ib += 1
            pb = getop_(b, ib)
        pstart = max(pstart, min(pa[1], pb[1]))
        pend = min(pa[2], pb[2])
        res = [pa[0], pb[0], pa[3]+pstart-pa[1], pa[4]+pend-pa[2],
                pb[3]+pstart-pb[1], pb[4]+pend-pb[2], pstart, pend]
        yield res

### Testing code

def merge3txt(a, b, parent, output, conflicts):
    files = []
    for f in (a, b, parent):
        with open(f, "rb") as inf:
            files.append([x for x in inf.readlines()])
    res = merge3(*files, conflicts=[clash_keep_inserts, clash_keep_deletes, clash_keep_b])
    with open(output, "wb") as outf:
        outf.write("".join(res))


if False and __name__ == '__main__':
    class UI:
        def warn(self, str):
            print ("W: " + str)
        def debug(self, str):
            print ("D:" + str)
        def write(self, str):
            print (str)
    if len(sys.argv) > 3:
        merge(UI(), None, [sys.argv[1], sys.argv[2], sys.argv[3]], r=1)
