// ============================================================
//  config.js — Savor'Afrik
//  Détecte automatiquement si on est en local ou en production
// ============================================================
const LOCAL_API_URL = "http://127.0.0.1:8000";
const PROD_API_URL  = "https://my-savorafrik-app.onrender.com"; // ← à changer après déploiement

const _hostname = window.location.hostname;
const _isLocal  = _hostname === "localhost"
               || _hostname === "127.0.0.1"
               || _hostname === "";

const CONFIG = {
  API_URL:  _isLocal ? LOCAL_API_URL : PROD_API_URL,
  IS_LOCAL: _isLocal,
};

console.log("🌍 API URL utilisée :", CONFIG.API_URL);
