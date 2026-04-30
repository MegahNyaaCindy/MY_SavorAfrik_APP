#cat > /mnt/user-data/outputs/main.py << 'EOF'
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models import Avis, PlatRecherche, ReponseSuggestion
from database import init_db, inserer_avis, inserer_suggestion, get_stats_plats, get_stats_pays, get_avis_par_plat
from scraper import rechercher_plat_complet
from image_gen import obtenir_image_plat
from pydantic import BaseModel
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Savor'Afrik API",
    description="API pour découvrir les plats d'Afrique Centrale",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def accueil():
    return {"message": "Bienvenue sur l'API Savor'Afrik 🍲", "version": "1.0.0"}


@app.get("/plat/{nom_plat}")
async def decouvrir_plat(nom_plat: str):
    if len(nom_plat.strip()) < 2:
        raise HTTPException(status_code=400, detail="Le nom du plat est trop court.")

    recette = await rechercher_plat_complet(nom_plat)

    image_url = await obtenir_image_plat(
        nom_plat,
        recette.get("pays_origine", ""),
        recette.get("image_url", ""),
    )
    recette["image_url"] = image_url

    stats = get_avis_par_plat(nom_plat)
    recette["note_moyenne"] = stats["note_moyenne"]
    recette["nombre_avis"] = stats["nombre_avis"]

    return recette


@app.post("/avis")
async def soumettre_avis(avis: Avis):
    avis_id = inserer_avis(
        nom_plat=avis.nom_plat,
        pays=avis.pays,
        note=avis.note,
        commentaire=avis.commentaire,
        auteur=avis.auteur,
    )
    return {
        "succes": True,
        "message": "Merci pour votre avis ! 🙏",
        "avis_id": avis_id,
    }


class SuggestionForm(BaseModel):
    nom: Optional[str] = None
    email: Optional[str] = None
    sujet: str
    message: str


@app.post("/suggestion")
async def soumettre_suggestion(suggestion: SuggestionForm):
    if len(suggestion.message.strip()) < 10:
        raise HTTPException(status_code=400, detail="Le message est trop court.")

    suggestion_id = inserer_suggestion(
        nom=suggestion.nom,
        email=suggestion.email,
        sujet=suggestion.sujet,
        message=suggestion.message,
    )
    return ReponseSuggestion(
        message="Votre suggestion a été envoyée avec succès ! Merci 🎉",
        succes=True,
    )


@app.get("/stats/plats")
async def statistiques_plats():
    stats = get_stats_plats(limite=10)
    return {"plats": stats, "total": len(stats)}


@app.get("/stats/pays")
async def statistiques_pays():
    stats = get_stats_pays()
    return {"pays": stats, "total": len(stats)}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Savor'Afrik API"}
#EOF
#echo "main.py créé"

#Sortie
#main.py créé
