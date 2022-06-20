document.getElementById("checkin-with-photo").addEventListener("click", () => {
    document.getElementById("message-with-photo").style.display = "block";
    document.getElementById("confirm-buttons-with-photo").style.display = "block";
    document.getElementById("uploadable").style.display = "none";
    document.getElementById("checkin-with-photo").style.display = "none";
    document.getElementById("close-with-photo").style.display = "none";
});

function checkin(withPhoto, locationId, targetLatitude, targetLongitude, visitCount, lastVisit) {
    const LIMIT = 60000; // 1日: 86400000
    const JST = 32400000;
    const THRESHOLD = 0.005;

    let classSuffix = "";

    if (withPhoto) {
        classSuffix = "-with-photo";
    } else {
        classSuffix = "-without-photo";
    }

    document.getElementById("message" + classSuffix).innerHTML = "チェックイン中…";
    document.getElementById("confirm-buttons" + classSuffix).style.display = "none";
    document.getElementById("close" + classSuffix).style.display = "block";

    navigator.geolocation.getCurrentPosition(pos => {
        let visitDate = new Date(lastVisit);
        document.getElementById("close" + classSuffix).className = "btn btn-secondary";
        if (Math.abs(targetLatitude - pos.coords.latitude) >= THRESHOLD || Math.abs(targetLongitude - pos.coords.longitude) >= THRESHOLD) {
            document.getElementById("message" + classSuffix).innerHTML = "<span class='text-danger'>*</span> チェックインに失敗しました<br>&nbsp;&nbsp;&nbsp;(距離が遠すぎます)";
        } else if (Date.now() - visitDate.getTime() - JST < LIMIT && visitCount > 0) {
            document.getElementById("message" + classSuffix).innerHTML = "<span class='text-danger'>*</span> チェックインに失敗しました<br>&nbsp;&nbsp;&nbsp;(前回のチェックインから24時間が経過していません)";
        } else {
            document.getElementById("message" + classSuffix).innerHTML = "<span class='text-success'>*</span> チェックインに成功しました";
            document.getElementById("close" + classSuffix).setAttribute("onclick", "reload(" + withPhoto + ", " + locationId + ")");
        }
    });
}

function reload(withPhoto, locationId) {
    if (withPhoto) {
        document.getElementById("upload-form").submit();
    } else {
        location.href = "/checkinWithoutPhoto/" + locationId + "/";
    }
}

let fileInput = document.getElementById("upload-photo");

fileInput.addEventListener("change", () => {
    const MB = 2 ** 20;
    const LIMIT = 10 * MB;
    let file = fileInput.files[0];

    document.getElementById("message-with-photo").style.display = "none";
    document.getElementById("confirm-buttons-with-photo").style.display = "none";
    document.getElementById("uploadable").style.display = "block";
    document.getElementById("checkin-with-photo").style.display = "block";
    document.getElementById("close-with-photo").style.display = "block";

    if (file.size > LIMIT) {
        document.getElementById("checkin-with-photo").style.display = "none";
        document.getElementById("uploadable").innerHTML = "<span class='text-danger'>*</span> ファイルサイズが大きすぎます<br>&nbsp;&nbsp;&nbsp;(10MB以下にしてください)";
        document.getElementById("preview").innerHTML = "";
    } else {
        document.getElementById("checkin-with-photo").style.display = "block";
        document.getElementById("uploadable").innerHTML = "<span class='text-success'>*</span> この画像はアップロード可能です";
        previewFile(file);
    }
});

function previewFile(file) {
    let preview = document.getElementById("preview");
    let reader = new FileReader();

    reader.onload = function(e) {
        preview.innerHTML = "";
        const imageUrl = e.target.result;
        preview.innerHTML = "<img src=" + imageUrl + " style='width: 100%;'></img>";
    }

    reader.readAsDataURL(file);
}