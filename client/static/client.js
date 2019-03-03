async function startTimer() {
  try {
    let response = await fetch("/start", {
      method: "post",
    });
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", function() {
  setInterval(async function() {
    let response, info;
    try {
      response = await fetch("/info");
      info = await response.json();
    } catch (error) {
      console.error(error);
    }
    // Do all the state updating.
    document.getElementById("time").textContent = `${info.elapsed}`;
  }, 500);
});
