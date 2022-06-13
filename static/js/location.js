function checkin(withPhoto, locationId, targetLatitude, targetLongitude, visitCount, lastVisit) {
    const LIMIT = 60000; // 1日: 86400000
    const JST = 32400000;
    const THRESHOLD = 0.005;
    navigator.geolocation.getCurrentPosition(pos => {
        let visitDate = new Date(lastVisit);
        if (Math.abs(targetLatitude - pos.coords.latitude) >= THRESHOLD || Math.abs(targetLongitude - pos.coords.longitude) >= THRESHOLD) {
            document.getElementById("result").innerHTML = "<span class='text-danger'>*</span> チェックインに失敗しました<br>&nbsp;&nbsp;&nbsp;(距離が遠すぎます)";
            document.getElementById("close").innerHTML = "<button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>とじる</button>";
        } else if (Date.now() - visitDate.getTime() - JST < LIMIT && visitCount > 0) {
            document.getElementById("result").innerHTML = "<span class='text-danger'>*</span> チェックインに失敗しました<br>&nbsp;&nbsp;&nbsp;(前回のチェックインから24時間が経過していません)";
            document.getElementById("close").innerHTML = "<button type='button' class='btn btn-secondary' data-bs-dismiss='modal'>とじる</button>";
        } else {
            document.getElementById("result").innerHTML = "<span class='text-success'>*</span> チェックインに成功しました";
            document.getElementById("close").innerHTML = "<button type='button' class='btn btn-secondary' data-bs-dismiss='modal' onclick='reload(" + withPhoto + ", " + locationId + ")'>とじる</button>";
        }
    });
}

function reload(withPhoto, locationId) {
    location.href = "/checkin/" + locationId + "/" + withPhoto;
}