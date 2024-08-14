console.clear();

var vid = document.getElementById('video');
var vid_width = vid.width;
var vid_height = vid.height;
var overlay = document.getElementById('overlay');
var overlayCC = overlay.getContext('2d');

var mouthClip = document.getElementById('mouth-clip');
var mouthOutline = document.getElementById('mouth-outline');
var eyeRInner = document.querySelector('#eye-r .inner'), eyeROuter = document.querySelector('#eye-r .outer');
var eyeLInner = document.querySelector('#eye-l .inner'), eyeLOuter = document.querySelector('#eye-l .outer');
var eyebrowL = document.getElementById('eyebrow-l'), eyebrowR = document.getElementById('eyebrow-r');
var earL = document.getElementById('ear-l'), earR = document.getElementById('ear-r');
var headLower = document.getElementById('head-lower'), faceLower = document.getElementById('face-lower');
var nose = document.getElementById('nose');
var teethTop = document.getElementById('teeth-top'), teethBot = document.getElementById('teeth-bot');

var mouthNormal = "M227,205.7h-54 c-1.1,0-2-0.8-2-2s0.9-2,2-2h54c1.1,0,2,0.9,2,2S228.1,205.7,227,205.7z";
var mouthHappy = "M197.8,218.5 c-30.5-0.8-39.8-16.6-42.6-26.2c-1-3.3,2-6.4,5.3-5.7c26.4,5.6,52.7,5.6,79.1,0c3.3-0.7,6.2,2.4,5.3,5.7 c-2.8,9.6-11.9,25.4-42.4,26.2C201.7,218.5,198.5,218.5,197.8,218.5z";
var mouthSurprised = "M192,204 c0-4.1,3.4-7.5,7.5-7.5h1c4.1,0,7.5,3.4,7.5,7.5c0,4.1-3.4,7.5-7.5,7.5h-1C195.4,211.5,192,208.1,192,204z";
var mouthSad = "M227.3,208.1 c-15.5-13.9-39.1-13.9-54.6,0c-0.9,0.8-2.3,1-3.1,0.2c-0.8-0.8-0.6-2.2,0.4-3.2c17-15.2,42.9-15.2,59.9,0c1.1,0.9,1.2,2.4,0.4,3.2 C229.6,209.1,228.3,208.9,227.3,208.1z";
var mouthAngry = "M217,211.9h-34 c-7.2,0-13-5.8-13-13c0-7.2,5.8-13,13-13h34c7.2,0,13,6.1,13,13S224.2,211.9,217,211.9z";

/********** check and set up video/webcam **********/

function enablestart() {
	var startbutton = document.getElementById('startbutton');
	startbutton.value = "start";
	startbutton.disabled = null;
}

function adjustVideoProportions() {
	// resize overlay and video if proportions are different
	// keep same height, just change width
	var proportion = vid.videoWidth/vid.videoHeight;
	vid_width = Math.round(vid_height * proportion);
	vid.width = vid_width;
	overlay.width = vid_width;
}

function gumSuccess( stream ) {
	// add camera stream if getUserMedia succeeded
	if ("srcObject" in vid) {
		vid.srcObject = stream;
	} else {
		vid.src = (window.URL && window.URL.createObjectURL(stream));
	}
	vid.onloadedmetadata = function() {
		adjustVideoProportions();
		vid.play();
	}
	vid.onresize = function() {
		adjustVideoProportions();
		if (trackingStarted) {
			ctrack.stop();
			ctrack.reset();
			ctrack.start(vid);
		}
	}
}

function gumFail() {
	alert("There was some problem trying to fetch video from your webcam. If you have a webcam, please make sure to accept when the browser asks for access to your webcam.");
}

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.URL = window.URL || window.webkitURL || window.msURL || window.mozURL;

// check for camerasupport
if (navigator.mediaDevices) {
	navigator.mediaDevices.getUserMedia({video : true}).then(gumSuccess).catch(gumFail);
} else if (navigator.getUserMedia) {
	navigator.getUserMedia({video : true}, gumSuccess, gumFail);
} else {
	alert("This demo depends on getUserMedia, which your browser does not seem to support. :(");
}

