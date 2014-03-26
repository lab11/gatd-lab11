
function draw_line(context, start, end) {
	context.beginPath();
	//console.log(start);
	//console.log(end);
	context.moveTo(start[0], start[1]);
	context.lineTo(end[0], end[1]);
	context.stroke();
}

// Adapted from http://jsfiddle.net/SguzM/89/
function findAngle(p1, p2) {
	return Math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]));
}

function drawArrowhead(ctx, locx, locy, angle, sizex, sizey, fill) {
	var hx = sizex / 2;
	var hy = sizey / 2;
	ctx.translate((locx ), (locy));
	ctx.rotate(angle);
	ctx.translate(-hx,-hy);

	if (fill) {
		ctx.beginPath();
		ctx.moveTo(0,0);
		ctx.lineTo(0,1*sizey);
		ctx.lineTo(1*sizex,1*hy);
		ctx.closePath();
		ctx.fill();
	} else {
		ctx.beginPath();
		ctx.moveTo(0,1*sizey);
		ctx.lineTo(1*sizex,1*hy);
		ctx.moveTo(0,0);
		ctx.lineTo(1*sizex,1*hy);
		ctx.stroke();
	}

	ctx.translate(hx,hy);
	ctx.rotate(-angle);
	ctx.translate(-locx,-locy);
}

function draw_arrow(context, start, end) {
	draw_line(context, start, end);
	angle = findAngle(start, end);
	//console.log("angle: " + angle);
	drawArrowhead(context, end[0], end[1], angle, 10, 10, false);
}
