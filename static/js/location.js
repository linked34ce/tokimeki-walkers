function checkin(with_photo, location_id, currentLatitude, currentLongitude) {
    let threshold = 0.005
    navigator.geolocation.getCurrentPosition(pos => {
        if (Math.abs(currentLatitude - pos.coords.latitude) < threshold && Math.abs(currentLongitude - pos.coords.longitude) < threshold) {
            location.href = "/checkin/" + location_id + "/" + with_photo;
        } else {
            document.getElementById("result").innerHTML = "<span class='text-danger'>*</span> チェックインに失敗しました (距離が遠すぎます)";
        }
    });
}