''' The publications of configurations across projects: what each is called, its books, and its
    titles, ISBN and other variables, read from and written to each project's ptxprint.cfg.

    A config's own variables ([vars]) are its "main" values, given here under the publication
    id MAIN. A publication ([publication.<id>]) has its books and its own values of the
    variables that are marked as differing between publications ([vars.publishable]).
'''

import os, re, configparser
from ptxprint.manager.validate import readConfig, asBool

MAIN = ""           # the publication id used here for the config's own variables
PUBSECT = "publication."
FIRSTCOLUMNS = ["t1title", "t2title", "maintitle", "subtitle", "isbn"]
ALWAYSPUBLISHABLE = ("maintitle", "subtitle")       # PTXprint gives every publication these

class ConfigPublications:
    ''' The variables and publications of one project's config '''

    def __init__(self, validator, prjid, cfg):
        self.prjid = prjid
        self.cfg = cfg
        self.path = os.path.join(validator.configDir(prjid, cfg), "ptxprint.cfg")
        self.read()

    def read(self):
        config = readConfig(self.path)
        self.variables = dict(config.items("vars")) if config.has_section("vars") else {}
        self.publishable = set(ALWAYSPUBLISHABLE)
        if config.has_section("vars.publishable"):
            self.publishable = set(k for k in config.options("vars.publishable") if asBool(config, "vars.publishable", k))
        self.pubs = {}
        for s in config.sections():
            if s.startswith(PUBSECT):
                self.pubs[s[len(PUBSECT):]] = dict(config.items(s))
        scope = config.get("project", "bookscope", fallback="single")
        self.books = config.get("project", "book", fallback="") if scope == "single" else \
                     config.get("project", "booklist", fallback="") if scope == "multiple" else f"({scope})"

    def value(self, pubid, key):
        ''' What this variable is for the publication: its own value, else the config's '''
        if pubid != MAIN and key in self.pubs.get(pubid, {}):
            return self.pubs[pubid][key]
        return self.variables.get(key, "")

    def booksOf(self, pubid):
        return self.books if pubid == MAIN else self.pubs.get(pubid, {}).get("__books", "")

    def apply(self, edits=(), adds=(), deletes=()):
        ''' edits: [(pubid, key, value)] where key "__books" is a publication's books
            adds: [(pubid, books)]   deletes: [pubid]
            A variable given a value in a publication is marked as differing between publications,
            or PTXprint would drop it from them the next time it saved the config. '''
        config = readConfig(self.path)
        def section(name):
            if not config.has_section(name):
                config.add_section(name)
            return name
        for pubid in deletes:
            config.remove_section(PUBSECT + pubid)
        for pubid, books in adds:
            if config.has_section(PUBSECT + pubid):
                raise ValueError(f"{self.prjid} / {self.cfg} already has a publication called {pubid}")
            s = section(PUBSECT + pubid)
            config.set(s, "__books", books)
            config.set(s, "__select", "false")
        for pubid, key, value in edits:
            if pubid == MAIN:
                if key == "__books":
                    continue            # the book chosen in PTXprint itself isn't set from here
                config.set(section("vars"), key, value)
            else:
                if not config.has_section(PUBSECT + pubid):
                    continue            # deleted in this same apply
                config.set(PUBSECT + pubid, key, value)
                if not key.startswith("__"):
                    if not config.has_section("vars.publishable"):
                        # until now only these two differed: keep them so
                        for k in ALWAYSPUBLISHABLE:
                            config.set(section("vars.publishable"), k, "True")
                    config.set("vars.publishable", key, "True")
                    if not config.has_option(section("vars"), key):
                        config.set("vars", key, "")
        with open(self.path, "w", encoding="utf-8") as outf:
            config.write(outf)
        self.read()


class PublicationTable:
    ''' The publications of a number of project configs, as one table '''

    def __init__(self, validator, pairs):
        self.validator = validator
        self.configs = {}
        for prjid, cfg in pairs:
            try:
                self.configs[(prjid, cfg)] = ConfigPublications(validator, prjid, cfg)
            except (configparser.Error, OSError):
                pass

    def columns(self):
        ''' The variables worth a column: the titles and ISBN that are in use, and whatever any
            publication has a value of its own for '''
        allvars = set()
        inpubs = set()
        for c in self.configs.values():
            allvars.update(c.variables)
            inpubs.update(c.publishable & (set(c.variables) | set(ALWAYSPUBLISHABLE)))
            for p in c.pubs.values():
                inpubs.update(k for k in p if not k.startswith("__"))
        first = [k for k in FIRSTCOLUMNS if (k in allvars or k in inpubs)
                 and (k in inpubs or any(c.variables.get(k, "").strip() for c in self.configs.values()))]
        return first + sorted(k for k in inpubs if k not in first)

    def otherVariables(self):
        ''' Variables that could be given a column '''
        cols = set(self.columns())
        res = set()
        for c in self.configs.values():
            res.update(k for k in c.variables if k not in cols)
        return sorted(res)

    def rows(self):
        ''' Returns [(prjid, cfg, pubid)]: each config's main values, then its publications '''
        res = []
        for (prjid, cfg), c in sorted(self.configs.items(), key=lambda x: (x[0][0].lower(), x[0][1].lower())):
            res.append((prjid, cfg, MAIN))
            res.extend((prjid, cfg, p) for p in sorted(c.pubs, key=str.lower))
        return res

    def publicationNames(self):
        res = set()
        for c in self.configs.values():
            res.update(c.pubs)
        return sorted(res, key=str.lower)


def validBooks(books):
    ''' A light check of a books value such as "JAS", "JAS GLO" or "MAT 1-7" '''
    books = books.strip()
    if not books:
        return False
    return all(re.match(r"^([A-Za-z0-9]{3}|\d+(-\d+)?|[A-Za-z0-9]{3}-[A-Za-z0-9]{3})$", b) for b in re.split(r"[\s,;]+", books))
