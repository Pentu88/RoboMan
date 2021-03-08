import pygame
from datetime import datetime, timedelta
from random import random, randint, shuffle, choices

class RoboMan :
    def __init__(self) :
        pygame.init()

        self.peliLoppu = True
        self.lataaKuvat()
        self.uusiPeli()

        # Määritellään ikkuna
        ruutuKoko = (self.peliAlue['leveys'] * self.peliAlue['skaalaus'], self.peliAlue['korkeus'] * self.peliAlue['skaalaus'])
        self.ruutu = pygame.display.set_mode(ruutuKoko)
        pygame.display.set_caption('Roboman')

    def lataaKuvat(self) :
        self.kuvat = {}

        for nimi in [('robo', 0), ('hirvio', 0), ('kolikko', 3), ('ovi', 4)] :
            kuva = {}
            kuva['nimi'] = nimi[0]
            kuva['kuva'] = pygame.image.load('src/' + nimi[0] + '.png')
            kuva['koodi'] = nimi[1]
            kuva['e'] = None
            
            self.kuvat[nimi[0]] = kuva

    def uusiPeli(self) :
        self.aliustaKartta()
        self.pisteet = 0
        self.raja = 25
        self.ovi = None
        self.aika = datetime.now()
        # self.seuraavaAskel = datetime.now()
        # print(self.aika.strftime('%H:%M:%S')) # strftime('%H:%M:%S')
        # self.aika += timedelta(seconds = 0.5)
        # print(self.aika)

        self.fps = 6

        # Alustetaan peliAlueen tiedot
        self.peliAlue = {}
        self.peliAlue['korkeus'] = len(self.kartta)
        self.peliAlue ['leveys'] = len(self.kartta[0])
        self.peliAlue['skaalaus'] = self.kuvat['robo']['kuva'].get_height()

        # Alustetaan oliot
        self.oliot = []
        self.oliot.append(self.alustaOlio(self.kuvat['robo'], (4, 7)))
        self.oliot.append(self.alustaOlio(self.kuvat['hirvio'], (7, 3)))
        self.oliot.append(self.alustaOlio(self.kuvat['hirvio'], (9, 3)))

        # print('olioita: ', len(self.oliot), '(rivi 47)')

        # Alustetaan tekstit
        self.fontti = pygame.font.SysFont("Arial", int(self.peliAlue['skaalaus'] * 0.5))

        self.tekstit = {}
        self.tekstit['pisteet'] = self.fontti.render(f'Pisteet: 0', True, (255, 0, 0))
        self.tekstit['ohje'] = self.fontti.render(f'F2 - Uusi peli', True, (255, 0, 0))

        self.lisaaSatunnainenKolikko(3)
        # self.lisaaOvi()
    
        self.peliLoppu = False

    def aliustaKartta(self) :
        self.kartta = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
                        [1, 0, 1, 0, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0, 1, 0, 1],
                        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
                        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
                        [1, 0, 1, 0, 2, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1],
                        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def alustaOlio(self, kuva, koordit) :
        olio = {}
        olio['id'] = len(self.oliot)
        olio['kuva'] = kuva
        olio['koordit'] = koordit
        olio['korjaus'] = (0, 0)
        olio['liike'] = (0, 0)

        if olio['kuva']['nimi'] != 'robo' :
            self.arvoSuunta(olio)

        return olio 

    def run(self) :
        kello = pygame.time.Clock()

        while True :
            self.tapahtumatKasittely()
            self.liikeenKasittely()
            self.ruudunKasittely()

            # DEBUG    
            # Vääräpaikka mutta liikuta aikaa
            # if self.aika > self.seuraavaAskel :
            #     print('askel 0,5')
            #     self.seuraavaAskel += timedelta(seconds = 0.5)
            
            # print('aika', self.aika > self.seuraavaAskel)
            
            kello.tick(self.fps)
    
    def haeVapaat(self) :
        vapaatRuudut = []

        for y in range(self.peliAlue['korkeus']) :
            for x in range(self.peliAlue['leveys']) :
                if self.kartta[y][x] == 0 :
                    vapaatRuudut.append((y, x))

        return vapaatRuudut

    # peli tilanteen käsittely
    def lisaaPiste(self) :
        self.pisteet += 1
        self.tekstit['pisteet'] = self.fontti.render(f'Pisteet: {self.pisteet}', True, (255, 0, 0))

    def lisaaSatunnainenKolikko(self, maara = 1) :
        vapaat = self.haeVapaat()
        if len(vapaat) == 0 :
            print('EI vapaita ruutuja? (rivi: 101)')
            return

        for r in choices(vapaat, k = maara) :
            self.kartta[r[0]][r[1]] = self.kuvat['kolikko']['koodi']

    def lisaaOvi(self) :
        if self.ovi == None :
            vapaat = self.haeVapaat()
            if len(vapaat) == 0 :
                print('EI vapaita ruutuja? (rivi: 111)')
                return

            r = choices(vapaat, k = 1)[0]
            self.kartta[r[0]][r[1]] = self.kuvat['ovi']['koodi']
            self.ovi = r

    def tyhjaaRuutu(self) :
        robo = self.etsiRobo()
        self.oliot.clear()
        self.oliot.append(robo)
        self.peliLoppu == True

        for i in range(1, len(self.kartta) - 1) :
            for j in range(1, len(self.kartta[i]) - 1) :
                self.kartta[i][j] = 0

    def lapaisu(self) :
        self.tyhjaaRuutu()
        self.tekstit['loppu'] = self.fontti.render(f'VOITIT', True, (255, 0, 0))
 
    def havio(self) :
        self.tyhjaaRuutu()
        self.tekstit['loppu'] = self.fontti.render(f'HÄVISIT', True, (255, 0, 0))


    def tapahtumatKasittely(self) :
        for tapahtuma in pygame.event.get() :
            if tapahtuma.type == pygame.KEYDOWN :
                if tapahtuma.key == pygame.K_LEFT :
                    self.liike(-1, 0)

                if tapahtuma.key == pygame.K_RIGHT :
                    self.liike(1, 0)

                if tapahtuma.key == pygame.K_UP :
                    self.liike(0, -1)

                if tapahtuma.key == pygame.K_DOWN :
                    self.liike(0, 1)

                if tapahtuma.key == pygame.K_F2 :
                    self.uusiPeli()

            if tapahtuma.type == pygame.KEYUP :
                if tapahtuma.key == pygame.K_LEFT or tapahtuma.key == pygame.K_RIGHT :
                    if self.oliot[0]['liike'][0] == 0 :
                        return

                    self.liike(0, 0)
                
                if tapahtuma.key == pygame.K_DOWN or tapahtuma.key == pygame.K_UP :
                    if self.oliot[0]['liike'][1] == 0 :
                        return

                    self.liike(0, 0)

            if tapahtuma.type == pygame.QUIT :
                exit()

    def etsiRobo(self) :
        for olio in self.oliot :
            if olio['kuva']['koodi'] == self.kuvat['robo']['koodi'] :
                return olio

    def liike(self, liikeX, liikeY, olio = None) :
        if olio == None :
            olio = self.oliot[0]

        olio['liike'] = (liikeX, liikeY)

    # Mörön liikkeisin
    def arvoSuunta(self, olio) :
        suunnat = []

        x, y = olio['koordit']

        if self.kartta[y - 1][x] != 1:
            suunnat.append((0, -1))

        if self.kartta[y + 1][x] != 1:
            suunnat.append((0, 1))

        if self.kartta[y][x - 1] != 1:
            suunnat.append((-1, 0))

        if self.kartta[y][x + 1] != 1:
            suunnat.append((1, 0))

        olio['liike'] = choices(suunnat, k = 1)[0]

        # print(suunnat)
        # print(olio['liike'])

    def liiku(self, olio) :
        uusiX = olio['koordit'][0] + olio['liike'][0]
        uusiY = olio['koordit'][1] + olio['liike'][1]

        # Ei edetä seiniä päin
        if self.kartta[uusiY][uusiX] == 1 :
            if olio['id'] != self.etsiRobo()['id'] :
                self.arvoSuunta(olio)

            return

        olio['koordit'] = (uusiX, uusiY)

        # DEBUG for tests
        return (uusiX, uusiY)
        
        # Jos robo
        if olio['id'] == self.etsiRobo()['id'] :
            # Jos kolikko
            if self.kartta[uusiY][uusiX] == self.kuvat['kolikko']['koodi'] :
                self.kartta[uusiY][uusiX] = 0
                self.lisaaSatunnainenKolikko()
                self.lisaaPiste()

                if self.pisteet % 7 == 0:
                    self.oliot.append(self.alustaOlio(self.kuvat['hirvio'], (7, 3)))
                    self.fps += 1

                if self.pisteet >= self.raja and self.ovi == None :
                    self.lisaaOvi()

            if self.kartta[uusiY][uusiX] == self.kuvat['ovi']['koodi'] :
                # self.kartta[uusiY][uusiX] = 0
                self.lapaisu()

        if olio['id'] != self.etsiRobo()['id'] :
            x, y = olio['liike']

            if x != 0 and (self.kartta[y + 1][x] != 1 or self.kartta[y - 1][x] != 1) :
                self.arvoSuunta(olio)
                # print('Arvo:', olio['liike'])

            if y != 0 and (self.kartta[y][x + 1] != 1 or self.kartta[y][x + 1] != 1) :
                self.arvoSuunta(olio)

    def liikeenKasittely(self) :
        for olio in self.oliot :
            self.liiku(olio)

        # Törmäyksen tarkastus
        robo = self.etsiRobo()
        
        for olio in self.oliot :
            if robo['id'] == olio['id'] :
                continue
            
            if robo['koordit'] == olio['koordit'] :
                self.havio()

    def ruudunKasittely(self) :
        koko = self.peliAlue['skaalaus']
        self.ruutu.fill((255, 255, 255))

        # Piirretään kartta
        for y in range(self.peliAlue['korkeus']) :
            for x in range(self.peliAlue['leveys']) :
                ruutuKartalla = self.kartta[y][x]

                if self.kartta[y][x] == 1 : 
                    vari = (0, 0, 0)
                    pygame.draw.rect(self.ruutu, vari, (x * koko, y * koko, koko, koko))

                if self.kartta[y][x] == self.kuvat['kolikko']['koodi'] :
                    self.ruutu.blit(self.kuvat['kolikko']['kuva'], (x * koko + ((self.peliAlue['skaalaus'] - self.kuvat['kolikko']['kuva'].get_width()) / 2), y * koko + ((self.peliAlue['skaalaus'] - self.kuvat['kolikko']['kuva'].get_width()) / 2)))

                if self.kartta[y][x] == self.kuvat['ovi']['koodi'] :
                    self.ruutu.blit(self.kuvat['ovi']['kuva'], (x * koko + ((self.peliAlue['skaalaus'] - self.kuvat['ovi']['kuva'].get_width()) / 2), y * koko + ((self.peliAlue['skaalaus'] - self.kuvat['ovi']['kuva'].get_height()) / 2)))

        # Piirretään oliot
        for olio in self.oliot :
            if olio == None :
                # DEBUG
                # print('Väärän tyyppinen olio!')
                continue
            
            kuva = olio['kuva']

            olionX = self.peliAlue['skaalaus'] * olio['koordit'][0] + ((koko - kuva['kuva'].get_width()) / 2)
            olionY = self.peliAlue['skaalaus'] * olio['koordit'][1] + ((koko - kuva['kuva'].get_height()) / 2)
            
            self.ruutu.blit(kuva['kuva'], (olionX, olionY))
            # print(olionX, olionY)

        # Piirretään tekstit :
        self.ruutu.blit(self.tekstit['pisteet'], (koko * 1.25 , koko * 0.25))

        if 'loppu' in self.tekstit :
            self.ruutu.blit(self.tekstit['loppu'], (koko * 7.75 , koko * 4.75))
            self.ruutu.blit(self.tekstit['ohje'], (koko * 1.25 , koko * 9.25))

        pygame.display.flip()

    def boardTest(self) :
        koko = self.peliAlue['skaalaus']
        self.ruutu.fill((0, 0, 0))

        # board testi
        for y in range(self.peliAlue['korkeus']) :
            for x in range(self.peliAlue['leveys']) :
                ruutuKartalla = self.kartta[y][x]
                vari = (0, 255, 0)

                if y % 2 == 1 and x % 2 == 0 : 
                    vari = (255, 0, 0)
                
                if y % 2 == 0 and x % 2 == 1 : 
                    vari = (0, 0, 255)

                pygame.draw.rect(self.ruutu, vari, (x * koko, y * koko, koko, koko))
                # self.ruutu.blit()

        pygame.display.flip()

