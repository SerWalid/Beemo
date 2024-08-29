import gamecontrollerJs from "https://cdn.skypack.dev/gamecontroller.js@1.5.0";

function toggleClass(el, val) {
  document.getElementById(el).classList.toggle("active", val)
}

gameControl.on('connect', function(gamepad) {
  const buttonMap = {
    "button0": "b",
    "button1": "a",
    "button2": "y",
    "button3": "x",
    "button4": "l",
    "button5": "r",
    "button8": "select",
    "button9": "start"
  };

  for (const property in buttonMap) {
    gamepad.on(property, function() { toggleClass(buttonMap[property], true) })
           .after(property, function() { toggleClass(buttonMap[property], false) });
  }
});






















