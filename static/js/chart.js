

// let metaData = {
//   information:"",
//   symbol:"",
//   lastRefresh:"",
//   outputSize:"",
//   timeZone:""
// }

let candleOhlcMappings = [];

let info = {
  yMin:[],
  xMin:[],
  yMax:[],
  xMax:[],
  l:0,
  h:0,
  minDate:"",
  maxDate:"",
}


let w = window.innerWidth - 30;
let h = window.innerHeight - 30;

let canvas = document.getElementById("myCanvas");
canvas.width = w;
canvas.height = h;
let ctx = canvas.getContext("2d");
let centerPoint = [w/2,h/2];
let boundaries = [w-50,h-50];

//amount of grid lines to evenly distribute for each axis
var xLines = 40;
var yLines = 100;

function getTimeslots(ohlc){
  let count = w/ohlc.length;
  return count;
}


let drawLine = (x,y,style=undefined) =>{
  ctx.beginPath();
  if(style){
    ctx.strokeStyle=style
  }
  ctx.moveTo(x[0], x[1]);
  ctx.lineTo(y[0], y[1]);
  ctx.stroke();
}
// 0 time
// 1 open
// 2 high
// 3 low
// 4 close
//DRAW CANDLESTICKS
function drawCandles(ohlc,dateRange,lp,hp,steps){
  let timeSlot = getTimeslots(ohlc);
  let idx = 0;
  console.log(steps);
  for(var candle of ohlc){
    console.log(timeSlot)
    console.log(candle)
    //x = maxPx - ((price - minPrice)/(maxPrice-minPrice)*maxPx)
    let calculatePosition = (price)=>{
      let maxPx = info.yMax[1]
      console.log(maxPx,price,lp,hp,maxPx);
      let x = maxPx-((price-lp)/(hp-lp)*maxPx)
      console.log("x",x);
      return x;
    }


    let open = candle[1]
    let low = candle[3]
    let close = candle[4]
    let high = candle[2]

    // y axis value for each price point
    let openPosition = Math.floor(calculatePosition(open));
    let lowPosition = Math.floor(calculatePosition(low));
    let highPosition = Math.floor(calculatePosition(high));
    let closePosition = Math.floor(calculatePosition(close));

    //pixel for candle center along x axis
    let currentStep = Math.floor(idx*timeSlot);


    if(openPosition > closePosition){ //x,y,w,h
      let height = openPosition-closePosition;
      ctx.fillStyle = "red";
      ctx.fillRect(currentStep-5, closePosition, 10, height);
      drawLine([currentStep,lowPosition],[currentStep,highPosition],"red");
      ctx.strokeStyle="black"
      ctx.beginPath();
      ctx.rect(currentStep-5, closePosition, 10, height);
      ctx.stroke();
    }else{
      let height = closePosition-openPosition;
      ctx.fillStyle = "green";
      ctx.fillRect(currentStep-5, openPosition, 10, height);
      drawLine([currentStep,lowPosition],[currentStep,highPosition],"green");
      ctx.strokeStyle="black"
      ctx.beginPath();
      ctx.rect(currentStep-5, openPosition, 10, height);
      ctx.stroke();
    }
    candleOhlcMappings.push({idx:idx,step:currentStep,positions:{openPosition:openPosition,lowPosition:lowPosition,highPosition:highPosition,closePosition:closePosition}});
    idx++;
  }
}

// CALCULATE AMOUNT OF ROWS TO FIT IN GRID
function calculateSteps()  {
//calculate horizontal lines across the Y axis
  let yDist = h/xLines;
  let yStep=yDist;
  let ySteps = [yStep];
  let yCount = 0;

  while(yCount != xLines){
    yCount++
    yStep+=yDist;
    ySteps.push(Math.floor(yStep));
  }

  //calculate vertical lines along the X axis
  let xDist = w/yLines;
  let xStep=xDist;
  let xSteps = [xStep];

  let xCount = 0;

  while(xCount< yLines){
    xCount++;
    xStep+=xDist;
    xSteps.push(Math.floor(xStep));
  }
  info.yMin = [0,0]
  info.yMax = [0,ySteps[ySteps.length-1]];
  info.xMin= [0,0];
  info.xMax = [xSteps[xSteps.length-1],0];
  return [xSteps,ySteps];
}

//DRAW GRID
function createGrid(lp,hp,dateRange){

  let drawHorizontal = (yPoints)=>{
    //draw top line
    drawLine([0,0],[w,0]);

    for(var point of yPoints){
      drawLine([0,point],[w,point], "grey")
    }
  }
  let drawVertical = (xPoints)=>{
    drawLine([0,0],[0,h]);

    for(var point of xPoints){
      drawLine([point,h],[point,0], "grey")
    }
  }
  let steps = calculateSteps();

  drawVertical(steps[0])
  drawHorizontal(steps[1])
  return steps;
}

function drawInfo(mousePos){
  drawLine([0,mousePos.y],[w,mousePos.y],"black");
  drawLine([mousePos.x,0],[mousePos.x,h],"black");
}

function getMousePos(canvas, evt) {
  var rect = canvas.getBoundingClientRect();
  return {
    x: evt.clientX - rect.left,
    y: evt.clientY - rect.top
  };
}

$(document).ready(function () {
  // var urls = "google.com";
  // 3FJ485A1KCAZCODB.ss
  // 1EATG6FH0JYICSWH
  var urls = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=aapl&apikey=1EATG6FH0JYICSWH';
  $.ajax({
    url: urls,
    dataType: 'json',
    contentType: "application/json",
    success: function (data) {
      console.log(data);
      // split the data set into ohlc and volume
      var i = 0;
      var ohlc = [];
      var volume = [];
      let hp = 0;
      let lp = Infinity;
      let dateRange = ["",""];
      var dataLength = data['Time Series (Daily)'];

      for(var time in dataLength)
      {

        var stock_info = dataLength[time];

        let newOHLC = [
          time,
          Number(stock_info["1. open"]),
          Number(stock_info["2. high"]),
          Number(stock_info["3. low"]),
          Number(stock_info["4. close"])
        ];

        ohlc.push(newOHLC);

        if(i==0){
          //set max/min date
          dateRange[0]=newOHLC[0];
        }
        if(newOHLC[2]>hp){
          //found highest point
          hp = newOHLC[2];
        }
        if(newOHLC[3]<lp){
          //found the lowest point
          lp = newOHLC[3];
        }

        volume.push([
          time, // the date
          Number(stock_info["5. volume"]) // the volume
        ]);

        i+=1;
      }
      let addEvent = () => {
        let state = "loading";
        canvas.addEventListener('mousemove', function(evt) {
          if(state=="progress"){
            return;
          }
//           state == "progress";
//           var mousePos = getMousePos(canvas, evt);
//           var message = 'Mouse position: ' + mousePos.x + ',' + mousePos.y;


//           var img = new Image();
//           img.onload = function () {
//             ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
//           }
//           img.src = dataUri;
//           drawInfo(mousePos);
//           state == "finished";
        }, false);
      }
      setTimeout(addEvent, 500);
      ctx.fillStyle="white";
      ctx.fillRect(0,0,w,h);
      ctx.fillStyle="black";

      //set max/min date
      dateRange[1]=ohlc[i-1][0];
      let steps = createGrid(lp,hp,dateRange);
      drawCandles(ohlc,dateRange,lp,hp,steps)
      var dataUri = canvas.toDataURL();

    }
  });
});
