#cat > /mnt/user-data/outputs/image_gen.py << 'EOF'
import httpx
import os
from typing import Optional

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
UNSPLASH_URL = "https://api.unsplash.com/search/photos"

IMAGES_FALLBACK = {
    "eru": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Le_Eru%2C_un_plat_camerounais.jpg",
    "poulet dg": "https://cdn.aistoucuisine.com/assets/3e65b48a-7346-482c-8eaf-2d3ab935b676/poulet-dg.jpg?width=1280",
    "ndolé": "https://www.tasteatlas.com/images/dishes/c13c5b6bafb645bca9ca67069b9769cb.jpg",
    "moamba": "https://www.tasteatlas.com/images/dishes/c13c5b6bafb645bca9ca67069b9769cb.jpg",
    "foufou": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Fufu_with_Egusi_soup.jpg/800px-Fufu_with_Egusi_soup.jpg",
}

IMAGE_PLACEHOLDER = "https://images.unsplash.com/photo-1567364816519-cbc9c4ffe1eb?w=600&q=80"


async def chercher_image_unsplash(nom_plat: str, pays: str = "") -> Optional[str]:
    if not UNSPLASH_ACCESS_KEY:
        return None

    queries = [
        f"{nom_plat} african food dish",
        f"{nom_plat} {pays} cuisine",
        f"african {pays} traditional food",
    ]

    async with httpx.AsyncClient(timeout=8.0) as client:
        for query in queries:
            try:
                resp = await client.get(
                    UNSPLASH_URL,
                    params={
                        "query": query,
                        "per_page": 1,
                        "orientation": "landscape",
                    },
                    headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
                )
                data = resp.json()
                resultats = data.get("results", [])
                if resultats:
                    return resultats[0]["urls"]["regular"]
            except Exception:
                continue

    return None


def chercher_image_locale(nom_plat: str) -> Optional[str]:
    nom_lower = nom_plat.lower().strip()
    for cle, url in IMAGES_FALLBACK.items():
        if cle in nom_lower or nom_lower in cle:
            return url
    return None


async def obtenir_image_plat(nom_plat: str, pays: str = "", image_existante: str = "") -> str:
    if image_existante and image_existante.startswith("http"):
        return image_existante

    image_locale = chercher_image_locale(nom_plat)
    if image_locale:
        return image_locale

    image_unsplash = await chercher_image_unsplash(nom_plat, pays)
    if image_unsplash:
        return image_unsplash

    return IMAGE_PLACEHOLDER
#EOF
#echo "image_gen.py créé"

#Sortie
#image_gen.py créé
