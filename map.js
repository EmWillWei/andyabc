function initMap() {

	const lats = [40.55, 40.65]
  const lons = [112.65001, 112.75]
  const myLatLng = { lat: lats[parseInt(lats.length / 2)], lng: lons[parseInt(lons.length / 2)] };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 10,
    center: myLatLng,    
  });
  
  lats.forEach((lat, i) => {lons.forEach((lng, j) =>    new google.maps.Marker({
    position: {lat, lng},
    map,
    title: ` ${j}   ${i}  `,
  })
    )})
  
   
  
}
