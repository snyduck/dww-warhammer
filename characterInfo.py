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
    newCharObject = Character(name=dbInfo[2],
                              blurb=dbInfo[4],
                              charClass=dbInfo[8],
                              career=dbInfo[9],
                              status=dbInfo[12],
                              distinguishingMark=dbInfo[10],
                              starsign=dbInfo[11],
                              bio=dbInfo[3],
                              image=dbInfo[5])
    return newCharObject


# tumney = Character(blurb="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt"
#                    ,name="tumney firebrand",charClass="rogue",career="foobar",status="alive",distinguishingMark="hair",starsign="drummer",bio="funny man")

# print(tumney.bio)