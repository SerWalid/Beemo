// letIABLES AND DOM ANIMATIONS
// $("#angry-mouth-invisible").addClass("beastmode-mouth")


let btn = document.getElementById("btn")
let unleash = document.getElementById("unleash")

let hatHead = document.querySelector(".hat-head")
let mouth = document.querySelector("#mouth")
let angryMouth = document.querySelector("#angry-mouth-invisible")
// let beastmodeMouth = document.querySelector('.beastmode-mouth')

let face  = document.querySelector('.face')
let head = document.querySelector('.head')
let browLeft = document.querySelector('.brow-left')
let browRight = document.querySelector('.brow-right')
let eyeLeft = document.querySelector('.eye-left')
let eyeRight = document.querySelector('.eye-right')
let nose = document.querySelector('.nose')
let mustacheBase = document.querySelector('.mustache-base')
let starFive = document.querySelector('.star-five')
let leftArm = document.querySelector('.left-arm')
let leftElbow = document.querySelector('.left-elbow')
let leftWrist = document.querySelector('.left-wrist')
let leftFingers = document.querySelector('.left-fingers')
let bicept = document.querySelector('.bicept')
const loadingBar = document.querySelector(".loading-bar")
const powerBar = document.querySelector(".power-bar")
const counter = document.querySelector(".counter")



btn.addEventListener("click", function(e) {
    e.preventDefault;

    face.classList.remove("tilted-animated-face");
    hatHead.classList.remove("tilt-animated-hat")
    head.classList.remove("tilt-animated");
    browLeft.classList.remove("tilt-animated-brow-left")
    browRight.classList.remove("tilt-animated-brow-right")
    mouth.classList.remove("mouth-animated");
    eyeLeft.classList.remove("tilt-animated-brow-left");
    eyeRight.classList.remove("tilt-animated-brow-right");
    nose.classList.remove("tilt-animated-nose");
    mustacheBase.classList.remove("moustache-titled-animated");
    starFive.classList.remove("star-five-animated");
    leftArm.classList.remove("left-arm-animated");
   bicept.classList.remove("bicept-animated")
    leftElbow.classList.remove("left-elbow-animated");
    leftWrist.classList.remove("left-wrist-animated");
    leftFingers.classList.remove("left-fingers-animated");


    void mouth.offsetWidth;

    face.classList.add("tilted-animated-face");
    hatHead.classList.add("tilt-animated-hat");
    mouth.classList.add("mouth-animated");
    head.classList.add("tilt-animated");



    eyeLeft.classList.add("tilt-animated-brow-left");
    eyeRight.classList.add("tilt-animated-brow-right");
    nose.classList.add("tilt-animated-nose");
    mustacheBase.classList.add("moustache-titled-animated");

    browLeft.classList.add("tilt-animated-brow-left")
    browRight.classList.add("tilt-animated-brow-right")
    starFive.classList.add("star-five-animated");
    leftArm.classList.add("left-arm-animated");
    leftElbow.classList.add("left-elbow-animated");
    leftWrist.classList.add("left-wrist-animated");
    leftFingers.classList.add("left-fingers-animated");
bicept.classList.add("bicept-animated")
}, false);



let y = document.getElementById("myDIV");


