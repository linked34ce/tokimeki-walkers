window.addEventListener("DOMContentLoaded", () => {
    let cookieString = document.cookie;
    let array = cookieString.split(";");
    let cookies = {};
    let group = "";

    array.forEach(function(string) {
        let content = string.split("=");
        if (content[0].trim() === "group") {
            group = content[1]
        }
    });

    //let group = cookies.group;
    console.log(group)

    if (!group) {
        group = "all";
    }

    if (group === "all") {
        showAll();
    } else {
        showOnly(group);
    }
    document.getElementById("season1-opening").addEventListener("click", () => {
        showOnly("season1-opening");
    });
    document.getElementById("season2-opening").addEventListener("click", () => {
        showOnly("season2-opening");
    });
    document.getElementById("season1-episodes").addEventListener("click", () => {
        showOnly("season1-episodes");
    });
    document.getElementById("season2-episodes").addEventListener("click", () => {
        showOnly("season2-episodes");
    });
    document.getElementById("others").addEventListener("click", () => {
        showOnly("others");
    });
    document.getElementById("all").addEventListener("click", showAll);
});

function showAll() {
    let allRange = [1, 54]
    for (let i = allRange[0]; i < allRange[1]; i++) {
        document.getElementById("location" + i).style.display = "block";
    }
    document.getElementById("numbers").innerHTML = "No. " + allRange[0] + " - No. " + allRange[1];
    let selectedButtons = document.getElementsByClassName("btn btn-dark col-4");
    for (let i = 0; i < selectedButtons.length; i++) {
        selectedButtons[i].className = "btn btn-outline-dark col-4";
    }
    document.getElementById("all").className = "btn btn-primary col-4";
    document.cookie = "group=all; max-age=604800";
}

function showOnly(group) {
    let locationRanges = {
        "season1-opening": [1, 7],
        "season2-opening": [8, 19],
        "season1-episodes": [20, 34],
        "season2-episodes": [35, 49],
        "others": [50, 54]
    };

    for (let i = locationRanges["season1-opening"][0]; i < locationRanges[group][0]; i++) {
        document.getElementById("location" + i).style.display = "none";
    }
    for (let i = locationRanges[group][0]; i <= locationRanges[group][1]; i++) {
        document.getElementById("location" + i).style.display = "block";
    }
    for (let i = locationRanges[group][1] + 1; i <= locationRanges["others"][1]; i++) {
        document.getElementById("location" + i).style.display = "none";
    }

    document.getElementById("numbers").innerHTML = "No. " + locationRanges[group][0] + " - No. " + locationRanges[group][1];

    let selectedButtons = document.getElementsByClassName("btn btn-dark col-4");
    for (let i = 0; i < selectedButtons.length; i++) {
        selectedButtons[i].className = "btn btn-outline-dark col-4";
    }
    document.getElementById("all").className = "btn btn-outline-primary col-4";
    document.getElementById(group).className = "btn btn-dark col-4";
    document.cookie = "group=" + group + "; max-age=604800";
}