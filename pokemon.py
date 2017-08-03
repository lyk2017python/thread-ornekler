class Pokemon:
    def __init__(self, adi, agirlik=0, boy=0, yetenekler=[], hiz=0, savunma=0, saldiri=0, can=0, resim=None):
        self.adi = adi
        self.agirlik = agirlik
        self.boy = boy
        self.yetenekler = yetenekler
        self.hiz = hiz
        self.savunma = savunma
        self.saldiri = saldiri
        self.can = can
        self.resim = resim

    def hasarVer(self, pokemon):
        if self.can > 0:
            pokemon.hasarAl(self)
        else:
            print(self.adi + " pokemonunun saldırmak için canı yok")

    def hasarAl(self, pokemon):
        if self.can > 0:
            self.can -= pokemon.saldiri
            print(self.adi + " " + str(pokemon.saldiri) + " hasar aldı. Canı: %0.2f" % self.can)
        else:
            print(self.adi + " pokemonu zaten ölü")

    def yetenekKullan(self, isim):
        print(self.adi + " " + isim + " yeteneğini kullanıyor.")