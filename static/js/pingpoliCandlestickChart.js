

/*
A single-file JavaScript class to draw candlestick charts.
Use at your own risk.

Copyright 2022 Christian Behler

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

https://twitter.com/pingpoli
https://pingpoli.de
*/
function pingpoliCandlestick( timestamp , open , close , high , low )
{
    this.timestamp = parseInt(timestamp);
    this.open = parseFloat(open);
    this.close = parseFloat(close);
    this.high = parseFloat(high);
    this.low = parseFloat(low);
}

pingpoliCandlestick.prototype.update = function( open , close , high , low )
{
    this.open = parseFloat(open);
    this.close = parseFloat(close);
    this.high = parseFloat(high);
    this.low = parseFloat(low);
}



function pingpoliCandlestickChart( canvasElementID )
{
    this.canvas = document.getElementById( canvasElementID );
	this.width = parseInt( this.canvas.width );
	this.height = parseInt( this.canvas.height );
	this.context = this.canvas.getContext( "2d" );

    this.canvas.addEventListener( "mousemove" , ( e ) => {
        this.mouseMove( e );
    } );
    this.canvas.addEventListener( "mouseout" , ( e ) => {
        this.mouseOut( e );
    } );
    this.canvas.addEventListener( "wheel" , ( e) => {
        this.scroll( e );
        e.preventDefault();
    } );

    this.canvas.style.backgroundColor = "#252525";
    this.context.font = '12px sans-serif';
    this.gridColor = "#444444";
    this.gridTextColor = "#aaaaaa";
    this.mouseHoverBackgroundColor = "#eeeeee";
    this.mouseHoverTextColor = "#000000";
    this.greenColor = "#00cc00";
    this.redColor = "#cc0000";
    this.greenHoverColor = "#00ff00";
    this.redHoverColor = "#ff0000";

    this.context.lineWidth = 1;
    this.candleWidth = 5;

    this.marginLeft = 10;
    this.marginRight = 100;
    this.marginTop = 10;
    this.marginBottom = 30;

    this.yStart = 0;
    this.yEnd = 0;
    this.yRange = 0;
    this.yPixelRange = this.height-this.marginTop-this.marginBottom;

    this.xStart = 0;
    this.xEnd = 0;
    this.xRange = 0;
    this.xPixelRange = this.width-this.marginLeft-this.marginRight;

    // these are only approximations, the grid will be divided in a way so the numbers are nice
    this.xGridCells = 16;
    this.yGridCells = 16;

    this.b_drawMouseOverlay = false;
    this.mousePosition = { x: 0 , y: 0 };
    this.xMouseHover = 0;
    this.yMouseHover = 0;
    this.hoveredCandlestickID = 0;

    // when zooming, just start at a later candlestick in the array
    this.zoomStartID = 0;

    this.candlesticks = [];

    this.technicalIndicators = [];
}



pingpoliCandlestickChart.prototype.clear = function()
{
    this.candlesticks = [];
    this.draw();
}



pingpoliCandlestickChart.prototype.addCandlestick = function( candlestick )
{
    this.candlesticks.push( candlestick );
    for ( var i = 0 ; i < this.technicalIndicators.length ; ++i )
    {
        this.technicalIndicators[i].onAddCandlestick( this , this.candlesticks.length-1 );
    }
}



pingpoliCandlestickChart.prototype.updateCandlestick = function( candlestickID , open , close , high , low )
{
    if ( candlestickID >= 0 && candlestickID < this.candlesticks.length )
    {
        this.candlesticks[candlestickID].update( open , close , high , low );
        for ( var i = 0 ; i < this.technicalIndicators.length ; ++i )
        {
            this.technicalIndicators[i].onUpdateCandlestick( this , candlestickID );
        }
    }
}



pingpoliCandlestickChart.prototype.mouseMove = function( e )
{
    var getMousePos = ( e ) =>
    {
        var rect = this.canvas.getBoundingClientRect();
        return { x: e.clientX-rect.left , y: e.clientY-rect.top };
    }
    this.mousePosition = getMousePos( e );
    this.mousePosition.x += this.candleWidth/2;
    this.b_drawMouseOverlay = true;
    if ( this.mousePosition.x < this.marginLeft ) this.b_drawMouseOverlay = false;
    if ( this.mousePosition.x > this.width-this.marginRight+this.candleWidth ) this.b_drawMouseOverlay = false;
    if ( this.mousePosition.y > this.height-this.marginBottom ) this.b_drawMouseOverlay = false;
    if ( this.b_drawMouseOverlay )
    {
        this.yMouseHover = this.yToValueCoords( this.mousePosition.y );
        this.xMouseHover = this.xToValueCoords( this.mousePosition.x );
        // snap to candlesticks
        var candlestickDelta = this.candlesticks[1].timestamp-this.candlesticks[0].timestamp;
        this.hoveredCandlestickID = Math.floor((this.xMouseHover-this.candlesticks[0].timestamp)/candlestickDelta);
        this.xMouseHover = Math.floor(this.xMouseHover/candlestickDelta)*candlestickDelta;
        this.mousePosition.x = this.xToPixelCoords( this.xMouseHover );
        this.draw();
    }
    else this.draw();
}



