// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBuflL8Z6WKePDr6GiH71QL1nSeRRW4d_A",
  authDomain: "sdm-models-898c8.firebaseapp.com",
  databaseURL: "https://sdm-models-898c8-default-rtdb.firebaseio.com",
  projectId: "sdm-models-898c8",
  storageBucket: "sdm-models-898c8.appspot.com",
  messagingSenderId: "646096058395",
  appId: "1:646096058395:web:247a20675b50cea67ea0be",
  measurementId: "G-74QDZR3MDX"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);