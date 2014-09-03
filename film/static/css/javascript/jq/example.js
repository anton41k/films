$(window).load(function() {

            
         

    function startBallOne() {
    $("#unicorn1").css("left", $("#unicorn1").position.left).circulate({
            sizeAdjustment: 150,
            speed: 5000,
            width: 820,
            height: 50,
            loop: true,
            zIndexValues: [1, 50, 50, 1]
    });

}
    function startBallTwo() {
    $("#unicorn2").css("left", $("#unicorn2").position.left).circulate({
            sizeAdjustment: 150,
            speed: 5000,
            width: 820,
            height: 50,
            loop: true,
            zIndexValues: [1, 50, 50, 1]
    });}
    
    setTimeout(startBallOne, 1000);
    setTimeout(startBallTwo, 2000);  
});

