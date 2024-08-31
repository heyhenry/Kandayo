class CharInfo:
    def __init__(self, ign, job, level, capped, bosses):
        self.ign = ign
        self.job = job
        self.level = level
        self.capped = capped
        self.bosses = bosses

    def charinfo_str(self):
        print(f"ign: {self.ign}, job: {self.job}, level: {self.level}, capped: {self.capped}")

class BossList:
    def __init__(self, cpb, hh, cyg, czak, pno, cqueen, cpierre, cvonbon, cvell, akechi, hmag, cpap, lotus, damien, gslime, lucid, will, gloom, darknell, vhilla, seren, kaling):
        self.cpb = cpb
        self.hh = hh
        self.cyg = cyg
        self.czak = czak
        self.pno = pno
        self.cqueen = cqueen
        self.cpierre = cpierre
        self.cvonbon = cvonbon
        self.cvell = cvell
        self.akechi = akechi
        self.hmag = hmag
        self.cpap = cpap
        self.lotus = lotus
        self.damien = damien
        self.gslime = gslime
        self.lucid = lucid
        self.will = will
        self.gloom = gloom 
        self.darknell = darknell
        self.vhilla = vhilla
        self.seren = seren
        self.kaling = kaling

