import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: import.meta.env.FIREBASE_API_KEY,
  authDomain: "pet-food-advice.firebaseapp.com",
  projectId: "pet-food-advice",
  storageBucket: "pet-food-advice.appspot.com",
  messagingSenderId: import.meta.env.SENDER_ID,
  appId: import.meta.env.APP_ID,
};

const app = initializeApp(firebaseConfig);