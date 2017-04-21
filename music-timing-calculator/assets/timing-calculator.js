(function () {
  "use strict";
  
  var input = {
    tempo: document.getElementById("tempo"),
    beats: document.getElementById("beats"),
    measures: document.getElementById("measures"),
    numDigits: document.getElementById("num-digits")
  };
  
  var output = {
    oneBeat: document.getElementById("one-beat"),
    oneMeasure: document.getElementById("one-measure"),
    songLength: document.getElementById("song-length"),
    songLengthMin: document.getElementById("song-length-min")
  };
  
  
  function calculateResult(tempo, beats, measures) {
    var result = {
      oneBeat: 0,
      oneMeasure: 0,
      songLength: 0,
      songLengthMin: [0, 0]
    };
    if (tempo > 0) {
      result.oneBeat = 60 / tempo;
      result.oneMeasure = result.oneBeat * Math.max(beats, 0) || 0;
      result.songLength = result.oneMeasure * Math.max(measures, 0) || 0;
      result.songLengthMin[0] = Math.floor(result.songLength / 60) || 0;
      result.songLengthMin[1] = result.songLength % 60 || 0;
    }
    return result;
  }
  
  
  function roundToFixed(inputNum, numDigits) {
    if ((numDigits || numDigits === 0) && numDigits >= 0 && numDigits <= 20) {
      return inputNum.toFixed(numDigits);
    }
    return inputNum;
  }
  
  
  function formatTime(time, numDigits) {
    if (typeof time === "number") {
      return roundToFixed(time, numDigits) + " sec";
    } else {
      var minutes = roundToFixed(time[0], 0);
      var seconds = roundToFixed(time[1], numDigits);
      return minutes + " min " + seconds + " sec";
    }
  }
  
  
  function formatResult(result, numDigits) {
    var newResult = {};
    for (var key in result) {
      if (result.hasOwnProperty(key)) {
        newResult[key] = formatTime(result[key], numDigits);
      }
    }
    return newResult;
  }
  
  
  function updatePage(e) {
    var tempo = parseFloat(input.tempo.value);
    var beats = parseFloat(input.beats.value);
    var measures = parseFloat(input.measures.value);
    var numDigits = parseInt(input.numDigits.value, 10);
    var result = calculateResult(tempo, beats, measures);
    result = formatResult(result, numDigits);
    for (var key in result) {
      if (result.hasOwnProperty(key)) {
        output[key].value = result[key];
      }
    }
    if (e) {
      e.preventDefault();
    }
  }
  
  
  function resetPage() {
    for (var elem in input) {
      if (input.hasOwnProperty(elem)) {
        input[elem].value = "";
      }
    }
    updatePage();
  }
  
  
  document.getElementById("input-form").addEventListener("submit", updatePage);
  document.getElementById("reset").addEventListener("click", resetPage);
  
  updatePage();
})();
