// Globale Variablen
var user;
function setUser(userJSON){
    user = userJSON;
}
//loadUserJSON(1,setUser);

// LogIn-Seite
function tryLogin(){
    let mail = document.getElementById("inputEmail").value;
    let pwd = document.getElementById("inputPassword").value;
    checkUserCredentails(mail, pwd, login, loginFailed);
}
function login(userId){
    loadUserJSON(userId,function(userJSON){setUser(userJSON); switch2homePage()});
    //switch2homePage();
}
function loginFailed(){
    alert("Nutzername oder Passwort falsch.");
}
function checkUserCredentails(mail, pwd, callback_success, callback_fail){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var userJSON = JSON.parse(this.responseText)[0];
            if(!userJSON.user_password){
                callback_fail();
            }
            if(userJSON.user_password === pwd && userJSON.user_email === mail){
                callback_success(userJSON.user_id);
            }else{
                callback_fail();
            }
        }
    }
    const params = new URLSearchParams({
        user_email: mail,
      });
    console.log(params.toString());
    //xhttp.open("GET","http://192.168.2.168:8080/user?user_email="+mail+"",true);
    xhttp.open("GET","http://192.168.2.168:8080/user?"+params.toString(),true);
    xhttp.send();
}
function switch2homePage(){
    loadHTML('index',setNavbar);
}

// Home-Seite
function switch2modulePage(){
    let userId = user.user_id;
    loadHTML('modules',setNavbar);
    loadModules(userId);
    console.log("s2mods");
    console.log(user);
    
}

// Modul-Übersicht-Seite
function loadModules(userId){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var modulesOfUser = JSON.parse(this.responseText);
            console.log(modulesOfUser);
            modulesOfUser.forEach(function(module){
                console.log(modules);
                console.log(module);
                loadModule(module.module_id);
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

function switch2detailsPage(moduleJSON){
    console.log(moduleJSON);
    console.log("switch page to details page");
    loadHTML('details', showDetails, moduleJSON);
    
    //showDetails(moduleJSON); (in loadHTML)
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
    cardBodyDetailsClassLVL.innerHTML = "Klassenstufe "+moduleJSON.module_class_lvl;
    var cardBodyDetailsSubject = document.createElement("li");
    cardBodyDetailsSubject.classList = "list-group-item";
    cardBodyDetailsSubject.innerHTML = moduleJSON.module_subject;
    cardBodyDetails.appendChild(cardBodyDetailsClassLVL);
    cardBodyDetails.appendChild(cardBodyDetailsSubject);
    cardBody.appendChild(cardBodyDetails);
    var cardBodyBtnDetails = document.createElement("button");
    cardBodyBtnDetails.classList = "btn btn-primary mr-1";
    cardBodyBtnDetails.innerHTML = "Details";
    //cardBodyBtnDetails.onclick = function(){alert("teststeset");};
    cardBody.appendChild(cardBodyBtnDetails);
    cardBodyBtnDetails.onclick = function(){switch2detailsPage(moduleJSON)};
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

// Modul-Detail-Seite
function showDetails(moduleJSON){
    //console.log(moduleJSON);
    //console.log("POINT1");
    setNavbar();
    
    document.getElementById("module_title").innerHTML = moduleJSON.module_name;
    document.getElementById("module_description").innerHTML = moduleJSON.module_description;
    document.getElementById("module_class_level").innerHTML = "Klassenstufe "+moduleJSON.module_class_lvl;
    document.getElementById("module_id").innerHTML = moduleJSON.module_id;
    document.getElementById("module_subject").innerHTML = moduleJSON.module_subject;
    document.getElementById("module_created_at").innerHTML = moduleJSON.module_created_at;
    //document.getElementById("module_created_by").innerHTML = moduleJSON.module_created_by;
    loadUserJSON(moduleJSON.module_created_by,function(userJSON){
        console.log(userJSON);
        document.getElementById("module_created_by").innerHTML = userJSON.user_name;
    });
    document.getElementById("module_img").src = "images/"+moduleJSON.module_img_name;
    loadTasks(moduleJSON.module_id, function(tasksJSON){
        let tasksDiv = document.getElementById("tasks");
        tasksJSON.forEach(function(task){
            console.log(task);
            let tasksDivRow = document.createElement("div");
            tasksDivRow.classList += " row";
            tasksDiv.appendChild(tasksDivRow);
            let tasksDivRowDiv = document.createElement("div");
            tasksDivRowDiv.classList += " col-md-6";
            let tasksDivRowDivLabel = document.createElement("label");
            tasksDivRowDivLabel.innerHTML = "Aufgabe:";
            tasksDivRowDiv.appendChild(tasksDivRowDivLabel);
            tasksDivRow.appendChild(tasksDivRowDiv);
            let tasksDivRowDiv2 = document.createElement("div");
            tasksDivRowDiv2.classList += " col-md-6";
            tasksDivRow.appendChild(tasksDivRowDiv2);

            let tasksDivRow2 = document.createElement("div");
            tasksDivRow2.classList += " row";
            tasksDiv.appendChild(tasksDivRow2);
            let tasksDivRowDiv2 = document.createElement("div");
            tasksDivRowDiv2.classList += " col-md-6";
            let tasksDivRowDivLabel2 = document.createElement("label");
            tasksDivRowDivLabel2.innerHTML = task.task_title;
            tasksDivRowDiv2.appendChild(tasksDivRowDivLabel2);
            tasksDivRow2.appendChild(tasksDivRowDiv2);
            let tasksDivRowDiv2 = document.createElement("div");
            tasksDivRowDiv2.classList += " col-md-6";
            tasksDivRow2.appendChild(tasksDivRowDiv2);
        })
    });
}
function loadTasks(moduleId, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var tasksJSON = JSON.parse(this.responseText);
            console.log(tasksJSON);
            callback(tasksJSON);
        }
    }
    xhttp.open("GET","http://192.168.2.168:8080/tasks?module_id="+moduleId,true);
    xhttp.send();
}

// Hilfsfunktion - lädt neue HTML in aktuelles Dokument
function loadHTML(fileName, callback, param){
    var xhr= new XMLHttpRequest();
    xhr.open('GET', 'http://192.168.2.168/'+fileName+'.html', true);
    xhr.onreadystatechange= function() {
        if (this.readyState!==4) return;
        if (this.status!==200) return; // or whatever error handling you want
        document.getElementById('html_doc').innerHTML= this.responseText;
        //console.log("POINT0");
        //document.getElementById("home_title").innerText = "TEST :D";
        if(callback){
            callback(param);
        }
    };
    xhr.send();
}

function loadUserJSON(userId, callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            var userJSON = JSON.parse(this.responseText)[0];
            console.log(userJSON);
            callback(userJSON);
        }
    }
    xhttp.open("GET","http://192.168.2.168:8080/user?user_id="+userId+"",true);
    xhttp.send();
}

function setNavbar(){
    console.log("user:");
    console.log(user);
    document.getElementById("navbar_name").innerHTML = user.user_firstname + " "+user.user_lastname;
}