vid.addEventListener('canplay', enablestart, false);


/*********** setup of emotion detection *************/
// set eigenvector 9 and 11 to not be regularized. This is to better detect motion of the eyebrows
pModel.shapeModel.nonRegularizedVectors.push(9);
pModel.shapeModel.nonRegularizedVectors.push(11);

var ctrack = new clm.tracker({useWebGL : true});
ctrack.init(pModel);
var trackingStarted = false;

function startVideo() {
	// start video
	vid.play();
	// start tracking
	ctrack.start(vid);
	trackingStarted = true;
	// start loop to draw face
	drawLoop();
}

function drawLoop() {
	window.requestAnimationFrame(drawLoop);
	overlayCC.clearRect(0, 0, vid_width, vid_height);
	if (ctrack.getCurrentPosition()) {
		ctrack.draw(overlay);
	}
	var cp = ctrack.getCurrentParameters();

	var er = ec.meanPredict(cp);
	if (er) {
		var winner = {value: 0, emotion: ""};
		for (var i = 0;i < er.length;i++) {
			if (er[i].value > 0.5) {
				if(winner.value < er[i].value) {
					winner = er[i];
				} else {
				}
				document.getElementById('icon'+(i+1)).style.visibility = 'visible';
			} else {
				document.getElementById('icon'+(i+1)).style.visibility = 'hidden';
			}
		}
		animateFace(winner.emotion);
	}
}

