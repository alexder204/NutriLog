"use strict"
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const foodData = {
      name: document.getElementById("food-name").value,
      brand: document.getElementById("brand").value,
      calories: parseFloat(document.getElementById("calories").value),
      total_fat: parseFloat(document.getElementById("total-fat").value),
      protein: parseFloat(document.getElementById("protein").value),
      sugars: parseFloat(document.getElementById("sugars").value),
      sodium: parseFloat(document.getElementById("sodium").value),
      cholesterol: parseFloat(document.getElementById("cholesterol").value),
      potassium: parseFloat(document.getElementById("potassium").value),
      total_carbohydrates: parseFloat(document.getElementById("total_carbohydrates").value)
    };

    try {
      const res = await fetch("/add_food", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(foodData)
      });

      const result = await res.json();
      if (res.ok) {
        form.reset();
        loadFoods();
      } else {
        alert(result.error);
      }
    } catch (err) {
      console.error("Error:", err);
      alert("Failed to add food.");
    }
  });
});

async function loadFoods() {
    const response = await fetch("/api/foods");
    const foods = await response.json();

    if (foods.error) {
      console.warn("Not logged in");
      return;
    }

    const tableBody = document.querySelector("#food-table tbody");
    tableBody.innerHTML = "";

    foods.forEach(food => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${food.name}</td>
            <td>${food.brand || "-"}</td>
            <td>${food.calories}</td>
            <td>${food.total_fat}</td>
            <td>${food.protein}</td>
            <td>${food.total_carbohydrates}</td>
            <td>${food.sugars}</td>
            <td>${food.sodium}</td>
        `;

        tableBody.appendChild(row);
    });
}

loadFoods();