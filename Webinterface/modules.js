loadModule(1);

function loadModules(userId){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var modulesOfUser = this.responseText;
            modulesOfUser.forEach(function(module){
                console.log(module);
                showModule(module.module_id);
            });
        }
    }
    xhttp.open("GET","http://192.168.2.168:8080/user_module?user_id="+userId+"",true);
    xhttp.send();
}

function loadModule(moduleId){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var moduleJSON = JSON.parse(this.responseText)[0];
            console.log(moduleJSON)
            addModuleCard(moduleJSON);
        }
    }
    xhttp.open("GET","http://192.168.2.168:8080/modules?module_id="+moduleId+"",true);
    xhttp.send();
}

function addModuleCard(moduleJSON){
    var card = document.createElement("div");
    card.classList = "card border-primary";
    var cardImg = document.createElement("img");
    cardImg.classList = "card-img-top cardimg";
    cardImg.src = "images/"+moduleJSON.module_img_name;
    card.appendChild(cardImg);
    var cardBody = document.createElement("div");
    cardBody.classList = "card-body";
    var cardBodyTitle = document.createElement("h5");
    cardBodyTitle.innerHTML = moduleJSON.module_name;
    cardBody.appendChild(cardBodyTitle);
    var cardBodyDescription = document.createElement("p");
    cardBodyDescription.innerHTML = moduleJSON.module_description;
    cardBodyDescription.classList = "card-text";
    cardBody.appendChild(cardBodyDescription);
    var cardBodyDetails = document.createElement("ul");
    cardBodyDetails.classList = "list-group list-group-flush";
    var cardBodyDetailsClassLVL = document.createElement("li");
    cardBodyDetailsClassLVL.classList = "list-group-item";
    cardBodyDetailsClassLVL.innerHTML = moduleJSON.class_lvl;
    var cardBodyDetailsSubject = document.createElement("li");
    cardBodyDetailsSubject.classList = "list-group-item";
    cardBodyDetailsSubject.innerHTML = moduleJSON.module_subject;
    cardBodyDetails.appendChild(cardBodyDetailsClassLVL);
    cardBodyDetails.appendChild(cardBodyDetailsSubject);
    cardBody.appendChild(cardBodyDetails);
    var cardBodyBtnDetails = document.createElement("button");
    cardBodyBtnDetails.onclick = "showDetails("+moduleJSON.module_id+")";
    cardBodyBtnDetails.classList = "btn btn-primary mr-1";
    cardBodyBtnDetails.innerHTML = "Details";
    cardBody.appendChild(cardBodyBtnDetails);
    var cardBodyBtnExport = document.createElement("button");
    cardBodyBtnExport.onclick = "showExport("+moduleJSON.module_id+")";
    cardBodyBtnExport.classList = "btn btn-primary";
    cardBodyBtnExport.innerHTML = "Export";
    cardBody.appendChild(cardBodyBtnExport);
    card.appendChild(cardBody);

    var boxCard = document.createElement("div");
    boxCard.classList = "col-sm-6 col-md-4 col-lg-3 col-xl-3 mb-2";
    boxCard.appendChild(card);
    document.getElementById("modules").appendChild(boxCard);
}