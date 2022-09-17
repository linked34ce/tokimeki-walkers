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

    document.getElementById("footer").style.display = "none";
    document.getElementById("uploadable").style.display = "block";
    document.getElementById("checkin-question").style.display = "none";

    if (file.size > LIMIT) {
        document.getElementById("footer").style.display = "none";
        document.getElementById("uploadable").innerHTML = "<span class='text-danger'>*</span> ファイルサイズが大きすぎます<br>&nbsp;&nbsp;&nbsp;(10MB以下にしてください)";
        document.getElementById("checkin-question").style.display = "none";
        document.getElementById("preview").innerHTML = "";
    } else {
        document.getElementById("footer").style.display = "block";
        document.getElementById("uploadable").innerHTML = "<span class='text-success'>*</span> この画像はアップロード可能です";
        document.getElementById("checkin-question").style.display = "block";
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