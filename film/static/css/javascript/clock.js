$(document).ready(function() {
// Создаем две переенные с названиями месяцев и дней недели в массиве
var monthNames = [ "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь" ]; 
var dayNames= ["Воскресенье","Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"]

// Создаем объект newDate()
var newDate = new Date();
// Извлекаем текущую дату из объекта Date
newDate.setDate(newDate.getDate());
// Навыходе день, дата, месяц и год    
$('#Date').html(dayNames[newDate.getDay()] + " " + newDate.getDate() + ' ' + monthNames[newDate.getMonth()] + ' ' + newDate.getFullYear());

setInterval( function() {
    // Создаем объект newDate() и извлекаем секунды текущего времени
    var seconds = new Date().getSeconds();
    // Добавляем начальный ноль к значению секунд
    $("#sec").html(( seconds < 10 ? "0" : "" ) + seconds);
    },1000);
    
setInterval( function() {
    // Создаем объект newDate() и извлекаем минуты текущего времени
    var minutes = new Date().getMinutes();
    // Добавляем начальный ноль к значению минут
    $("#min").html(( minutes < 10 ? "0" : "" ) + minutes);
    },1000);
    
setInterval( function() {
    // Создаем объект newDate() и извлекаем часы из текущего времени
    var hours = new Date().getHours();
    // Добавляем начальный ноль к значению часов
    $("#hours").html(( hours < 10 ? "0" : "" ) + hours);
    }, 1000);
    
}); 
