#cat > /mnt/user-data/outputs/scraper.py << 'EOF'
import httpx
import re
from typing import Optional


THEMEALDB_URL = "https://www.themealdb.com/api/json/v1/1/search.php"
WIKI_URL = "https://fr.wikipedia.org/api/rest_v1/page/summary"

PAYS_AFRIQUE_CENTRALE = {
    "cameroon": "Cameroun",
    "cameroun": "Cameroun",
    "congo": "Congo",
    "republic of congo": "Congo",
    "democratic republic of congo": "RD Congo",
    "rdc": "RD Congo",
    "gabon": "Gabon",
    "central african republic": "RCA",
    "rca": "RCA",
    "chad": "Tchad",
    "tchad": "Tchad",
    "equatorial guinea": "Guinée Équatoriale",
    "guinée équatoriale": "Guinée Équatoriale",
    "guinea": "Guinée Équatoriale",
}

PLATS_LOCAUX = {
    "eru": {
        "pays_origine": "Cameroun",
        "description": "Plat traditionnel camerounais à base de feuilles d'okok (gnetum africanum) mijotées avec du waterleaf, de la viande fumée et du poisson séché. Riche en nutriments, c'est un des plats les plus appréciés du Cameroun anglophone.",
        "ingredients": [
            "500g de feuilles d'okok (eru) finement émincées",
            "500g de waterleaf (légume aquatique)",
            "300g de viande fumée (bœuf ou porc)",
            "200g de poisson fumé",
            "150ml d'huile de palme",
            "2 cubes de bouillon",
            "Sel et poivre au goût",
            "1 poignée de crevettes séchées",
        ],
        "etapes": [
            "Rincer et émincer finement les feuilles d'eru. Laver le waterleaf.",
            "Faire chauffer l'huile de palme dans une grande marmite à feu moyen.",
            "Ajouter la viande fumée et le poisson, faire revenir 5 minutes.",
            "Incorporer les crevettes séchées et les cubes de bouillon.",
            "Ajouter les feuilles d'eru et mélanger soigneusement.",
            "Cuire 20 à 25 minutes en remuant régulièrement.",
            "Ajouter le waterleaf en fin de cuisson, cuire encore 5 minutes.",
            "Rectifier l'assaisonnement et servir chaud avec du fufu ou du garri.",
        ],
    },
    "poulet dg": {
        "pays_origine": "Cameroun",
        "description": "Le Poulet DG (Directeur Général) est un plat festif camerounais à base de poulet frit accompagné de plantains mûrs et de légumes sautés. Symbole de prestige et de célébration.",
        "ingredients": [
            "1 poulet entier découpé en morceaux",
            "3 plantains mûrs coupés en rondelles",
            "2 poivrons (rouge et vert)",
            "3 carottes coupées en rondelles",
            "2 oignons émincés",
            "4 gousses d'ail",
            "1 morceau de gingembre frais",
            "Huile pour friture",
            "Sel, poivre, cubes de bouillon",
        ],
        "etapes": [
            "Assaisonner le poulet avec sel, poivre, ail et gingembre. Mariner 30 min.",
            "Faire frire les morceaux de poulet jusqu'à dorure. Réserver.",
            "Faire frire les rondelles de plantains jusqu'à coloration. Réserver.",
            "Dans la même poêle, faire revenir les oignons jusqu'à transparence.",
            "Ajouter les poivrons et carottes, faire sauter 5 minutes.",
            "Remettre le poulet frit dans la poêle, mélanger avec les légumes.",
            "Ajouter les plantains frits, mélanger délicatement.",
            "Laisser mijoter 10 minutes à feu doux. Servir chaud.",
        ],
    },
    "ndolé": {
        "pays_origine": "Cameroun",
        "description": "Le Ndolé est considéré comme le plat national du Cameroun. Préparé à base de feuilles amères (ndolé) mijotées avec des arachides, de la viande et des crevettes.",
        "ingredients": [
            "500g de feuilles de ndolé (fraîches ou en conserve)",
            "200g d'arachides crues",
            "300g de bœuf ou de porc",
            "200g de crevettes fraîches",
            "3 oignons",
            "4 gousses d'ail",
            "Huile de palme",
            "Sel, poivre, cubes Maggi",
        ],
        "etapes": [
            "Blanchir les feuilles de ndolé 3 fois pour enlever l'amertume.",
            "Moudre les arachides en pâte grossière.",
            "Cuire la viande avec oignon, ail, sel et bouillon jusqu'à tendreté.",
            "Dans une marmite, faire chauffer l'huile de palme.",
            "Ajouter la pâte d'arachide, faire revenir 10 minutes.",
            "Incorporer les feuilles de ndolé égouttées, bien mélanger.",
            "Ajouter la viande et son bouillon, laisser mijoter 20 minutes.",
            "Ajouter les crevettes en fin de cuisson. Servir avec du miondo ou du riz.",
        ],
    },
    "moamba": {
        "pays_origine": "Congo",
        "description": "La Moamba est un ragoût traditionnel congolais préparé avec de la pâte de noix de palme (moamba), du poulet ou du poisson, et des épices locales.",
        "ingredients": [
            "1 poulet découpé en morceaux",
            "400g de pâte de noix de palme (moamba)",
            "2 oignons",
            "3 gousses d'ail",
            "1 aubergine africaine",
            "Feuilles de cassave (optionnel)",
            "Sel, piment, bouillon",
        ],
        "etapes": [
            "Faire bouillir la pâte de moamba avec de l'eau pour en extraire l'huile.",
            "Filtrer pour obtenir une sauce onctueuse.",
            "Faire dorer le poulet dans un peu d'huile. Réserver.",
            "Dans la sauce moamba, ajouter oignon et ail émincés.",
            "Incorporer le poulet, l'aubergine et le piment.",
            "Laisser mijoter 30 à 40 minutes à feu moyen.",
            "Rectifier l'assaisonnement. Servir avec du foufou ou du riz.",
        ],
    },
    "sanga": {
        "pays_origine": "RCA",
        "description": "Le Sanga est un plat typique de la République Centrafricaine, préparé avec des feuilles de manioc pilées mélangées aux arachides et à la viande.",
        "ingredients": [
            "500g de feuilles de manioc",
            "200g d'arachides moulues",
            "300g de viande de gibier ou de poulet",
            "Huile de palme",
            "Oignon, ail, piment",
            "Sel, bouillon",
        ],
        "etapes": [
            "Piler les feuilles de manioc jusqu'à obtenir une pâte fine.",
            "Cuire les feuilles pilées à l'eau bouillante 15 minutes.",
            "Faire cuire la viande séparément avec oignon et bouillon.",
            "Mélanger les feuilles cuites avec la pâte d'arachide.",
            "Ajouter l'huile de palme et bien mélanger.",
            "Incorporer la viande cuite, laisser mijoter 15 minutes.",
            "Servir chaud avec du foufou de manioc.",
        ],
    },
    "daraba": {
        "pays_origine": "Tchad",
        "description": "Le Daraba est une sauce épaisse tchadienne à base de gombo séché pilé, accompagnée de viande ou de poisson et servie avec du boule (foufou de mil).",
        "ingredients": [
            "200g de gombo séché et pilé",
            "300g de viande (bœuf ou mouton)",
            "100g de poisson fumé",
            "2 oignons",
            "Huile d'arachide",
            "Sel, potasse, piment",
        ],
        "etapes": [
            "Réhydrater le gombo pilé dans de l'eau chaude 10 minutes.",
            "Faire cuire la viande dans de l'eau salée jusqu'à tendreté.",
            "Ajouter le gombo réhydraté dans le bouillon de viande.",
            "Incorporer le poisson fumé émietté et l'oignon.",
            "Ajouter un peu de potasse pour épaissir la sauce.",
            "Cuire à feu doux 20 minutes en remuant.",
            "Servir avec du boule (foufou de mil ou de sorgho).",
        ],
    },
}


