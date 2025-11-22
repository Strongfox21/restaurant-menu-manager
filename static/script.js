async function loadMenu() {
    let filter = document.getElementById("filter").value;

    let res = await fetch("/api/menu");
    let menu = await res.json();

    let container = document.getElementById("menu");
    container.innerHTML = "";

    menu.filter(item =>
        !filter || item.category.toLowerCase().includes(filter.toLowerCase())
    ).forEach(item => {
        container.innerHTML += `
            <div class="item">
                <h3>${item.name}</h3>
                <p>Цена: ${item.price} сом</p>
                <p>Категория: ${item.category}</p>
                <p>Статус: ${item.availability == "yes" ? "В наличии" : "Нет"}</p>
                <button class="delete-btn" onclick="deleteItem(${item.id})">Удалить</button>
            </div>
        `;
    });
}

async function addItem() {
    let newItem = {
        name: document.getElementById("name").value,
        price: document.getElementById("price").value,
        category: document.getElementById("category").value,
        availability: document.getElementById("availability").value
    };

    await fetch("/api/menu", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newItem)
    });

    loadMenu();
}

async function deleteItem(id) {
    await fetch(`/api/menu/${id}`, { method: "DELETE" });
    loadMenu();
}

function logout() {
    fetch("/logout").then(() => location.reload());
}

loadMenu();
