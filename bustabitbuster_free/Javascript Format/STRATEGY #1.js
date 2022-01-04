var config = {
	baseBet: { value: '100', type: 'balance', label: 'Base Bet'},
	minBet: { value: '100', type: 'balance', label: 'Min Bet'},
	maxBet: { value: '1e8', type: 'balance', label: 'Max Bet'},
	protectBal: { value: '100000', type: 'balance', label: 'Protect Balance'},
};

var baseBet = config.baseBet.value; 
var baseMultiplier = 2; 

var minBet = config.minBet.value; 
var maxBet = config.maxBet.value; 
var protectBal = config.protectBal.value; 


// DO NOT CHANGE
var currentBet = baseBet;
var currentMultiplier = baseMultiplier;
var currentMinBet = minBet;
var currentMaxBet = maxBet;

// LOCKERS
var betUnlock = true;
var recoveryOn = false;
var OktoGo = true;

var putBet = currentBet;
var putMultiplier = currentMultiplier;

engine.on('GAME_STARTING', function() {
    
    if (userInfo.balance < protectBal) {
        stop('Script was Stopped due to balance is protected. balance is '+ userInfo.balance);
    }
    if (putBet >= currentMaxBet) {
        stop('Script was Stopped due to the bet size exceeded maximum allowed bet size');
    }
    if (putBet < currentMinBet) {
        stop('Script was Stopped due to the bet size is lower than allowed minimum bet size');
    } 
    
    if (OktoGo && betUnlock){
        engine.bet(parseInt(putBet), parseFloat(putMultiplier));
		log('You are ready to play! ');
        log('A bet will be placed:- Bet Size: '+ putBet/100 +' Multiplier: '+ putMultiplier);
    }   
    
});

engine.on('GAME_STARTED', function() {
	if (engine.getCurrentBet()){
		var cbet = engine.getCurrentBet();
		log('Game Started with '+ (cbet.wager/100) + ' * ' + cbet.payout+ 'x');
	} else {
		log('A bet did not placed!');
	}
});


engine.on('GAME_ENDED', function() {
    
	var lastGame = engine.history.first();
	
    log('Game crashed at '+ lastGame.bust);
	
	log('Last Game wagered at '+ (lastGame.wager)/100);
    
    if (lastGame.wager > 0){
        if (lastGame.cashedAt){
            putBet = currentBet;
            recoveryOn = false;
            betUnlock = true;
            log('You Won the Last Game');
        } else {
			recoveryOn = true;
            log('You Lost the Last Game. Recovery Mode is Activated');
		}
    }
    if (recoveryOn && (lastGame.wager > 0) && lastGame.cashedAt == false){
        putBet *= 2;
        betUnlock = false;
        log('You are about to skip next game.');
    } else{
        betUnlock = true;
		log('Recovery Mode is Deactivated');
    }
});




