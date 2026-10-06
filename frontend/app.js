const transactions = document.querySelector("#transactions");
const form = document.querySelector("#score-form");
const result = document.querySelector("#result");
const error = document.querySelector("#error");

function addTransaction(type = "entree", amount = "") {
  const row = document.createElement("div");
  row.className = "transaction-row";
  row.innerHTML = `
    <input class="amount" type="number" min="0" step="0.01" placeholder="Montant" value="${amount}" required>
    <select class="type">
      <option value="entree" ${type === "entree" ? "selected" : ""}>Entrée</option>
      <option value="sortie" ${type === "sortie" ? "selected" : ""}>Sortie</option>
    </select>
    <button class="remove" type="button" aria-label="Supprimer la transaction">×</button>
  `;
  row.querySelector(".remove").addEventListener("click", () => row.remove());
  transactions.appendChild(row);
}

function formatAmount(value) {
  return `${new Intl.NumberFormat("fr-FR").format(value)} FCFA`;
}

document.querySelector("#add-transaction").addEventListener("click", () => addTransaction());

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  error.hidden = true;
  const payload = [...document.querySelectorAll(".transaction-row")].map((row) => ({
    montant: Number(row.querySelector(".amount").value),
    type_transaction: row.querySelector(".type").value,
  }));

  try {
    const response = await fetch("/api/score", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transactions: payload }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Impossible de calculer le score.");
    document.querySelector("#score").textContent = data.score.toFixed(0);
    document.querySelector("#entries").textContent = formatAmount(data.total_entrees);
    document.querySelector("#exits").textContent = formatAmount(data.total_sorties);
    document.querySelector("#balance").textContent = formatAmount(data.solde);
    result.hidden = false;
  } catch (requestError) {
    error.textContent = requestError.message;
    error.hidden = false;
  }
});

addTransaction("entree", 1000);
addTransaction("sortie", 400);
