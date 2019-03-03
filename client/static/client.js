async function startTimer() {
  try {
    let response = await fetch("/start", {
      method: "post",
    });
    console.warn(response);
  } catch (error) {
    console.error(error);
  }
}
