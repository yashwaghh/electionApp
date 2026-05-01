import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Improved Security: Load configuration from environment variables instead of hardcoding.
// Locally, these would be in a .env file. In Cloud Run, they are injected via Secret Manager or environment variables.
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "demo_key_not_for_prod",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "election-project.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "election-project-096",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "election-project.appspot.com",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "1234567890",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:1234567890:web:abcdef123456"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
