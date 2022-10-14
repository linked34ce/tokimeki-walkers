showOnly("season1-opening");
showOnly("season2-opening");
showOnly("season1-episodes");
showOnly("season2-episodes");
showOnly("others");

document.getElementById("all").addEventListener("click", () => {
    let allRange = [1, 54]
    for (let i = allRange[0]; i < allRange[1]; i++) {
        document.getElementById("location" + i).style.display = "block";
    }
    document.getElementById("numbers").innerHTML = "No. " + allRange[0] + " - No. " + allRange[1];
});

function showOnly(group) {
    let locationRanges = {
        "season1-opening": [1, 7],
        "season2-opening": [8, 19],
        "season1-episodes": [20, 34],
        "season2-episodes": [35, 49],
        "others": [50, 54]
    };

    document.getElementById(group).addEventListener("click", () => {
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
    });
}