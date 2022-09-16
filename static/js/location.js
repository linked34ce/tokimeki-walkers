document.getElementById("checkin-with-photo").addEventListener("click", () => {
    document.getElementById("message-with-photo").style.display = "block";
    document.getElementById("confirm-buttons-with-photo").style.display = "block";
    document.getElementById("uploadable").style.display = "none";
    document.getElementById("checkin-with-photo").style.display = "none";
    document.getElementById("close-with-photo").style.display = "none";
});

function checkin(withPhoto, locationId, targetLatitude, targetLongitude, visitCount, lastVisit) {
    const LIMIT = 60000; // 1日: 86400000 1分: 60000
    const JST = 32400000;
    const THRESHOLD = 1000000; // 実際は50m テスト用: 100000m

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
        let distance = hubenyFormula(pos.coords.latitude, pos.coords.longitude, targetLatitude, targetLongitude);
        let visitDate = new Date(lastVisit.replace(/-/g, "/"));
        document.getElementById("close" + classSuffix).className = "btn btn-secondary";
        if (distance > THRESHOLD) {
            document.getElementById("message" + classSuffix).innerHTML = "<span class='text-danger'>*</span> チェックインに失敗しました<br>&nbsp;&nbsp;&nbsp;(距離が遠すぎます; " + Math.round(distance).toLocaleString() + "m)";
            document.getElementById("close" + classSuffix).setAttribute("onclick", "window.location.reload()");
        } else if (Date.now() - visitDate.getTime() - JST < LIMIT && visitCount > 0) {
            document.getElementById("message" + classSuffix).innerHTML = "<span class='text-danger'>*</span> チェックインに失敗しました<br>&nbsp;&nbsp;&nbsp;(前回のチェックインから24時間が経過していません)";
            document.getElementById("close" + classSuffix).setAttribute("onclick", "window.location.reload()");
        } else {
            document.getElementById("message" + classSuffix).innerHTML = "<span class='text-success'>*</span> チェックインに成功しました";
            document.getElementById("close" + classSuffix).setAttribute("onclick", "reload(" + withPhoto + ", " + locationId + ")");
        }
    }, err => {
        let err_msg = "位置情報の取得に失敗しました:\n";
        switch (err.code) {
            case 1:
                err_msg += "位置情報サービス (GPS) の利用が許可されていません";
                break;
            case 2:
                err_msg = "お使いの端末の位置を判定することができません";
                break;
            case 3:
                err_msg = "位置情報の取得に時間がかかっています";
                break;
        }
        window.alert(err_msg);
        window.location.reload();
    }, {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    });
}

function hubenyFormula(latitude1, longitude1, latitude2, longitude2) {
    const SEMI_MAJOR_AXIS = 6378137;
    const SEMI_MINOR_AXIS = 6356752.314245;
    let eccentricitySquared = (SEMI_MAJOR_AXIS ** 2 - SEMI_MINOR_AXIS ** 2) / SEMI_MAJOR_AXIS ** 2;

    let radianLatitude1 = radian(latitude1);
    let radianLatitude2 = radian(latitude2);
    let radianLongitude1 = radian(longitude1);
    let radianLongitude2 = radian(longitude2);

    let latitudeDelta = radianLatitude2 - radianLatitude1;
    let longitudeDelta = radianLongitude2 - radianLongitude1;
    let latitudeAverage = (radianLatitude1 + radianLatitude2) / 2;

    let denominator = Math.sqrt((1 - eccentricitySquared * Math.sin(latitudeAverage) ** 2));
    let radiusOfCurvatureInTheMeridian = (SEMI_MAJOR_AXIS * (1 - eccentricitySquared)) / denominator ** 3;
    let radiusOfCurvatureInThePrimeVertical = SEMI_MAJOR_AXIS / denominator;

    let distance = Math.sqrt((latitudeDelta * radiusOfCurvatureInTheMeridian) ** 2 + (longitudeDelta * radiusOfCurvatureInThePrimeVertical * Math.cos(latitudeAverage)) ** 2);

    return distance;
}

function radian(degree) {
    return degree * Math.PI / 180;
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