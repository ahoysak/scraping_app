import reinigungschemie.reinigungschemie
import waschraum.waschraum
import gastronomiebedarf.gastronomiebedarf
import reinigungsmaschinen.reinigungsmaschinen
import mobileReinigung.mobile
import Reinigungshilfen.reinigungshilfen
import Entsorgung.entsorgung
import Medical.medical
import Spezialanwendungen.spezialanwendungen


while True:
    menu = int(input('Write number for Scraping\n'
                     '1. Reinigungschemie\n'
                     '2. Waschraum-Hygiene\n'
                     '3. Gastronomiebedarf\n'
                     '4. Reinigungsmaschinen\n'
                     '5. Mobile Reinigung\n'
                     '6. Reinigungshilfen\n'
                     '7. Entsorgung\n'
                     '8. Medical\n'
                     '9. Spezialanwendungen\n'
                     'Your number: '))

    if menu == 1:
        reinigungschemie.reinigungschemie.run()
    elif menu == 2:
        waschraum.waschraum.run()
    elif menu == 3:
        gastronomiebedarf.gastronomiebedarf.run()
    elif menu == 4:
        reinigungsmaschinen.reinigungsmaschinen.run()
    elif menu == 5:
        mobileReinigung.mobile.run()
    elif menu == 6:
        Reinigungshilfen.reinigungshilfen.run()
    elif menu == 7:
        Entsorgung.entsorgung.run()
    elif menu == 8:
        Medical.medical.run()
    elif menu == 9:
        Spezialanwendungen.spezialanwendungen.run()
    elif menu == 0:
        break
    else:
        print('\n Wrong choice, try again\n')
