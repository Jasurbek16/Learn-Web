console.log("Working");

let theme = localStorage.getItem("theme");

if (theme == null) {
  setTheme("light");
} else {
  setTheme(theme);
}

let themeDots = document.getElementsByClassName("theme-dot");

for (var i = 0; themeDots.length > i; i++) {
  themeDots[i].addEventListener("click", function () {
    let mode = this.dataset.mode;
    console.log("Option clicked", mode);
    setTheme(mode);
  });
}

function setTheme(mode) {
  if (mode == "light") {
    document.getElementById("theme-style").href = "staticfiles/styles/app.css";
  }

  if (mode == "blue") {
    document.getElementById("theme-style").href = "staticfiles/styles/blue.css";
  }

  if (mode == "purple") {
    document.getElementById("theme-style").href =
      "staticfiles/styles/purple.css";
  }

  if (mode == "green") {
    document.getElementById("theme-style").href =
      "staticfiles/styles/green.css";
  }

  localStorage.setItem("theme", mode);
}