def detecter_pays(nom_plat: str, zone: str = "") -> str:
    nom_lower = nom_plat.lower()
    zone_lower = zone.lower()

    for mot_cle, pays in PAYS_AFRIQUE_CENTRALE.items():
        if mot_cle in nom_lower or mot_cle in zone_lower:
            return pays

    for nom_local in PLATS_LOCAUX:
        if nom_local in nom_lower:
            return PLATS_LOCAUX[nom_local]["pays_origine"]

    return "Afrique Centrale"


async def chercher_recette_locale(nom_plat: str) -> Optional[dict]:
    nom_lower = nom_plat.lower().strip()
    for cle, data in PLATS_LOCAUX.items():
        if cle in nom_lower or nom_lower in cle:
            return {**data, "nom": nom_plat.title(), "source": "locale"}
    return None


async def chercher_recette_themealdb(nom_plat: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(THEMEALDB_URL, params={"s": nom_plat})
            data = resp.json()

            if not data.get("meals"):
                return None

            meal = data["meals"][0]

            ingredients = []
            for i in range(1, 21):
                ing = meal.get(f"strIngredient{i}", "").strip()
                mesure = meal.get(f"strMeasure{i}", "").strip()
                if ing:
                    ingredients.append(f"{mesure} {ing}".strip())

            instructions = meal.get("strInstructions", "")
            etapes = [e.strip() for e in re.split(r'\.\s+|\n+', instructions) if len(e.strip()) > 20][:10]

            zone = meal.get("strArea", "")
            pays = detecter_pays(nom_plat, zone)

            return {
                "nom": meal.get("strMeal", nom_plat),
                "pays_origine": pays,
                "description": f"Plat traditionnel découvert via notre base de données culinaire mondiale. Originaire de la région {zone}.",
                "ingredients": ingredients[:12],
                "etapes": etapes[:8],
                "image_url": meal.get("strMealThumb", ""),
                "source": "themealdb",
            }
    except Exception:
        return None


async def chercher_description_wikipedia(nom_plat: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(f"{WIKI_URL}/{nom_plat.replace(' ', '_')}")
            if resp.status_code == 200:
                data = resp.json()
                extrait = data.get("extract", "")
                if extrait and len(extrait) > 50:
                    return extrait[:400] + "..."
    except Exception:
        pass
    return ""


async def rechercher_plat_complet(nom_plat: str) -> dict:
    resultat_local = await chercher_recette_locale(nom_plat)
    if resultat_local:
        return resultat_local

    resultat_api = await chercher_recette_themealdb(nom_plat)
    if resultat_api:
        if not resultat_api.get("description") or "mondiale" in resultat_api["description"]:
            desc_wiki = await chercher_description_wikipedia(nom_plat)
            if desc_wiki:
                resultat_api["description"] = desc_wiki
        return resultat_api

    desc_wiki = await chercher_description_wikipedia(nom_plat)

    return {
        "nom": nom_plat.title(),
        "pays_origine": detecter_pays(nom_plat),
        "description": desc_wiki or f"Plat traditionnel d'Afrique Centrale. Les informations détaillées sur '{nom_plat}' seront enrichies prochainement.",
        "ingredients": ["Informations en cours de collecte pour ce plat."],
        "etapes": ["Recette en cours d'ajout à notre base de données."],
        "image_url": "",
        "source": "non_trouve",
    }
#EOF
#echo "scraper.py créé"

#Sortie
#scraper.py créé
