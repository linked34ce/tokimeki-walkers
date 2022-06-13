let currentUsername = "";
let currentProfile = "";

document.getElementById("change-username").addEventListener("click", () => {
    let inputUsername = document.getElementById("input-username");
    currentUsername = inputUsername.value;
    if (inputUsername.disabled) {
        inputUsername.disabled = !inputUsername.disabled;
        document.getElementById("change-username").style.display = "none";
        document.getElementById("confirm-username").style.display = "";
        document.getElementById("cancel-username").style.display = "";
        document.getElementById("submit").name = "username";
        document.getElementById("change-profile").className = "btn btn-sm btn-primary mt-2 disabled";
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
        document.getElementById("submit").name = "";
        document.getElementById("change-profile").className = "btn btn-sm btn-primary mt-2";
    }
});

document.getElementById("change-profile").addEventListener("click", () => {
    let inputProfile = document.getElementById("input-profile");
    currentProfile = inputProfile.value;
    if (inputProfile.disabled) {
        inputProfile.disabled = !inputProfile.disabled;
        document.getElementById("change-profile").style.display = "none";
        document.getElementById("confirm-profile").style.display = "";
        document.getElementById("cancel-profile").style.display = "";
        document.getElementById("submit").name = "profile";
        document.getElementById("change-username").className = "btn btn-sm btn-primary disabled";
    }
});

document.getElementById("cancel-profile").addEventListener("click", () => {
    let inputProfile = document.getElementById("input-profile");
    inputProfile.value = currentProfile;
    if (!inputProfile.disabled) {
        inputProfile.disabled = !inputProfile.disabled;
        document.getElementById("change-profile").style.display = "";
        document.getElementById("confirm-profile").style.display = "none";
        document.getElementById("cancel-profile").style.display = "none";
        document.getElementById("submit").name = "";
        document.getElementById("change-username").className = "btn btn-sm btn-primary";
    }
});