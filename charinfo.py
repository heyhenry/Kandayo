class CharInfo:
    def __init__(self, ign, job, level, capped):
        self.ign = ign
        self.job = job
        self.level = level
        self.capped = capped

    def charinfo_str(self):
        print(f"ign: {self.ign}, job: {self.job}, level: {self.level}, capped: {self.capped}")