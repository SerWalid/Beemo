var c = $('#canvas')[0];
var ctx = c.getContext('2d');
var selectedColor = '#1abc9c';
var selectedThickness = 4;
var selectedLayer = 1;
var isPressed = false;
var prevPoint = [0, 0];

// Sets width of canvas

c.width = 1400;
c.height = 1000;

// Event listeners

$('.color').on('click', function(){
	$('.color.active').removeClass('active');
	$(this).addClass('active');

	selectedColor = $(this).data('color');
});

$('.thickness').on('click', function(){
	$('.thickness.active').removeClass('active');
	$(this).addClass('active');

	selectedThickness = $(this).data('thickness');
});

$(c).on('mousemove', function(e){
	var x = e.offsetX * 2;
	var y = e.offsetY * 2;

	if(isPressed){
		drawLine(x, y);
	}
});

$(c).on('mousedown', function(e){
	prevPoint = [(e.offsetX * 2), e.offsetY * 2];
	ctx.beginPath();
	ctx.moveTo(prevPoint[0], prevPoint[1]);
	isPressed = true;
});

$(c).on('mouseup mouseleave', function(){
	isPressed = false;
	ctx.closePath();
	saveImage();
});

$('[data-clear]').on('click', function(){
	clearCanvas();
	saveImage();
});

$('#save').on('click', function(){
	saveImage();
});

// Does what is says

function clearCanvas(){
	ctx.clearRect(0, 0, 1400, 1000);
}

// Saves image to bg

function saveImage(){
	var image = c.toDataURL('image/png');

	$('.bg-img').css({
		'background-image': 'url(' + image + ')'
	});
}

// Draws a line

function drawLine(x, y){
	ctx.lineTo(x, y);
	ctx.lineWidth = selectedThickness;
	ctx.strokeStyle = selectedColor;
	ctx.lineCap = 'round';
	ctx.lineJoin = 'round';
	ctx.stroke();

	prevPoint = [x, y];
}

// Draws the initial picture

function drawInit(){
	ctx.beginPath();
	ctx.moveTo(300, 250);
	ctx.lineTo(340, 700);

	ctx.moveTo(300, 500);
	ctx.lineTo(500, 480);

	ctx.moveTo(500, 250);
	ctx.lineTo(540, 700);

	ctx.moveTo(710, 400);
	ctx.lineTo(700, 700);

	ctx.moveTo(710, 210);
	ctx.lineTo(710, 240);

	ctx.moveTo(910, 210);
	ctx.lineTo(900, 540);

	ctx.moveTo(925, 620);
	ctx.lineTo(880, 720);

	ctx.moveTo(870, 630);
	ctx.lineTo(940, 720);

	ctx.closePath();
	ctx.lineWidth = '48';
	ctx.strokeStyle = '#2ecc71';
	ctx.lineCap = 'round';
	ctx.lineJoin = 'round';
	ctx.stroke();

	saveImage();
}

drawInit();