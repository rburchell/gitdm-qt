#
# aggregate per-month statistics for people
#
import sys, datetime

class CSVStat:
    def __init__ (self, name, employer, date, email):
        self.name = name
        self.employer = employer
        self.added = self.removed = 0
        self.date = date
        self.email = email
    def accumulate (self, p):
        self.added = self.added + p.added
        self.removed = self.removed + p.removed

PeriodCommitHash = { }

def AccumulatePatch (p):
    date = "%.2d-%.2d-01"%(p.date.year, p.date.month)
    authdatekey = "%s-%s"%(p.author.name, date)
    if authdatekey not in PeriodCommitHash:
        empl = p.author.emailemployer (p.email, p.date)
        stat = CSVStat (p.author.name, empl, date, p.email)
        PeriodCommitHash[authdatekey] = stat
    else:
        stat = PeriodCommitHash[authdatekey]
    stat.accumulate (p)

def OutputCSV (file):
    if file is None:
        return
    file.write ("Name\tAffliation\tDate\tAdded\tRemoved\tEmails\n")
    for date, stat in PeriodCommitHash.items():
        # sanitise names " is common and \" sometimes too
        empl_name = stat.employer.name.replace ("\"", ".").replace ("\\", ".")
        author_name = stat.name.replace ("\"", ".").replace ("\\", ".")
        author_email = stat.email.replace ("\"", ".").replace ("\\", ".")
        file.write ("\"%s\"\t\"%s\"\t%s\t%d\t%d\t%s\n"%(author_name, empl_name, stat.date, \
                                                    stat.added, stat.removed,
                                                    author_email))
