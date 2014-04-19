
function draw_solid_line (context, x1, y1, x2, y2) {
	context.beginPath();
	context.moveTo(x1, y1);
	context.lineTo(x2, y2);
	context.closePath();
	context.fill();
	context.stroke();
}

function draw_circle (context, x, y, radius_in_px, color) {
	context.beginPath();
	context.arc(x, y, radius_in_px, 0, 2 * Math.PI);
	context.fillStyle = color;
	context.strokeStyle = color;
	context.fill();
	context.lineWidth = 2;
	context.stroke();
}

function draw_line(context, start, end) {
	context.beginPath();
	context.moveTo(start[0], start[1]);
	context.lineTo(end[0], end[1]);
	context.stroke();
}

// Adapted from http://jsfiddle.net/SguzM/89/
function findAngle(p1, p2) {
	return Math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]));
}

function draw_arrowhead(ctx, locx, locy, angle, sizex, sizey, fill) {
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

function draw_arrow(context, start, end, fill, length_xy_x, length_y) {
	// Default values in JS:
	fill        = typeof fill        !== 'undefined' ? fill        : false;
	length_xy_x = typeof length_xy_x !== 'undefined' ? length_xy_x : 10;
	length_y    = typeof length_y    !== 'undefined' ? length_y    : length_xy_x;

	draw_line(context, start, end);
	angle = findAngle(start, end);
	draw_arrowhead(context, end[0], end[1], angle, length_xy_x, length_y, fill);
}
