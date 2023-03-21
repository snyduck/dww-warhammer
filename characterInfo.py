class Character:
    def __init__(self, name, blurb, charClass, career, status, distinguishingMark, starsign, bio, image):
        self.name = name
        self.blurb = blurb
        self.charClass = charClass
        self.career = career
        self.status = status
        self.distinguishingMark = distinguishingMark
        self.starsign = starsign
        self.bio = bio
        self.image = image


def buildCharacter(dbInfo):
    newCharObject = Character(name=dbInfo.charName,
                              blurb=dbInfo.charBlurb,
                              charClass=dbInfo.charClass,
                              career=dbInfo.charCareer,
                              status=dbInfo.charStatus,
                              distinguishingMark=dbInfo.charDistMark,
                              starsign=dbInfo.charStar,
                              bio=dbInfo.charBio,
                              image=dbInfo.charImg
                              )
    return newCharObject