# Peliin jäi vielä reippaasti Refaktoroitavaa :
# - Pelin aloittaminen (voisi olla hyvä aloittaa vasta kun käyttäjä niin haluaa, eikä heti kun ikkuna aukeaa)
# - Robon haku (olio / id), sitä tarvitseviin kohtiin (jos Roboa ei löydy, palautetaanko None)
# - Mahdollisesti robo:n voisi säilöä omaan muuttujaansa ja möröt listaan
# - Rahan / Oven tarkasteluun voisi tehdä metodin (nyt tarkastelee kuvan id:n perusteella)
# - Liikkeen päivitys ajan mukaan (toisaalta nyt ei päivitetä turhaan ruutua uudelleen)
# - Mahdollistaisi eri nopeudet liikkeisiin
# - Liike voisi olla smuuthimpaa (Toisaalta aika hauska nyt kun siirrytään koko ruutu kerralla)
# - Mörkö voisi paremmin hakeutua pelaajaa kohti
# - Ehto rakennetta tulisi päivittää esineiden keräylyn ja ovelle tulemisen suhteen (nyt aika purkka viritelmä)
# - karttoja voisi olla useampi
# - Mörön suunnan arvontaa pitäisi tarkastella
# - Koko oven voisi ehkä hukata pelistä (tarkoitus kerätä vain mahdollisimman monta kolikkoa)
# - Lopetusta pitäisi parantaa, nyt peli kaatuu, jos pelin lopussa tyhjentää olio listan
# - Kuvan haku keskelle ruutua metodiksi (nyt jokainen kuva haetaan erikseen keskelle ruutua)"
# - Häviö ei aina toteudu vaikka mörkö ja robo törmääkin (auttaisiko apu taulukko?)
# - samassa ruudussa ei voi olla useita olioita!