pingpoliCandlestickChart.prototype.mouseOut = function( e )
{
    this.b_drawMouseOverlay = false;
    this.draw();
}



pingpoliCandlestickChart.prototype.scroll = function( e )
{
    if ( e.deltaY < 0 )
    {
        this.zoomStartID += 10;
        if ( this.zoomStartID > this.candlesticks.length-50 ) this.zoomStartID = this.candlesticks.length-50;
    }
    else
    {
        this.zoomStartID -= 10;
        if ( this.zoomStartID < 0 ) this.zoomStartID = 0;
    }
    this.draw();
}



pingpoliCandlestickChart.prototype.draw = function()
{
	// clear background
	this.context.clearRect( 0 , 0 , this.width , this.height );

    this.calculateYRange();
    this.calculateXRange();

    this.drawGrid();

    this.candleWidth = this.xPixelRange/(this.candlesticks.length-this.zoomStartID);
    this.candleWidth--;
    if ( this.candleWidth%2 == 0 ) this.candleWidth--;

    for ( var i = this.zoomStartID ; i < this.candlesticks.length ; ++i )
    {
        var color = ( this.candlesticks[i].close > this.candlesticks[i].open ) ? this.greenColor : this.redColor;

        if ( i == this.hoveredCandlestickID )
        {
            if ( color == this.greenColor ) color = this.greenHoverColor;
            else if ( color == this.redColor ) color = this.redHoverColor;
        }

        // draw the wick
        this.drawLine( this.xToPixelCoords( this.candlesticks[i].timestamp ) , this.yToPixelCoords( this.candlesticks[i].low ) , this.xToPixelCoords( this.candlesticks[i].timestamp ) , this.yToPixelCoords( this.candlesticks[i].high ) , color );

        // draw the candle
        this.fillRect( this.xToPixelCoords( this.candlesticks[i].timestamp )-Math.floor( this.candleWidth/2 ) , this.yToPixelCoords( this.candlesticks[i].open ) , this.candleWidth , this.yToPixelCoords( this.candlesticks[i].close ) - this.yToPixelCoords( this.candlesticks[i].open ) , color );
    }

    // draw technical indicators
    for ( var i = 0 ; i < this.technicalIndicators.length ; ++i )
    {
        this.technicalIndicators[i].draw( this );
    }

    // draw mouse hover
    if ( this.b_drawMouseOverlay )
    {
        // price line
        this.context.setLineDash( [5,5] );
        this.drawLine( 0 , this.mousePosition.y , this.width , this.mousePosition.y , this.mouseHoverBackgroundColor );
        this.context.setLineDash( [] );
        var str = this.roundPriceValue( this.yMouseHover );
        var textWidth = this.context.measureText( str ).width;
        this.fillRect( this.width-70 , this.mousePosition.y-10 , 70 , 20 , this.mouseHoverBackgroundColor );
        this.context.fillStyle = this.mouseHoverTextColor;
        this.context.fillText( str , this.width-textWidth-5 , this.mousePosition.y+5 );

        // time line
        this.context.setLineDash( [5,5] );
        this.drawLine( this.mousePosition.x , 0 , this.mousePosition.x , this.height , this.mouseHoverBackgroundColor );
        this.context.setLineDash( [] );
        str = this.formatDate( new Date( this.xMouseHover ) );
        textWidth = this.context.measureText( str ).width;
        this.fillRect( this.mousePosition.x-textWidth/2-5 , this.height-20 , textWidth+10 , 20 , this.mouseHoverBackgroundColor );
        this.context.fillStyle = this.mouseHoverTextColor;
        this.context.fillText( str , this.mousePosition.x-textWidth/2 , this.height-5 );

        // data
        var yPos = this.mousePosition.y-95;
        if ( yPos < 0 ) yPos = this.mousePosition.y+15;

        this.fillRect( this.mousePosition.x+15 , yPos , 100 , 80 , this.mouseHoverBackgroundColor );
        var color = ( this.candlesticks[this.hoveredCandlestickID].close > this.candlesticks[this.hoveredCandlestickID].open ) ? this.greenColor : this.redColor;
        this.fillRect( this.mousePosition.x+15 , yPos , 10 , 80 , color );
        this.context.lineWidth = 2;
        this.drawRect( this.mousePosition.x+15 , yPos , 100 , 80 , color );
        this.context.lineWidth = 1;

        this.context.fillStyle = this.mouseHoverTextColor;
        this.context.fillText( "O: "+this.candlesticks[this.hoveredCandlestickID].open , this.mousePosition.x+30 , yPos+15 );
        this.context.fillText( "C: "+this.candlesticks[this.hoveredCandlestickID].close , this.mousePosition.x+30 , yPos+35 );
        this.context.fillText( "H: "+this.candlesticks[this.hoveredCandlestickID].high , this.mousePosition.x+30 , yPos+55 );
        this.context.fillText( "L: "+this.candlesticks[this.hoveredCandlestickID].low , this.mousePosition.x+30 , yPos+75 );
    }
}



