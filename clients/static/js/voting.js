function vote(elemId, target) {
	var elem = document.getElementById(elemId);
	var votingLabel = elem.getElementsByClassName('votes')[0];
	var value;
    if (target.closest('.down')) {
    	value = -1;
    } else if (target.closest('.up')) {
    	value = 1;
    }
	dojo.xhrGet({
		url: "setvote/?id=" + elemId + "&value=" + value,
		handleAs: "text",
		load: function(data){
			console.log(data);
			votingLabel.innerHTML = data;
		},
		error: function(error){
			console.log("An unexpected error occurred: " + error);
		}
	})
    
}
