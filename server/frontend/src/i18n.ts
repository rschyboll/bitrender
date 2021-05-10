import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import translationEN from "./i18n/en.json";
import translationPL from "./i18n/pl.json";

const resources = {
  en: {
    translation: translationEN,
  },
  pl: {
    translation: translationPL,
  },
};

i18n.use(initReactI18next).init({
  resources,
  lng: "pl",
  fallbackLng: "en",

  interpolation: {
    escapeValue: false,
  },
});
