
dojo.require("dojox.grid.EnhancedGrid");
dojo.require("dojox.grid.enhanced.plugins.NestedSorting");
dojo.require("dojox.grid.enhanced.plugins.filter");
dojo.require("dojox.grid.enhanced.plugins.filter.FilterBar");
dojo.require("dojox.grid.enhanced.plugins.Cookie");
dojo.require("dojox.grid.enhanced.plugins.Pagination");
dojo.require("dojo.data.ItemFileWriteStore");
dojo.require("dijit.layout.ContentPane");
dojo.require("dijit.Dialog");
dojo.require("dijit.form.Button");
dojo.require("dijit.form.TextBox");
dojo.require('dijit.form.DateTextBox');
dojo.require('dojo.cookie')
dojo.require("dojo.dom");
dojo.require("dojo.on");
dojo.require("dojo.io.iframe");
	
function formatType(value){
	return "<img src='" + MYMEDIA + value + "' alt='Photo' width='64' height='64'/>";
}


function onAddNew () {
    var form = dojo.dom.byId('add-form');
    dojo.on(form, 'submit', function (evt) {
        evt.stopPropagation();
        evt.preventDefault();

        var errMsg = '';
        var form_error = false;
        if (document.getElementById('id_last_name').value.length == 0) {
            errMsg += 'Введите, пожалуйста, фамилию!';
            form_error = true;
        }
        if (document.getElementById('id_first_name').value.length == 0) {
            errMsg += 'Введите, пожалуйста, имя!';
            form_error = true;
        }
        var file = dojo.query('#id_photo')[0]; //dijit.byId('symbology-import-file').getFileList();//
        if (file.files.length == 0) {
            errMsg += 'Выберите, пожалуйста, файл!';
            form_error = true;
        } else {
            var fileType = file.files[0].type; //file[0].type;//
            var fileSize = file.files[0].size; //file[0].size;//

            if (fileType.search('image/') == -1 || fileType.indexOf('svg+xml') != -1) {
                errMsg += 'Выберите, пожалуйста, графические файлы!';
                form_error = true;
            };
        }
        if (form_error == false) {
            dojo.io.iframe.send({
                url: 'save/',
                method: 'POST',
                form: 'add-form',
                headers: {
                    'X-CSRFToken': dojo.cookie('csrftoken')
                },
                handleAs: 'text',
                load: function (response, ioArgs) {
                    setStore();

                    if (response.search('ok') != -1) {
                        alert('Новый клиент добавлен');
                        document.getElementById("add-form").reset();
                        dijit.byId("add-new-dialog").hide();
                    };
                    if (response.search('error') != -1) {
                        alert('Произошла ошибка: ' + response);
                    };
                },
                error: function (response, ioArgs) {
                	alert('Произошла ошибка: ' + response);
                }
            });
        } else {
            alert(errMsg);
        }
    })
    var input_form = document.getElementById('add-form');
    if (input_form != undefined) {
    	input_form.setAttribute('style', 'display: table');
    }
    var dialogWindow = dijit.byId('add-new-dialog');
    dialogWindow.show();
}

function makeStore(data) {
	var field_list = data['field_list'];
	var client_list = data['client_list'];
	var headers = [[
      {'field': 'id', 'width': '20px'},
      {'field': 'first_name', 'width': '100px'},
      {'field': 'last_name', 'width': '100px'},
      {'field': 'date_of_birth', 'width': '100px'},
      {'field': 'age', 'width': '50px'},
      {'field': 'photo', 'formatter': formatType, 'width': '100px'},
      {'field': 'votes', 'width': '50px'}
    ]];
    for (var i in headers[0]) {
        headers[0][i]['name'] = field_list[headers[0][i]['field']];
    }
	var data = {
	  identifier: 'id',
	  items: client_list
	};
	return {'headers': headers, 'storedata': data};
}

function setStore() {
	dojo.xhrGet({
		url: "getall/",
		handleAs: "json",
		load: function(data){
		    var myStore = makeStore(data);
		    var store = new dojo.data.ItemFileWriteStore({data: myStore['storedata']});
            var grid = dijit.byId('grid');
			grid.store.close();
            grid.setStructure(myStore['headers']);
			grid.setStore(store);
		    grid._refresh();
            grid.autoWidth = true;
            grid.autoHeight = true;
            grid.update();
		},
		error: function(error){
			console.log("An unexpected error occurred: " + error);
		}})
}

function deleteSelected() {
    var items = dijit.byId('grid').selection.getSelected();
    var gridStore = dijit.byId('grid').store;
    if (items.length) {
    	var ids = [];
        dojo.forEach(items, function (selectedItem) {
            if (selectedItem !== null) {
            	ids.push(selectedItem['id'][0]);
                gridStore.deleteItem(selectedItem);
            } 
        });
		dojo.xhrGet({
			url: "delete/?ids=" + ids,
			handleAs: "text",
			load: function(data){

			},
			error: function(error){
				console.log("An unexpected error occurred: " + error);
			}
		})
    }
}

function setAge(date1) {
    var date2 = new Date();
    var years = date2.getFullYear() - date1.getFullYear();
    var months = years * 12 + date2.getMonth() - date1.getMonth();
    var days = date2.getDate() - date1.getDate(); 
    years -= date2.getMonth() < date1.getMonth();
    document.getElementById('id_age').value = years;
}

dojo.ready(function(){
    myStore = new dojo.data.ItemFileWriteStore({
        data: {
            identifier: 'id',
            items: []
        }
    });
    var grid = new dojox.grid.EnhancedGrid({
        id: 'grid',
        //structure: storeInfo['headers'],
        store: myStore,
        rowSelector: '25px',
        style: 'max-width: 800px; height: 85%;',
        plugins : {
            nestedSorting: true,

            pagination: {
                pageSizes: ["10", "25", "50", "100", "All"],
                description: true,
                sizeSwitch: true,
                pageStepper: true,
                gotoButton: true,
                maxPageStep: 7,
                position: "bottom"
            },
            filter: {
                itemsName: ' клиентов',
                closeFilterbarButton: false,
                ruleCount: 100
            }
        }
    });
    dojo.byId("gridDiv").appendChild(grid.domNode);
    grid.startup();
    setStore();
});