pingpoliCandlestickChart.prototype.drawGrid = function()
{
    // roughly divide the yRange into cells
    var yGridSize = (this.yRange)/this.yGridCells;

    // try to find a nice number to round to
    var niceNumber = Math.pow( 10 , Math.ceil( Math.log10( yGridSize ) ) );
    if ( yGridSize < 0.25 * niceNumber ) niceNumber = 0.25 * niceNumber;
    else if ( yGridSize < 0.5 * niceNumber ) niceNumber = 0.5 * niceNumber;

    // find next largest nice number above yStart
    var yStartRoundNumber = Math.ceil( this.yStart/niceNumber ) * niceNumber;
    // find next lowest nice number below yEnd
    var yEndRoundNumber = Math.floor( this.yEnd/niceNumber ) * niceNumber;

    for ( var y = yStartRoundNumber ; y <= yEndRoundNumber ; y += niceNumber )
    {
        this.drawLine( 0 , this.yToPixelCoords( y ) , this.width , this.yToPixelCoords( y ) , this.gridColor );
        var textWidth = this.context.measureText( this.roundPriceValue( y ) ).width;
        this.context.fillStyle = this.gridTextColor;
        this.context.fillText( this.roundPriceValue( y ) , this.width-textWidth-5 , this.yToPixelCoords( y )-5 );
    }

    // roughly divide the xRange into cells
    var xGridSize = (this.xRange)/this.xGridCells;

    // try to find a nice number to round to
    niceNumber = Math.pow( 10 , Math.ceil( Math.log10( xGridSize ) ) );
    if ( xGridSize < 0.25 * niceNumber ) niceNumber = 0.25 * niceNumber;
    else if ( xGridSize < 0.5 * niceNumber ) niceNumber = 0.5 * niceNumber;

    // find next largest nice number above yStart
    var xStartRoundNumber = Math.ceil( this.xStart/niceNumber ) * niceNumber;
    // find next lowest nice number below yEnd
    var xEndRoundNumber = Math.floor( this.xEnd/niceNumber ) * niceNumber;

    // if the total x range is more than 5 days, format the timestamp as date instead of hours
    var b_formatAsDate = false;
    if ( this.xRange > 60*60*24*1000*5 ) b_formatAsDate = true;

    for ( var x = xStartRoundNumber ; x <= xEndRoundNumber ; x += niceNumber )
    {
        this.drawLine( this.xToPixelCoords( x ) , 0 , this.xToPixelCoords( x ) , this.height , this.gridColor );
        var date = new Date( x );
        var dateStr = "";
        if ( b_formatAsDate )
        {
            var day = date.getDate();
            if ( day < 10 ) day = "0"+day;
            var month = date.getMonth()+1;
            if ( month < 10 ) month = "0"+month;
            dateStr = day+"."+month;
        }
        else
        {
            var minutes = date.getMinutes();
            if ( minutes < 10 ) minutes = "0"+minutes;
            dateStr = date.getHours()+":"+minutes;
        }
        this.context.fillStyle = this.gridTextColor;
        this.context.fillText( dateStr , this.xToPixelCoords( x )+5 , this.height-5 );
    }
}



pingpoliCandlestickChart.prototype.calculateYRange = function()
{
    for ( var i = this.zoomStartID ; i < this.candlesticks.length ; ++i )
    {
        if ( i == this.zoomStartID )
        {
            this.yStart = this.candlesticks[i].low;
            this.yEnd = this.candlesticks[i].high;
        }
        else
        {
            if ( this.candlesticks[i].low < this.yStart )
            {
                this.yStart = this.candlesticks[i].low;
            }
            if ( this.candlesticks[i].high > this.yEnd )
            {
                this.yEnd = this.candlesticks[i].high;
            }
        }
    }
    this.yRange = this.yEnd - this.yStart;
}



pingpoliCandlestickChart.prototype.calculateXRange = function()
{
    this.xStart = this.candlesticks[this.zoomStartID].timestamp;
    this.xEnd = this.candlesticks[this.candlesticks.length-1].timestamp;
    this.xRange = this.xEnd - this.xStart;
}



pingpoliCandlestickChart.prototype.yToPixelCoords = function( y )
{
    return this.height - this.marginBottom - (y-this.yStart) * this.yPixelRange/this.yRange;
}



