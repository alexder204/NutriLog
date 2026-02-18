"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  const loginForm = document.getElementById("login-form");

  if (signupForm) {
    signupForm.addEventListener("submit", handleSignup);
  }

  if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
  }
});

async function handleSignup(e) {
  e.preventDefault();

  const data = {
    username: document.getElementById("signup-username").value,
    email: document.getElementById("signup-email").value,
    password: document.getElementById("signup-password").value
  };

  const res = await fetch("/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();

  if (res.ok) {
    alert("Account created. You can now login.");
    window.location.href = "/login";
  } else {
    alert(result.error);
  }
}

async function handleLogin(e) {
  e.preventDefault();

  const data = {
    username: document.getElementById("login-username").value,
    password: document.getElementById("login-password").value
  };

  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();

  if (res.ok) {
    alert("Logged in!");
    window.location.href = "/";
  } else {
    alert(result.error);
  }
}