import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Note: In production, these should be environment variables.
const firebaseConfig = {
  projectId: "election-project-096",

  // Placeholder config values for local testing
  apiKey: "AIzaSy_placeholder_key",
  authDomain: "election-project-096.firebaseapp.com",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