pingpoliCandlestickChart.prototype.xToPixelCoords = function( x )
{
    return this.marginLeft + (x-this.xStart) * this.xPixelRange/this.xRange;
}



pingpoliCandlestickChart.prototype.yToValueCoords = function( y )
{
    return this.yStart + ( this.height - this.marginBottom - y ) * this.yRange/this.yPixelRange;
}



pingpoliCandlestickChart.prototype.xToValueCoords = function( x )
{
    return this.xStart + ( x - this.marginLeft ) * this.xRange/this.xPixelRange;
}



pingpoliCandlestickChart.prototype.drawLine = function( xStart , yStart , xEnd , yEnd , color )
{
	this.context.beginPath();
    // to get a crisp 1 pixel wide line, we need to add 0.5 to the coords
	this.context.moveTo( xStart+0.5 , yStart+0.5 );
	this.context.lineTo( xEnd+0.5 , yEnd+0.5 );
	this.context.strokeStyle = color;
	this.context.stroke();
}



pingpoliCandlestickChart.prototype.fillRect = function( x , y , width , height , color )
{
	this.context.beginPath();
    this.context.fillStyle = color;
	this.context.rect( x , y , width , height );
	this.context.fill();
}



pingpoliCandlestickChart.prototype.drawRect = function( x , y , width , height , color )
{
	this.context.beginPath();
    this.context.strokeStyle = color;
	this.context.rect( x , y , width , height );
	this.context.stroke();
}



pingpoliCandlestickChart.prototype.formatDate = function( date )
{
    var day = date.getDate();
    if ( day < 10 ) day = "0"+day;
    var month = date.getMonth()+1;
    if ( month < 10 ) month = "0"+month;
    var hours = date.getHours();
    if ( hours < 10 ) hours = "0"+hours;
    var minutes = date.getMinutes();
    if ( minutes < 10 ) minutes = "0"+minutes;
    return day+"."+month+"."+date.getFullYear()+" - "+hours+":"+minutes;
}



pingpoliCandlestickChart.prototype.roundPriceValue = function( value )
{
    if ( value > 1.0 ) return Math.round( value*100 )/100;
    if ( value > 0.001 ) return Math.round( value*1000 )/1000;
    if ( value > 0.00001 ) return Math.round( value*100000 )/100000;
    if ( value > 0.0000001 ) return Math.round( value*10000000 )/10000000;
    else return Math.round( value*1000000000 )/1000000000;
}



pingpoliCandlestickChart.prototype.addTechnicalIndicator = function( indicator )
{
    indicator.onInit( this );
    this.technicalIndicators.push( indicator );
}



function MovingAverage( samples , color , lineWidth )
{
    this.samples = samples;
    this.color = color;
    this.lineWidth = lineWidth;
    this.data = [];
}



MovingAverage.prototype.onInit = function( candlestickChart )
{
    for ( var i = 0 ; i < candlestickChart.candlesticks.length ; ++i )
    {
        // average the number of samples
        var avg = 0;
        var counter = 0;
        for ( var j = i ; j > i-this.samples && j >= 0 ; --j )
        {
            avg += candlestickChart.candlesticks[j].close;
            ++counter;
        }
        avg /= counter;
        this.data.push( avg );
    }
}



MovingAverage.prototype.onAddCandlestick = function( candlestickChart , candlestickID )
{
    // average the number of samples
    var avg = 0;
    var counter = 0;
    for ( var i = candlestickID ; i > candlestickID-this.samples && i >= 0 ; --i )
    {
        avg += candlestickChart.candlesticks[i].close;
        ++counter;
    }
    avg /= counter;
    this.data.push( avg );
}



MovingAverage.prototype.onUpdateCandlestick = function( candlestickChart , candlestickID )
{
    // average the number of samples
    var avg = 0;
    var counter = 0;
    for ( var i = candlestickID ; i > candlestickID-this.samples && i >= 0 ; --i )
    {
        avg += candlestickChart.candlesticks[i].close;
        ++counter;
    }
    avg /= counter;
    this.data[candlestickID] = avg;
}



MovingAverage.prototype.draw = function( candlestickChart )
{
    var oldLineWidth = candlestickChart.context.lineWidth;
    candlestickChart.context.lineWidth = this.lineWidth;
    for ( var i = candlestickChart.zoomStartID ; i < this.data.length-1 ; ++i )
    {
        candlestickChart.drawLine( candlestickChart.xToPixelCoords( candlestickChart.candlesticks[i].timestamp ) , candlestickChart.yToPixelCoords( this.data[i] ) , candlestickChart.xToPixelCoords( candlestickChart.candlesticks[i+1].timestamp ) , candlestickChart.yToPixelCoords( this.data[i+1] ) , this.color );
    }
    candlestickChart.context.lineWidth = oldLineWidth;
}