unleash.addEventListener("click", () => {

    if (y.style.display === "none") {

        y.style.display = "block";


         $(".power-bar").slideUp()
         $(".loading-bar").delay(500).fadeOut(500);

         //this helps to with slideout to remove the blocky effect
         loadingBar.style.transition = "0s";

         $("#text").toggle();
         $("#btn").toggle();
        // powerBar.style.display = "none"
        // loadingBar.style.display = "none"
        $("#angry-mouth-invisible").removeClass("beastmode-mouth")
        $(".bicept").toggleClass("bicept-flexed");
        bicept.classList.remove("bicept-flexed");
        bicept.classList.remove("bicept-animated");
        $(".head").toggleClass("shake-head");
        $(".hat-head").toggleClass("shake-head");
        hatHead.classList.remove("tilt-animated-hat");
        head.classList.remove("tilt-animated");


        face.classList.remove("tilted-animated-face");
        $(".face").toggleClass("shake-head");

        $("#mouth").toggleClass("disappear");
        mouth.classList.remove("mouth-animated");
        $("#mouth").toggleClass("shake-head");

        $("#angry-mouth-invisible").toggleClass("angry-mouth-invisible");
        $(".brow-left").toggleClass("angry-brow-left");
        $(".brow-right").toggleClass("angry-brow-right");
        browLeft.classList.remove("tilt-animated-brow-left");
        browRight.classList.remove("tilt-animated-brow-right")
        $(".eye-left").toggleClass("eye-left-angry")
        $(".eye-right").toggleClass("eye-right-angry")
        eyeLeft.classList.remove("tilt-animated-brow-left");
        eyeRight.classList.remove("tilt-animated-brow-right");
        $(".mustache-base").toggleClass("shake-head")
        mustacheBase.classList.remove("moustache-titled-animated");
        $(".nose").toggleClass("shake-head")
        nose.classList.remove("tilt-animated-nose");

        leftArm.classList.remove("left-arm-animated");

        $(".left-arm").toggleClass("left-arm-flex");
        leftElbow.classList.remove("left-elbow-animated");
        $(".left-elbow").toggleClass("left-elbow-flex");
        leftWrist.classList.remove("left-wrist-animated");
        $(".left-wrist").toggleClass("left-wrist-flex");
        leftFingers.classList.remove("left-fingers-animated");
        $(".left-fingers").toggleClass("left-fingers-flex");

    } else {


        $("#btn").toggle();
        $("#text").toggle();
        // loadingBar.style.display = "block"
        $("#angry-mouth-invisible").removeClass("beastmode-mouth")
        // powerBar.style.display = "block"
        $(".power-bar").slideDown();
        $(".loading-bar").delay(500).fadeIn(500);

        $("#mouth").toggleClass("shake-head")
        $("#mouth").toggleClass("disappear");
        $("#angry-mouth-invisible").toggleClass("angry-mouth-invisible");
        $(".brow-left").toggleClass("angry-brow-left")
        $(".brow-right").toggleClass("angry-brow-right")
        $(".eye-left").toggleClass("eye-left-angry")
        $(".eye-right").toggleClass("eye-right-angry")
        $(".head").toggleClass("shake-head")
        $(".hat-head").toggleClass("shake-head")

        $(".face").toggleClass("shake-head");

        $(".mustache-base").toggleClass("shake-head")
        $(".nose").toggleClass("shake-head")
        $(".left-arm").toggleClass("left-arm-flex")
        $(".left-elbow").toggleClass("left-elbow-flex");
        $(".left-wrist").toggleClass("left-wrist-flex");
        $(".left-fingers").toggleClass("left-fingers-flex");

        $(".bicept").toggleClass("bicept-flexed");


        y.style.display = "none";
    }

})


// LOADING BAR


let x = 50;
let count = 0;
let biceptSize = 21
powerBar.addEventListener("click", () => {


    count += 1
    bicept.style.width = `${biceptSize+=1}px`
    loadingBar.style.transition = "all 1s";
    loadingBar.style.width = `${x+=10}px`;

    if (x > 150 && x < 200) {
    loadingBar.style.backgroundColor = "#00b894"

    } else if (x > 200 && x < 300) {

      $(".face").css("background-color", "#f3a683")

    } else if (x > 300) {
        loadingBar.style.backgroundColor = "#e17055"
        loadingBar.style.width = `${x+= -20}px`
        biceptSize = 50
        bicept.style.width = `${biceptSize+= -1}px`
      $("#angry-mouth-invisible").addClass("beastmode-mouth")
    }
    counter.innerHTML = count
    console.log(x, counter.value)
});


setInterval(() => {
reset()
}, 500);

function reset() {
    bicept.style.width = `${biceptSize+= -1}px`
    loadingBar.style.width = `${x+=-10}px`
    if (x < 50) {
        count=0;
        loadingBar.style.width = "50px"
        bicept.style.width = "22px"
         x = 50

    }else if (x > 50 && x < 150) {

     loadingBar.style.backgroundColor = "#00b894"

    }else if( x > 150 && x < 250) {
         loadingBar.style.backgroundColor = "#fdcb6e"

      // angryMouth.style.display = "block"
       $(".face").css("background-color", "#f9c29d")
      $("#angry-mouth-invisible").removeClass("beastmode-mouth")

    }
}


//Reset animation for the number
powerBar.addEventListener("click", function(e) {
    e.preventDefault;

    counter.classList.remove("fade-in");

    void counter.offsetWidth;

    counter.classList.add("fade-in");
}, false);


function send() {

    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", 'https://api.icndb.com/jokes/random');

        xhr.onload = () => {

            if (xhr.status === 200 && xhr.readyState === 4) {

                let jokes = JSON.parse(xhr.responseText);
                let arr = jokes.value;

                let toWrite = arr.joke
                document.getElementById('text').innerHTML = toWrite;

                resolve(xhr.response);

            } else {
                reject(Error(xhr.statusText));
            }
        };

        xhr.onerror = () => {
            reject(Error('Error fetching data.'))
        }

        xhr.send();
    });
}

 btn.addEventListener("click", (event) =>{
   event.target.textContent = "loading"

 let promise = send();

  promise.then((result) => {
  console.log('Got data!', result);
}).catch((error) => {
  console.log('Error occurred!', error, alert("error"), btn.style.display = "none"
);
}).finally(() => {

    event.target.textContent = "Make Me Laugh"
});

});
