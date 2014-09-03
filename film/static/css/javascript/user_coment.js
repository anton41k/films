function showFormall() {
    document.getElementById("authall").hidden = false;
   }
function showall() {
    document.getElementById("authall").hidden = true;
   }

function redact_on() {
    document.getElementById("profile").hidden = false;
   }
function redact_off() {
    document.getElementById("profile").hidden = true;
   }
function newfilm() {
    document.getElementById("newfilm").hidden = false;
   }
function closnewfilm() {
    document.getElementById("newfilm").hidden = true;
   }
function inbox() {
    document.getElementById("inbox").hidden = false;
    document.getElementById("sent").hidden = true;
   }
function sent() {
    document.getElementById("sent").hidden = false;
    document.getElementById("inbox").hidden = true;
   }
function send() {
    document.getElementById("sent").hidden = true;
    document.getElementById("inbox").hidden = true;
   }

function answer(x) {
    document.getElementById(x).hidden = false;
   }
function reset(x) {
    document.getElementById(x).hidden = true;
   }

function rating(x,y) {
    document.getElementById(y).hidden = false;
    document.getElementById(x).hidden = true;
   }
function ratingout(x,y) {
    document.getElementById(y).hidden = false;
    document.getElementById(x).hidden = true;
   }