function animateFace(emotion) {
	switch(emotion) {
		case "happy":
			//console.log("happy");
			TweenMax.to([mouthClip, mouthOutline], .25, {morphSVG: mouthHappy});
			TweenMax.to([eyeLOuter, eyeROuter], .25, {y: -8, scaleY: 1.25});
			TweenMax.to([eyeLInner, eyeRInner], .25, {y: -5, scaleY: 1.23});
			TweenMax.to(eyebrowL, .25, {rotation: "-20deg", x: -6, y: -10, scaleX: 1});
			TweenMax.to(eyebrowR, .25, {rotation: "20deg", x: 6, y: -10, scaleX: 1});
			TweenMax.to(earL, .25, {x: -3, y: -10});
			TweenMax.to(earR, .25, {x: 3, y: -10});
			TweenMax.to(headLower, .25, {y: -5, scaleX: 1.09, scaleY: .9});
			TweenMax.to(faceLower, .25, {y: -5, scaleX: 1.125, scaleY: .88});
			TweenMax.to(nose, .25, {y: -3});
			TweenMax.to(teethTop, .25, {y: 0});
			TweenMax.to(teethBot, .25, {y: 0});
			break;
		case "surprised":
			//console.log("surprised");
			TweenMax.to([mouthClip, mouthOutline], .25, {morphSVG: mouthSurprised});
			TweenMax.to([eyeLOuter, eyeROuter], .25, {y: -13, scaleY: 1.38});
			TweenMax.to([eyeLInner, eyeRInner], .25, {y: -8, scaleY: 1.36});
			TweenMax.to(eyebrowL, .25, {rotation: "0deg", x: 0, y: -17, scaleX: 1});
			TweenMax.to(eyebrowR, .25, {rotation: "0deg", x: 0, y: -17, scaleX: 1});
			TweenMax.to(earL, .25, {x: 0, y: 0});
			TweenMax.to(earR, .25, {x: 0, y: 0});
			TweenMax.to(headLower, .25, {y: 4, scaleX: .89, scaleY: 1.05});
			TweenMax.to(faceLower, .25, {y: 4, scaleX: .875, scaleY: 1.06});
			TweenMax.to(nose, .25, {y: -2});
			TweenMax.to(teethTop, .25, {y: -3});
			TweenMax.to(teethBot, .25, {y: 3});
			break;
		case "sad":
			//console.log("sad");
			TweenMax.to([mouthClip, mouthOutline], .25, {morphSVG: mouthSad});
			TweenMax.to([eyeLOuter, eyeROuter], .25, {y: 6, scaleY: .88});
			TweenMax.to([eyeLInner, eyeRInner], .25, {y: 5, scaleY: .85});
			TweenMax.to(eyebrowL, .25, {rotation: "0deg", x: 0, y: 8, scaleX: 1});
			TweenMax.to(eyebrowR, .25, {rotation: "0deg", x: 0, y: 8, scaleX: 1});
			TweenMax.to(earL, .25, {x: 0, y: 0});
			TweenMax.to(earR, .25, {x: 0, y: 0});
			TweenMax.to(headLower, .25, {y: 2, scaleX: 1, scaleY: 1});
			TweenMax.to(faceLower, .25, {y: 2, scaleX: 1, scaleY: 1});
			TweenMax.to(nose, .25, {y: 1});
			TweenMax.to(teethTop, .25, {y: -6});
			TweenMax.to(teethBot, .25, {y: 0});
			break;
		case "angry":
			//console.log("angry");
			TweenMax.to([mouthClip, mouthOutline], .25, {morphSVG: mouthAngry});
			TweenMax.to([eyeLOuter, eyeROuter], .25, {y: 12, scaleY: .67});
			TweenMax.to([eyeLInner, eyeRInner], .25, {y: 5, scaleY: .85});
			TweenMax.to(eyebrowL, .25, {rotation: "27deg", x: 8, y: 15, scaleX: 1.5});
			TweenMax.to(eyebrowR, .25, {rotation: "-27deg", x: -8, y: 15, scaleX: 1.5});
			TweenMax.to(earL, .25, {x: -6, y: -6});
			TweenMax.to(earR, .25, {x: 6, y: -6});
			TweenMax.to(headLower, .25, {y: -2, scaleX: 1.07, scaleY: .95});
			TweenMax.to(faceLower, .25, {y: -2, scaleX: 1.09, scaleY: .92});
			TweenMax.to(nose, .25, {y: -4});
			TweenMax.to(teethTop, .25, {y: -1});
			TweenMax.to(teethBot, .25, {y: -9});
			break;
		default:
			//console.log("normal");
			TweenMax.to([mouthClip, mouthOutline], .25, {morphSVG: mouthNormal});
			TweenMax.to([eyeLOuter, eyeROuter], .25, {y: 0, scaleY: 1});
			TweenMax.to([eyeLInner, eyeRInner], .25, {y: 0, scaleY: 1});
			TweenMax.to([eyebrowL, eyebrowR], .25, {x: 0, y: 0, rotation: "0deg", scaleX: 1});
			TweenMax.to([earL, earR], .25, {x: 0, y: 0});
			TweenMax.to([headLower, faceLower], .25, {y: 0, scaleX: 1, scaleY: 1});
			TweenMax.to(nose, .25, {y: 0});
			TweenMax.to([teethBot, teethTop], .25, {y: 0});
	}
}

delete emotionModel['disgusted'];
delete emotionModel['fear'];
var ec = new emotionClassifier();
ec.init(emotionModel);
var emotionData = ec.getBlank();

TweenMax.set([eyeLOuter, eyeROuter], {transformOrigin: "center top"});
TweenMax.set([eyeLInner, eyeRInner], {transformOrigin: "center top"});
TweenMax.set(eyebrowL, {svgOrigin: "159px 105px"});
TweenMax.set(eyebrowR, {svgOrigin: "241px 105px"});
TweenMax.set([headLower, faceLower], {transformOrigin: "50% 50%"});
TweenLite.defaultEase = Quad.easeOut;

var tl = new TimelineMax({paused: true, repeat: -1, yoyo: true});
tl.addCallback(function() {
	animateFace("surprised");
}, "0");
tl.addCallback(function() {
	animateFace("normal");
}, "1");
//tl.play();



/******** stats ********/
stats = new Stats();
stats.domElement.style.position = 'absolute';
stats.domElement.style.top = '0px';
stats.domElement.style.right = '0px';
document.getElementById('container').appendChild( stats.domElement );

// update stats on every iteration
document.addEventListener('clmtrackrIteration', function(event) {
	stats.update();
}, false);













