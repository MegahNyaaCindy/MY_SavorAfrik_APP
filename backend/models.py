#cat > /mnt/user-data/outputs/models.py << 'EOF'
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PlatRecherche(BaseModel):
    nom: str = Field(..., min_length=2, max_length=100, description="Nom du plat à rechercher")


class Avis(BaseModel):
    nom_plat: str = Field(..., min_length=2, max_length=100)
    pays: Optional[str] = Field(None, max_length=60)
    note: int = Field(..., ge=1, le=5, description="Note de 1 à 5")
    commentaire: Optional[str] = Field(None, max_length=500)
    auteur: Optional[str] = Field(None, max_length=80)


class AvisEnBase(Avis):
    id: int
    date_creation: datetime

    class Config:
        from_attributes = True


class RecettePlat(BaseModel):
    nom: str
    pays_origine: str
    description: str
    ingredients: list[str]
    etapes: list[str]
    image_url: str
    note_moyenne: Optional[float] = None
    nombre_avis: Optional[int] = 0


class ReponseSuggestion(BaseModel):
    message: str
    succes: bool


class StatistiquesPlat(BaseModel):
    nom_plat: str
    note_moyenne: float
    nombre_avis: int
    pays: str


class StatistiquesPays(BaseModel):
    pays: str
    nombre_plats: int
    note_moyenne: float
#EOF
#echo "models.py créé"

#Sortie
#models.py créé
