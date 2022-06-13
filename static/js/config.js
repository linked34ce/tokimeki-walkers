let currentUsername = "";

document.getElementById("change-username").addEventListener("click", () => {
    let inputUsername = document.getElementById("input-username");
    currentUsername = inputUsername.value;
    if (inputUsername.disabled) {
        inputUsername.disabled = !inputUsername.disabled;
        document.getElementById("change-username").style.display = "none";
        document.getElementById("confirm-username").style.display = "";
        document.getElementById("cancel-username").style.display = "";
    }
});

document.getElementById("cancel-username").addEventListener("click", () => {
    let inputUsername = document.getElementById("input-username");
    inputUsername.value = currentUsername;
    if (!inputUsername.disabled) {
        inputUsername.disabled = !inputUsername.disabled;
        document.getElementById("change-username").style.display = "";
        document.getElementById("confirm-username").style.display = "none";
        document.getElementById("cancel-username").style.display = "none";
    }
});