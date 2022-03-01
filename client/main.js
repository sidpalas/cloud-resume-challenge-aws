function updateViewCount() {
  viewCount = document.getElementById('viewCount');
  fetch('https://resume.devopsdirective.com/api/v1/visits').then((response) =>
    response.json().then((data) => (viewCount.innerHTML = data.view_count))
  );
}

window.onload = updateViewCount();
